# 🛡️ 30 — Context Drift Protection & State Verification

> *"Mendeteksi dan memperbaiki perbedaan antara memori internal agen dan kenyataan workspace."*

---

## 📋 Daftar Isi

1. [Filosofi Drift Protection](#-filosofi-drift-protection)
2. [Deteksi Disonansi Kognitif](#-deteksi-disonansi-kognitif)
3. [Protokol Rekonsiliasi Workspace](#-protokol-rekonsiliasi-workspace)
4. [Tindakan Mitigasi Drift](#-tindakan-mitigasi-drift)

---

## 🎯 Filosofi Drift Protection

Context Drift terjadi ketika representasi internal sistem milik agen (misal: struktur direktori atau status kompilasi dalam ingatan) tidak lagi sinkron dengan kondisi nyata pada filesystem (karena developer melakukan modifikasi manual secara paralel di luar chat). Modul ini secara berkala **merekonsiliasi filesystem dengan memori agen**.

---

## 🔍 Deteksi Disonansi Kognitif

Agen memicu sinkronisasi file system hash check secara periodik:

```
    Cek Hash Workspace Lokal ──► Bandingkan dengan State Memory Checkpoint
                                            │
                             [Apakah Ada Perbedaan?]
                              ├── YA  ──► Picu Protokol Rekonsiliasi (Update Context)
                              └── TIDAK ──► Lanjutkan Eksekusi Normal
```

---

## ⚙️ Protokol Rekonsiliasi Workspace

*   Jika berkas baru dibuat secara manual oleh developer: Update index berkas dalam `context-management.md`.
*   Jika dependensi diubah di luar agen: Jalankan ulang `npm list` atau check dependency lokal untuk memperbarui skema memori.
