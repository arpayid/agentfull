# 🛡️ 13 — Behavioral Guardrails & Infinite Loop Prevention

> *"Kemampuan untuk berhenti dan berbalik arah saat mendeteksi kesalahan berulang adalah tanda kecerdasan tingkat tinggi."*

---

## 📋 Daftar Isi

1. [Filosofi Guardrails](#-filosofi-guardrails)
2. [Arsitektur Deteksi Loop (Loop Detection Architecture)](#-arsitektur-deteksi-loop-loop-detection-architecture)
3. [Algoritma Pendeteksi Loop Perilaku (Behavioral Loop Detector Algorithm)](#-algoritma-pendeteksi-loop-perilaku-behavioral-loop-detector-algorithm)
4. [Mekanisme Pemotongan Loop (Loop Breakers Mechanism)](#-mekanisme-pemotongan-loop-loop-breakers-mechanism)
5. [Tabel Aturan Perilaku Pengamanan (Behavioral Safety Rules)](#-tabel-aturan-perilaku-pengamanan-behavioral-safety-rules)
6. [Langkah Eskalasi ke Pengguna (User Escalation Steps)](#-langkah-eskalasi-ke-pengguna-user-escalation-steps)
7. [Anti-Patterns Guardrails](#-anti-patterns-guardrails)

---

## 🎯 Filosofi Guardrails

Behavioral Guardrails adalah **pagar pembatas logis** yang mencegah agen dari perilaku anomali, seperti mengulang perintah yang sama secara terus-menerus meskipun hasilnya selalu gagal. Agen harus bertindak secara sadar diri (metacognition) untuk mendeteksi kemacetan logika sebelum menghabiskan token atau merusak workspace.

---

## 🔍 Arsitektur Deteksi Loop

Agen harus memantau riwayat aktivitasnya sendiri secara real-time untuk mendeteksi perintah CLI atau pemanggilan tool yang identik:

```
                  ┌───────────────────────┐
                  │   EKSEKUSI PERINTAH   │
                  └───────────┬───────────┘
                              │
                  ┌───────────┴───────────┐
                  │    VERIFIKASI LOG     │
                  └───────────┬───────────┘
                              │
            [Apakah Output Identik 3x Berturut?]
             ├── YA  → Aktifkan Anti-Loop Protocol! (Ubah Asumsi)
             └── TIDAK → Lanjutkan Eksekusi Normal
```

---

## 💻 Algoritma Pendeteksi Loop Perilaku

Berikut adalah contoh fungsi pemantau (monitoring utility) dalam Python yang berjalan di dalam runtime agen untuk mendeteksi kegagalan berturut-turut:

```python
import json
import hashlib

class ActionMonitor:
    def __init__(self, threshold: int = 3):
        self.history = []
        self.threshold = threshold

    def _hash_action(self, tool_name: str, arguments: dict) -> str:
        # Normalize and serialize arguments to ensure stable hashing
        serialized = json.dumps(arguments, sort_keys=True)
        raw_string = f"{tool_name}:{serialized}"
        return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

    def record_and_check_loop(self, tool_name: str, arguments: dict) -> bool:
        action_hash = self._hash_action(tool_name, arguments)
        self.history.append(action_hash)
        
        # Check last N items in history
        if len(self.history) >= self.threshold:
            last_n = self.history[-self.threshold:]
            if len(set(last_n)) == 1:
                print(f"[Guardrail Alert] Loop detected on tool '{tool_name}'!")
                return True
        return False

# Usage Example:
# monitor = ActionMonitor(threshold=3)
# monitor.record_and_check_loop("bash", {"command": "npm install"}) -> False
# monitor.record_and_check_loop("bash", {"command": "npm install"}) -> False
# monitor.record_and_check_loop("bash", {"command": "npm install"}) -> True (Trigger Loop Breaker)
```

---

## ⚡ Mekanisme Pemotongan Loop

Jika loop terdeteksi, ambil langkah penyelamatan berikut:
1. **Hard Reset Asumsi**: Hapus semua asumsi solusi saat ini. Tulis ulang hypothesis list di memori kerja.
2. **Ubah Sudut Pandang (Pivot)**: Cari jalur alternatif (misal: jika instalasi `npm` gagal terus, coba ganti ke `yarn` atau gunakan file `.js` murni tanpa dependency tambahan).
3. **Escalate ke User**: Jika 3 jalur berbeda gagal, beritahu pengguna secara jujur beserta riwayat percobaannya.

---

## 📋 Tabel Aturan Perilaku Pengamanan

| Gejala Loop | Penyebab Umum | Tindakan Pengamanan (Guardrail) |
| :--- | :--- | :--- |
| Perintah `npm install` gagal terus | Masalah koneksi / versi Node | Batalkan instalasi, gunakan runtime default yang sudah ada. |
| Pengeditan file yang sama dibatalkan oleh linter | Format / syntax error berulang | Baca detail error linter dari bawah, perbaiki konfigurasi linter terlebih dahulu. |
| Tool `bash` mengembalikan timeout | Proses background macet | Jalankan `kill` pada process ID terkait sebelum mencoba kembali. |
| File `edit` gagal karena oldString not found | File berubah secara eksternal | Muat ulang isi file dengan `read` sebelum mencoba edit kembali. |

---

## 📞 Langkah Eskalasi ke Pengguna

Saat semua alternatif otomatis gagal, buat pesan eskalasi formal dengan struktur berikut:

```markdown
### 🔴 Eskalasi Sistem: Loop Terdeteksi & Gagal Dipulihkan

Saya mendeteksi kegagalan berulang pada tool: `bash` dengan command `npm run build`.

**Riwayat Percobaan:**
1. Percobaan 1: `npm run build` -> Error: `Cannot find module './dist/index'`
2. Percobaan 2: Menjalankan `npm run compile` terlebih dahulu -> Tetap gagal.
3. Percobaan 3: Menghapus `node_modules` dan menginstal ulang -> Error koneksi / registry.

**Rekomendasi Tindakan Manual:**
Silakan jalankan perintah instalasi di terminal lokal Anda terlebih dahulu, atau periksa versi Node Anda (butuh Node >= 18).
```

---

## ⚠️ Anti-Patterns Guardrails

* ❌ **Ignoring Failures**: Terus mengulang perintah yang sama tanpa menganalisis kode kesalahan (stderr) di setiap langkah.
* ❌ **Infinite Retries**: Menetapkan hitungan retry tanpa batas maksimum (maximum limit) pada fungsi eksekusi asinkronus.
* ❌ **Silent Failures**: Mengabaikan kemacetan proses dan membiarkan terminal menggantung (hang) tanpa timeout control.
