# 🧪 25 — Self-Healing Compilers & Runtime Code Recovery

> *"Sebuah sistem yang handal tidak sekadar mendeteksi kerusakan; ia memperbaikinya saat proses kompilasi berjalan."*

---

## 📋 Daftar Isi

1. [Filosofi Self-Healing](#-filosofi-self-healing)
2. [Alur Pemulihan Mandiri (Self-Healing Loop Architecture)](#-alur-pemulihan-mandiri-self-healing-loop-architecture)
3. [Integrasi dengan CLI Compiler (CLI Compiler Integration)](#-integrasi-dengan-cli-compiler-cli-compiler-integration)
4. [Tabel Klasifikasi Kesalahan Kompilasi (Compilation Errors Classification)](#-tabel-klasifikasi-kesalahan-kompilasi-compilation-errors-classification)
5. [Implementasi Kode Pemulihan (Self-Healing Python Agent Script)](#-implementasi-kode-pemulihan-self-healing-python-agent-script)
6. [Mitigasi Loop Pemulihan Tak Terbatas (Infinite Recovery Prevention)](#-mitigasi-loop-pemulihan-tak-terbatas-infinite-recovery-prevention)
7. [Anti-Patterns Self-Healing](#-anti-patterns-self-healing)

---

## 🎯 Filosofi Self-Healing

Self-Healing Compilers adalah **sekumpulan mekanisme pemulihan kode runtime secara otomatis**. Ketika compiler (seperti `tsc` untuk TypeScript, `rustc` untuk Rust, atau runtime `node`) mengembalikan error, agen tidak langsung menyerah atau bertanya pada pengguna. Agen menangkap manifestasi error, mengisolasi baris kode yang rusak, dan menerapkan perbaikan secara langsung dalam satu siklus kompilasi.

---

## 🏗️ Alur Pemulihan Mandiri

Siklus penangkapan kesalahan dan perbaikan kode berjalan secara dinamis sebagai berikut:

```
    Tulis Kode ──► Jalankan Compiler ──► [Kompilasi Sukses?]
                                                 ├── YA  ──► Selesai
                                                 └── TIDAK ──► Baca Stack Trace
                                                                     │
                                                                     ▼
                                                              Ubah Kode Rusak 
                                                              (Re-compile Loop)
```

---

## 💻 Integrasi dengan CLI Compiler

Agen harus membungkus setiap perintah build/test dengan skrip penangkap stderr:
* **TypeScript Compiler (`tsc`)**: Jalankan dengan flag `--pretty false` agar parser regex dapat dengan mudah memotong detail baris dan kolom yang error.
* **Rust Compiler (`rustc`)**: Gunakan format output JSON (`--error-format=json`) untuk mendapatkan metadata baris kode yang bermasalah secara langsung.

### Perintah CLI untuk Menangkap Output Error:
```bash
# Compile and output clean error messages without formatting to compile_errors.log
npx tsc --noEmit --pretty false > compile_errors.log 2>&1 || true

# Extract specific line numbers from the TypeScript compiler output
grep -E "error TS[0-9]+:" compile_errors.log | head -n 5
```

---

## 📊 Tabel Klasifikasi Kesalahan Kompilasi

| Kode Kesalahan | Jenis Masalah | Contoh Pesan Error | Tindakan Korektif Otomatis |
| :--- | :--- | :--- | :--- |
| `TS2307` | Missing Import Module | *Cannot find module 'lodash'* | Jalankan `npm install --save-dev @types/lodash`. |
| `TS2322` | Type Mismatch | *Type 'string' is not assignable to 'number'* | Sesuaikan definisi tipe atau gunakan fungsi parser data. |
| `TS2339` | Property Missing | *Property 'id' does not exist on type 'User'* | Perbarui antarmuka (interface) data terkait. |

---

## 💻 Implementasi Kode Pemulihan

Skrip Python di bawah ini memotong baris file yang salah dari output compiler TypeScript dan mengirimkan instruksi perbaikan khusus ke model:

```python
import re

class SelfHealingCompiler:
    def __init__(self, error_log_path: str):
        self.error_log_path = error_log_path

    def parse_typescript_errors(self) -> list:
        errors = []
        # Pattern to match: src/auth.ts(12,5): error TS2322: Type 'X' is not assignable to 'Y'
        pattern = re.compile(r"^(.*?)\((\d+),(\d+)\): error (TS\d+): (.*)$")
        
        with open(self.error_log_path, 'r') as f:
            for line in f:
                match = pattern.match(line.strip())
                if match:
                    file_path, line_num, col_num, error_code, message = match.groups()
                    errors.append({
                        "file": file_path,
                        "line": int(line_num),
                        "column": int(col_num),
                        "code": error_code,
                        "message": message
                    })
        return errors

# Usage Example:
# healer = SelfHealingCompiler('compile_errors.log')
# detected_errors = healer.parse_typescript_errors()
# print(f"Isolated {len(detected_errors)} compiler errors.")
```

---

## 🛡️ Mitigasi Loop Pemulihan Tak Terbatas

Untuk menghindari agen merusak file lain dalam upaya perbaikan yang salah:
1. **Maksimum Percobaan (Retry Limit)**: Batasi siklus perbaikan maksimal 3 kali untuk satu baris kode yang sama.
2. **Backtrack System**: Jika percobaan ketiga tetap gagal, kembalikan file ke status checkout awal (`git checkout -- <file_path>`) dan laporkan detail kegagalan kompilasi ke pengguna.

---

## ⚠️ Anti-Patterns Self-Healing

* ❌ **Blind Regex Replacements**: Melakukan pencarian dan penggantian teks (find-replace) secara serabutan tanpa memvalidasi struktur AST file.
* ❌ **Ignoring Parent Errors**: Mencoba memperbaiki kesalahan tipe di hilir (downstream code) sebelum memperbaiki pustaka induk (parent package dependency) yang hilang.
* ❌ **Infinite Compile Loops**: Mengulang instruksi build tanpa memeriksa status file yang berubah, sehingga membuang-buang token API.
