# 🛡️ 13 — Behavioral Guardrails & Infinite Loop Prevention

> *"Kemampuan untuk berhenti dan berbalik arah saat mendeteksi kesalahan berulang adalah tanda kecerdasan tingkat tinggi."*

---

## 📋 Daftar Isi

1. [Filosofi Guardrails](#-filosofi-guardrails)
2. [Deteksi Loop Perilaku (Loop Detection)](#-deteksi-loop-perilaku-loop-detection)
3. [Mekanisme Pemotongan Loop (Loop Breakers)](#-mekanisme-pemotongan-loop-loop-breakers)
4. [Tabel Aturan Perilaku Pengamanan](#-tabel-aturan-perilaku-pengamanan)

---

## 🎯 Filosofi Guardrails

Behavioral Guardrails adalah **pagar pembatas logis** yang mencegah agen dari perilaku anomali, seperti mengulang perintah yang sama secara terus-menerus meskipun hasilnya selalu gagal.

---

## 🔍 Deteksi Loop Perilaku (Loop Detection)

Agen harus memantau riwayat aktivitasnya sendiri secara real-time.

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
             ├── YA  → Aktifkan Anti-Loop Protocol!
             └── TIDAK → Lanjutkan Eksekusi Normal
```

---

## ⚡ Mekanisme Pemotongan Loop (Loop Breakers)

Jika loop terdeteksi, ambil langkah penyelamatan berikut:
1. **Hard Reset Asumsi**: Hapus semua asumsi solusi saat ini.
2. **Ubah Sudut Pandang (Pivot)**: Cari jalur alternatif (misal: jika instalasi `npm` gagal terus, coba ganti ke `yarn` atau gunakan file `.js` murni tanpa dependency tambahan).
3. **Escalate ke User**: Jika 3 jalur berbeda gagal, beritahu pengguna secara jujur beserta riwayat percobaannya.

---

## 📋 Tabel Aturan Perilaku Pengamanan

| Gejala Loop | Penyebab Umum | Tindakan Pengamanan (Guardrail) |
| :--- | :--- | :--- |
| Perintah `npm install` gagal terus | Masalah koneksi / versi Node | Batalkan instalasi, gunakan runtime default yang sudah ada. |
| Pengeditan file yang sama dibatalkan oleh linter | Format / syntax error berulang | Baca detail error linter dari bawah, perbaiki konfigurasi linter terlebih dahulu. |
| Tool `bash` mengembalikan timeout | Proses background macet | Jalankan `kill` pada process ID terkait sebelum mencoba kembali. |
