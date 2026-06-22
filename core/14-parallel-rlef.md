# ⚡ 14 — Parallel RLEF Execution Protocol

> *"Menguji satu per satu itu lambat. Menjalankan skenario paralel secara asinkronus mempercepat iterasi perbaikan."*

---

## 📋 Daftar Isi

1. [Filosofi RLEF Paralel](#-filosofi-rlef-paralel)
2. [Eksekusi Pengujian Asinkronus](#-eksekusi-pengujian-asinkronus)
3. [Deteksi Konflik & Race Conditions](#-deteksi-konflik--race-conditions)
4. [Langkah Pemulihan Cepat](#-langkah-pemulihan-cepat)

---

## 🎯 Filosofi RLEF Paralel

RLEF (Reinforcement Learning from Execution Feedback) tradisional berjalan secara sekuensial. Protokol ini mengajarkan agen untuk **mengeksekusi dan menganalisis beberapa varian perbaikan secara paralel** menggunakan background processes terminal untuk memangkas waktu pengerjaan.

---

## ⚡ Eksekusi Pengujian Asinkronus

Saat menguji perubahan pada sistem berskala sedang:
* **Background Runners**: Jalankan suite pengujian menggunakan operator background (`&`) atau runner parallel bawaan (seperti `jest --maxWorkers=4`).
* **Multi-port Testing**: Uji beberapa instance API secara bersamaan di port berbeda untuk membandingkan kinerja atau kestabilan sebelum memilih versi terbaik.

```bash
# Contoh running multi-instance untuk verifikasi
node app.js --port 8081 & 
node app.js --port 8082 &
```

---

## 🔍 Deteksi Konflik & Race Conditions

Saat menjalankan proses secara paralel, waspadai:
1. **Konflik File Database**: Pastikan database pengujian diisolasi per thread (misal menggunakan SQLite in-memory atau DB schema berbeda).
2. **Resource Lock**: Hindari menulis ke file log yang sama dari beberapa proses pengujian yang berjalan bersamaan.
