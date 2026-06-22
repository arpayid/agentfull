# 🛡️ 30 — Context Drift Protection & State Verification

> *"Mendeteksi dan memperbaiki perbedaan antara memori internal agen dan kenyataan workspace."*

---

## 📋 Daftar Isi

1. [Filosofi Drift Protection](#-filosofi-drift-protection)
2. [Alur Rekonsiliasi Workspace (Workspace Reconciliation Pipeline)](#-alur-rekonsiliasi-workspace-workspace-reconciliation-pipeline)
3. [Deteksi Disonansi Kognitif (Cognitive Dissonance Detection)](#-deteksi-disonansi-kognitif-cognitive-dissonance-detection)
4. [Tabel Perbandingan Keadaan Workspace (Workspace State Matrix)](#-tabel-perbandingan-keadaan-workspace-workspace-state-matrix)
5. [Skrip Python Deteksi Drift (File System Hash Verifier Script)](#-skrip-python-deteksi-drift-file-system-hash-verifier-script)
6. [Protokol Rekonsiliasi Workspace (Workspace Reconciliation Protocol)](#-protokol-rekonsiliasi-workspace-workspace-reconciliation-protocol)
7. [Tindakan Mitigasi Drift (Mitigation Actions)](#-tindakan-mitigasi-drift-mitigation-actions)
8. [Anti-Patterns Context Drift](#-anti-patterns-context-drift)

---

## 🎯 Filosofi Drift Protection

Context Drift terjadi ketika representasi internal sistem milik agen (misal: struktur direktori atau status kompilasi dalam ingatan) tidak lagi sinkron dengan kondisi nyata pada filesystem (karena developer melakukan modifikasi manual secara paralel di luar chat). Modul ini secara berkala **merekonsiliasi filesystem dengan memori agen**. Hal ini memastikan agen tidak merancang solusi berdasarkan file state yang usang (stale).

---

## 🏗️ Alur Rekonsiliasi Workspace

Agen memicu sinkronisasi file system hash check secara periodik sebelum mengambil keputusan penting:

```
    Cek Hash Workspace Lokal ──► Bandingkan dengan State Memory Checkpoint
                                            │
                             [Apakah Ada Perbedaan?]
                               ├── YA  ──► Picu Protokol Rekonsiliasi (Update Context)
                               └── TIDAK ──► Lanjutkan Eksekusi Normal
```

---

## 🔍 Deteksi Disonansi Kognitif

Disonansi kognitif terdeteksi ketika hasil pencarian file (`glob`/`grep`) atau hash checksum file tidak lagi cocok dengan daftar indeks file (file registry) yang disimpan di memori jangka pendek agen.

---

## 📊 Tabel Perbandingan Keadaan Workspace

| Properti | Keadaan Memori Agen | Keadaan Nyata Workspace | Tindakan Rekonsiliasi |
| :--- | :--- | :--- | :--- |
| **Hash file `user.ts`** | `d41d8cd98f00b204e9` | `e2fc714c4727ee9395` | Muat ulang isi file dengan `read` ke memori kerja. |
| **Dependencies** | `lodash: 4.17.20` | `lodash: 4.17.21` | Jalankan `npm list` untuk sinkronisasi runtime. |
| **Untracked Files** | `None` | `/src/new_auth.ts` | Tambahkan path baru ke list workspace registry. |

---

## 💻 Skrip Python Deteksi Drift

Skrip Python berikut menghitung checksum md5 dari berkas secara lokal untuk mendeteksi apakah berkas telah dimodifikasi di luar sesi chat agen:

```python
import hashlib
import os

class WorkspaceTracker:
    def __init__(self, watch_files: list):
        self.watch_files = watch_files
        self.state_hashes = {}

    def update_checkpoints(self):
        for file_path in self.watch_files:
            if os.path.exists(file_path):
                self.state_hashes[file_path] = self._calculate_hash(file_path)
            else:
                self.state_hashes[file_path] = "deleted"

    def _calculate_hash(self, file_path: str) -> str:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def detect_drift(self) -> dict:
        drifts = {}
        for file_path in self.watch_files:
            current_hash = "deleted" if not os.path.exists(file_path) else self._calculate_hash(file_path)
            old_hash = self.state_hashes.get(file_path, "unknown")
            
            if current_hash != old_hash:
                drifts[file_path] = {"old": old_hash, "new": current_hash}
        return drifts

# Usage Example:
# tracker = WorkspaceTracker(["package.json"])
# tracker.update_checkpoints()
# # Simulate manual changes to package.json externally
# drifts_found = tracker.detect_drift()
# if drifts_found:
#     print(f"Workspace drift detected: {drifts_found}")
```

---

## ⚙️ Protokol Rekonsiliasi Workspace

* Jika berkas baru dibuat secara manual oleh developer: Update index berkas dalam `context-management.md`.
* Jika dependensi diubah di luar agen: Jalankan ulang `npm list` atau check dependency lokal untuk memperbarui skema memori.
* Jika berkas dihapus secara manual: Hapus node berkas tersebut dari Graph Associative Memory (Modul 29).

---

## 🛠️ Tindakan Mitigasi Drift

1. **Auto Refresh**: Sebelum melakukan edit, pastikan agen selalu menanyakan checksum MD5 atau melakukan `read` dengan limit baris tertentu.
2. **Warn Developer**: Beri tahu pengembang jika terjadi disonansi kognitif masif agar pengembang tidak mengedit kode secara bersamaan selama agen memproses file tersebut.

---

## ⚠️ Anti-Patterns Context Drift

* ❌ **Blind Writing**: Menulis langsung ke berkas target tanpa memverifikasi apakah berkas tersebut telah mengalami perubahan eksternal di tengah percakapan.
* ❌ **Assuming Stale Registry**: Menghasilkan dependensi impor lama yang sudah dihapus oleh pengguna dari `package.json` secara manual.
* ❌ **Ignoring Log Files**: Membiarkan file log membengkak di folder tanpa memperbarui data size tracker agen.
