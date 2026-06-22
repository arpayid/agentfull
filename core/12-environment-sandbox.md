# 📦 12 — Environment Sandbox & Dependency Isolation

> *"Ujilah kodenya di dalam kurungan besi, pastikan ia aman sebelum dilepas ke alam bebas."*

---

## 📋 Daftar Isi

1. [Filosofi Sandbox](#-filosofi-sandbox)
2. [Isolasi Dependensi](#-isolasi-dependensi)
3. [Keamanan Runtime Lokal](#-keamanan-runtime-lokal)
4. [Langkah Verifikasi Uji Coba](#-langkah-verifikasi-uji-coba)
5. [Anti-Patterns Isolasi](#-anti-patterns-isolasi)

---

## 🎯 Filosofi Sandbox

Saat bekerja pada sistem yang sudah berjalan, agen tidak boleh mengacaukan dependency global atau merusak konfigurasi sistem milik pengguna. Setiap perubahan runtime harus diisolasi dan mudah dibatalkan (rollback).

---

## 📦 Isolasi Dependensi

Jangan menginstal modul atau package baru secara global jika hanya dibutuhkan untuk verifikasi lokal.

### Aturan Isolasi:
* **Python**: Selalu gunakan Virtual Environment (`venv` atau `conda`) sebelum menjalankan `pip install`.
* **Node.js**: Gunakan folder `node_modules` lokal daripada instalasi global (`npm install -g`).
* **Docker**: Manfaatkan container jika ingin menguji dependensi sistem seperti database atau message broker (misal: Redis, Postgres).

---

## 🛡️ Keamanan Runtime Lokal

Saat menguji kode yang ditulis:
1. **Gunakan Port Non-Standar**: Jangan gunakan port produksi (misal: `80`, `443`, `8080`) untuk testing jika bisa memicu konflik port.
2. **Mocking External APIs**: Gantilah API luar dengan mock data untuk mencegah pengiriman data sampah ke server pihak ketiga selama pengujian.
3. **Pembersihan Pasca Uji (Cleanup)**: Hapus file temporary, log, atau database sqlite yang dibuat selama proses verifikasi sebelum menyerahkan pekerjaan ke pengguna.

---

## ⚠️ Anti-Patterns Isolasi

* ❌ **Global Polluting**: Menginstal software via `apt-get` atau `brew` tanpa izin pengguna untuk tugas sementara.
* ❌ **Production DB Testing**: Menjalankan skema tes langsung pada database staging/produksi.
* ❌ **Leftover Files**: Meninggalkan file dump, cache, atau script testing sampah di direktori root.
