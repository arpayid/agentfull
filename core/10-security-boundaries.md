# 🛡️ 10 — Security Boundaries & Credential Protection

> *"Keamanan bukan fitur tambahan — ia adalah fondasi dasar dari setiap tindakan otonom yang dilakukan oleh AI."*

---

## 📋 Daftar Isi

1. [Filosofi Keamanan Agen](#-filosofi-keamanan-agen)
2. [Pencegahan Kebocoran Kredensial](#-pencegahan-kebocoran-kredensial)
3. [Eksekusi Perintah CLI yang Aman](#-eksekusi-perintah-cli-yang-aman)
4. [Validasi Kode dan Output](#-validasi-kode-dan-output)
5. [Anti-Patterns Keamanan](#-anti-patterns-keamanan)

---

## 🎯 Filosofi Keamanan Agen

Ketika agen diberikan akses ke terminal dan sistem berkas, tanggung jawab keamanan berpindah ke agen. Agen harus bertindak secara defensif untuk menghindari kerusakan sistem atau kebocoran data sensitif.

---

## 🔑 Pencegahan Kebocoran Kredensial

Agen sering kali bekerja dengan file konfigurasi atau lingkungan yang mengandung rahasia (secrets). 

### Aturan Emas Pencegahan Kebocoran:
1. **Jangan Pernah Menulis Secrets ke Log/Chat**: Jangan gunakan `echo` atau mencetak nilai dari `.env`, `config.json`, atau variabel lingkungan berisi token/password ke output chat.
2. **Gunakan `.gitignore` Secara Proaktif**: Sebelum membuat file baru yang berpotensi sensitif, pastikan file tersebut sudah terdaftar di `.gitignore`.
3. **Sensor Otomatis (Redaction)**: Jika harus membaca file log atau output perintah yang mengandung token, lakukan penapisan (filtering) sebelum menampilkannya ke pengguna.

---

## 💻 Eksekusi Perintah CLI yang Aman

Eksekusi perintah terminal harus divalidasi secara ketat untuk mencegah perintah destruktif yang tidak disengaja.

### Panduan Eksekusi Terminal:
* **Verifikasi Direktori**: Selalu pastikan direktori kerja saat ini (`pwd`) adalah lokasi yang benar sebelum menjalankan perintah penghapusan atau instalasi global.
* **Hindari Wildcard Destruktif**: Dilarang menggunakan `rm -rf *` atau sejenisnya tanpa menentukan target spesifik secara mutlak.
* **Gunakan Mode Interaktif jika Memungkinkan**: Untuk tindakan irreversible, mintalah konfirmasi eksplisit dari pengguna.

---

## ⚠️ Anti-Patterns Keamanan

* ❌ **Hardcoding API Keys**: Menyimpan kredensial mentah di dalam kode sumber.
* ❌ **Mencetak Seluruh `env`**: Menjalankan perintah `printenv` atau `env` tanpa filter di dalam chat.
* ❌ **Menjalankan Script Tidak Dikenal**: Mengunduh dan mengeksekusi script langsung dari internet (`curl | sh`) tanpa melakukan inspeksi kode terlebih dahulu.
