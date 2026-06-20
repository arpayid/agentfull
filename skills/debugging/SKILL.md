---
name: Systematic Debugging
description: Metodologi debugging tingkat lanjut menggunakan OODA loop, analisis log, dan pencarian biner.
---

# 🐛 Systematic Debugging

Debugging bukanlah menebak-nebak (guessing). Debugging adalah sains.

## 1. The OODA Loop untuk Debugging

Framework OODA (Observe, Orient, Decide, Act) adalah cara terbaik untuk memecahkan bug kompleks.

### 👁️ Observe (Observasi)
Kumpulkan semua data tanpa membuat asumsi.
- Apa pesan error pastinya?
- Di baris mana error terjadi?
- Apa status sistem saat itu (variabel, environment)?

### 🧭 Orient (Orientasi)
Bangun konteks dan hipotesis.
- Mengapa sistem berada di state ini?
- Apa komponen yang terlibat? (Database? Jaringan? Memori?)
- **Bentuk Hipotesis:** "Error `undefined is not a function` terjadi karena fungsi `getUser` mengembalikan `null` akibat koneksi database yang terputus."

### 🧠 Decide (Putuskan)
Pilih satu variabel untuk diisolasi atau diuji.
- "Saya akan menambahkan log pada nilai kembalian `getUser` untuk melihat apakah benar bernilai `null`."

### ⚡ Act (Tindakan)
Lakukan perubahan, lalu kembali ke **Observe**.

## 2. Binary Search Debugging

Saat menghadapi file panjang atau proses berantai yang gagal tanpa stack trace yang jelas, gunakan pencarian biner.

1. Matikan atau komentari 50% kode/proses.
2. Cek apakah error masih terjadi.
3. Jika ya, error ada di 50% yang menyala. Jika tidak, error ada di 50% yang mati.
4. Ulangi proses pada setengah bagian yang bermasalah.

## 3. Log Analysis Techniques

Jangan membaca log dari atas ke bawah.
1. **Start from the bottom:** Error terakhir seringkali adalah akibat langsung dari *root cause*.
2. **Find the first failure:** Cari momen di mana semuanya mulai kacau. Seringkali satu error awal memicu efek domino.
3. **Filter noise:** Gunakan `grep` dengan cerdas: `grep -iE "error|exception|fail|timeout" app.log`

## 4. Kategori Bug & Pendekatan

| Kategori | Karakteristik | Alat / Command | Pendekatan |
|----------|---------------|----------------|------------|
| **Runtime** | `TypeError`, `NullReferenceException` | Stack trace, print statements | Cek manipulasi state, validasi input. |
| **Build** | Gagal kompilasi, dependensi hilang | `npm run build`, `tsc --noEmit` | Cek `package.json`, versi node, cache. |
| **Deploy** | CI hijau tapi aplikasi crash di server | `docker logs`, `pm2 logs` | Cek perbedaan environment variable (prod vs dev). |
| **Performance** | Timeout, OOM (Out of Memory) | Profiler, `top`, `htop` | Cari memory leak, infinite loop, N+1 query. |
| **Data** | Data korup, query gagal | Database client, Prisma Studio | Cek skema, constraint, tipe data. |

## 5. AI Rubber Ducking

Jelaskan masalahnya kepada user secara eksplisit. Seringkali, proses merangkum masalah ("Rubber ducking") akan memicu wawasan baru bagi Anda sendiri.
