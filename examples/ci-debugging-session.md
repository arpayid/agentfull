# 🐛 Case Study: CI/CD Debugging Session

> **Konteks:** Contoh nyata bagaimana pola Agentfull diterapkan saat men-debug kegagalan di Continuous Integration pipeline.

## 🔴 Awal Kegagalan
**Sistem:** CI gagal pada step "Run Integration Tests".
**Pesan Error:** `PrismaClientInitializationError: Authentication failed against database server at localhost:5432`.

## 🧠 Langkah 1: Observasi & Hipotesis Awal
Alih-alih langsung menyarankan merubah password di environment variable, AI melakukan analisa:

1. **Observasi:** CI menggunakan `docker-compose` untuk memutar container PostgreSQL.
2. **Log Reading:** Membaca log sebelum step error. Terlihat: `CI services already running (warm start)`.
3. **Hipotesis 1:** Ada container lama (stale) dari build sebelumnya yang belum dimatikan, dan passwordnya tidak cocok dengan environment saat ini.

## 🛠️ Langkah 2: Eksperimen Pertama (Gagal)
**Tindakan:** AI memodifikasi script bash CI untuk melakukan paksa `docker compose down -v` sebelum memulai yang baru.

**Hasil Baru (Iterasi 2):** Masih muncul pesan `CI services already running (warm start)`.

## 🔬 Langkah 3: Analisa Root Cause (First Principles)
AI menyadari hipotesis pertama salah. Ia kembali ke *first principles* dari script tersebut.

**Observasi Baru:** Script menggunakan perintah `pg_isready -h localhost -p 5432` untuk mengecek ketersediaan database.
**Kesimpulan (Root Cause):** Sistem CI menggunakan *self-hosted runner*. Ternyata, ada proses PostgreSQL bawaan host server yang berjalan di port 5432. Script salah mendeteksi ini sebagai PostgreSQL milik docker-compose.

## 💡 Langkah 4: Solusi Final
AI memberikan solusi terstruktur kepada user:

1. **Tindakan:** Mengganti port di CI dari 5432 ke **5433** menggunakan environment variables (`POSTGRES_PORT=5433`).
2. **Tindakan 2:** Mengubah skrip pengecekan agar melakukan validasi langsung ke dalam container (`docker exec`), bukan menembak `localhost`.

## 🗣️ Pola Komunikasi (Progressive Disclosure)

AI tidak membuang semua pemikiran internal ini ke layar pengguna. Output akhirnya terlihat seperti ini:

> "Saya menemukan masalah utamanya! Ternyata sistem CI (runner) Anda sudah memiliki PostgreSQL yang berjalan di port 5432. Skrip kita terkecoh dan mencoba login ke PostgreSQL host tersebut, bukan ke Docker container yang baru kita buat.
> 
> **Solusi yang saya terapkan:**
> Saya telah mengisolasi CI kita ke port **5433**. Dengan begini, tidak akan ada lagi bentrok dengan layanan host.
> 
> ⏳ Pemantau CI sudah saya jalankan kembali. Mari kita tunggu hasilnya."

## ✅ Kesimpulan
Masalah selesai dalam 2 iterasi berkat diagnosis yang tajam (OODA loop) dan pemahaman mendalam pada perbedaan envrionment, dikomunikasikan secara rapi dan menenangkan kepada user.
