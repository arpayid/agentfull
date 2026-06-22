# 🤖 09 — Tool Mastery & Context Pruning (SOTA 2026)

> *"Kehebatan seorang agen otonom tidak hanya diukur dari kemampuan menulis kodenya, melainkan dari efisiensi pemanfaatan perkakas (tools) dan kecerdasan memangkas beban memori percakapan."*

---

## 📋 Daftar Isi / Table of Contents
1. [Filosofi Penguasaan Alat](#-filosofi-penguasaan-alat)
2. [Master-Level Tool Orchestration (Orkestrasi Alat Tingkat Master)](#-master-level-tool-orchestration)
3. [RLEF (Reinforcement Learning from Execution Feedback)](#-rlef)
4. [Context Pruning & Lost-in-the-Middle Prevention](#-context-pruning)
5. [Custom Tool Creation (Pembuatan Alat Mandiri)](#-custom-tool-creation)
6. [Anti-Patterns dalam Penggunaan Alat](#-anti-patterns)

---

## 🎯 Filosofi Penguasaan Alat

Pada ekosistem SOTA 2026, agen cerdas beroperasi layaknya insinyur sistem senior. Alat-alat seperti terminal shell, pencarian berkas (*file search*), penelusuran regex (*grep*), dan penelusuran web (*web fetch*) tidak digunakan secara acak. Agen harus memahami keterbatasan setiap alat, memperkirakan waktu eksekusi, serta memilih alat yang menghasilkan keluaran paling bersih dengan konsumsi sumber daya paling hemat.

```
                  ┌────────────────────────────────────────┐
                  │             DIAGNOSTIC TASK            │
                  └──────────────────┬─────────────────────┘
                                     │
                                     ▼
                  ┌────────────────────────────────────────┐
                  │        SELECT EFFICIENT TOOL           │
                  └────────┬──────────────────────┬────────┘
                           │                      │
                  [Standard File Scan]     [Heavy 1GB Log Scan]
                           │                      │
                           ▼                      ▼
                  ┌─────────────────┐    ┌─────────────────┐
                  │     Glob/Grep   │    │  Stream Tail /  │
                  │   Direct search │    │   Regex Filter  │
                  └─────────────────┘    └─────────────────┘
```

---

## 🔧 Master-Level Tool Orchestration (Orkestrasi Alat Tingkat Master)

Gunakan perintah terminal secara efisien. Hindari memuat data sampah ke dalam memori kerja agen yang dapat mendegradasi kemampuan analisis logis.

### Praktik Terbaik Penggunaan Perintah / Best Practices CLI Commands

- **Batas Pembacaan Log:** Jangan pernah menjalankan perintah `cat` pada file log berukuran besar. Gunakan pemotongan streaming seperti `tail` atau pencarian terfilter.
- **Pencarian Berkas Terarah:** Gunakan perkakas pencarian terarah seperti `find` atau `glob` dengan kriteria spesifik untuk menghindari hasil pencarian ribuan berkas tak relevan.

```bash
# Contoh 1: Mencari string error secara efisien pada log tanpa memuat file ke memory
tail -n 500 /var/log/application.log | grep -i "exception"

# Contoh 2: Mencari file konfigurasi typescript di dalam direktori proyek
find . -maxdepth 3 -name "tsconfig.json"
```

---

## 🔁 RLEF (Reinforcement Learning from Execution Feedback)

Jangan pernah memberikan kode mentah kepada pengguna dan membiarkan mereka menjadi kelinci percobaan untuk menguji error kompilasi. Terapkan siklus pembelajaran umpan balik eksekusi secara mandiri (*Self-Validation Loop*):

```
                   ┌────────────────────────────────────────┐
                   │             WRITE CODE FILE            │
                   └──────────────────┬─────────────────────┘
                                      │
                                      ▼
                   ┌────────────────────────────────────────┐
                   │        EXECUTE RUNTIME / COMPILER      │
                   └──────────────────┬─────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                  [Exit Code = 0]           [Exit Code != 0]
                         │                         │
                         ▼                         ▼
                  ┌──────────────┐          ┌──────────────┐
                  │  Test Passed │          │ Read Error & │
                  │ Deliver Code │          │  Self-Heal   │
                  └──────────────┘          └──────────────┘
```

1. **Write:** Tulis kode ke dalam file proyek.
2. **Execute Validation:** Jalankan perintah kompilasi atau tes lokal secara diam-diam di latar belakang.
3. **Capture Feedback:** Baca status keluaran (*exit code*) dan pesan kegagalan dari terminal secara mandiri.
4. **Self-Heal:** Perbaiki kode Anda kembali berdasarkan pesan kesalahan tersebut hingga program lolos kompilasi 100%, baru serahkan hasil akhir kepada pengguna.

```bash
# Validasi sintaksis TypeScript sebelum melaporkan ke user
npx tsc --noEmit
```

---

## ✂️ Context Pruning & Lost-in-the-Middle Prevention

Ketika sesi interaksi berlangsung lama, memori kerja agen akan dipenuhi oleh log kesalahan, perintah terminal yang tidak berhasil, dan sisa-sisa debug lama. Hal ini dapat memicu bias keputusan kognitif.

### Langkah Pembersihan Memori / Context Cleaning Steps

- **Create Internal Summary:** Secara berkala, ringkas hasil temuan absolut ke dalam satu paragraf kecil.
- **Discard Noise:** Abaikan log uji coba yang gagal dari ingatan aktif Anda. Fokuskan seluruh sisa memori kerja pada rangkuman ringkas terbaru.
- **Selective Memory Reset:** Minta pembersihan riwayat obrolan jika tugas utama telah diselesaikan sepenuhnya dan Anda beralih ke fitur baru yang tidak berhubungan.

---

## 💡 Custom Tool Creation (Pembuatan Alat Mandiri)

Jika perkakas bawaan tidak memadai untuk menyelesaikan tugas yang rumit (misalnya: memindai perbedaan struktur data XML kompleks di 100 direktori), buat alat bantu Anda sendiri secara otonom.

- Tulis skrip pembantu singkat (misal dalam bahasa Python atau Bash).
- Jalankan skrip tersebut di terminal untuk mendapatkan data analitik.
- Hapus skrip pembantu tersebut setelah data terkumpul untuk menjaga kebersihan sistem (*clean environment*).

```python
# Script analyzer.py dibuat secara dinamis untuk analisis AST terarah, lalu dihapus
import ast
import sys

# Scan AST for hardcoded API keys
with open(sys.argv[1], "r") as f:
    tree = ast.parse(f.read())
    # Logika analisis spesifik...
```

---

## 🚫 Anti-Patterns dalam Penggunaan Alat

- **Lethargic Coder Pattern:** Memberikan kode mentah ke pengguna tanpa pernah menjalankan tes atau memverifikasi apakah kode tersebut bisa dikompilasi secara lokal.
- **Spamming Commands:** Menjalankan perintah acak seperti `ls -la` atau `pwd` berulang-ulang tanpa tujuan diagnostik yang jelas.
- **Context Flooding:** Membaca berkas gambar biner, file zip, atau berkas pustaka eksternal (`node_modules`) ke dalam token obrolan.

---

*(Penggunaan alat secara presisi adalah tanda kedewasaan profesional seorang agen rekayasa perangkat lunak.)*
