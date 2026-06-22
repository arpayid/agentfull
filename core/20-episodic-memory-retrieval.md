# 🧠 20 — Episodic Memory Retrieval & Persistent State Sync

> *"Sebuah agen tidak boleh mengulang kesalahan yang sama hanya karena ia berada di sesi percakapan baru."*

---

## 📋 Daftar Isi

1. [Filosofi Memori Episodik](#-filosofi-memori-episodik)
2. [Arsitektur Sinkronisasi Memori](#-arsitektur-sinkronisasi-memori)
3. [Format Penyimpanan Ringkasan Episodik](#-format-penyimpanan-ringkasan-episodik)
4. [Mekanisme Retrieval Memori](#-mekanisme-retrieval-memori)

---

## 🎯 Filosofi Memori Episodik

Episodic Memory Retrieval adalah **sistem retensi informasi lintas sesi**. Saat sesi chat dimulai, agen secara dinamis mencari memori dari sesi sebelumnya terkait file konfigurasi, kegagalan compiler masa lalu, atau trade-off desain yang disepakati pengguna sebelumnya.

---

## 🏗️ Arsitektur Sinkronisasi Memori

```
Sesi Baru Dimulai ──► Ambil Konteks Sesi Terakhir ──► Embedding Match via Vector DB
                                                           │
                                                           ▼
                                               Suntikkan Temuan Penting 
                                               ke Immediate Context (Modul 06)
```

---

## 📝 Format Penyimpanan Ringkasan Episodik

Di akhir setiap sesi kerja, simpan file metadata memori terkompresi:

```json
{
  "session_id": "8bb63-agy",
  "knowledge_cutoff": "2026-06-22",
  "conventions_discovered": [
    "Project menggunakan space indentation (2 spaces)",
    "Linting ketat di typescript mewajibkan explicitly return types"
  ],
  "trapped_errors": [
    "Port 8080 dikunci oleh container docker lama, gunakan 8081"
  ]
}
```
