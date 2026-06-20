# 🏗️ Case Study: Infrastructure Migration

> **Konteks:** Contoh bagaimana AI mengambil keputusan terstruktur dan menerapkan manajemen risiko saat melakukan migrasi sistem berskala besar.

## 🎯 Tujuan
User ingin memigrasikan penyimpanan gambar dari sistem lokal (Local File System) ke cloud storage (AWS S3) tanpa mengganggu layanan aplikasi yang sedang berjalan.

## 🧠 Langkah 1: Planning Mode
Karena ini adalah perubahan arsitektur (high risk), AI otomatis mengaktifkan "Planning Mode" dan tidak langsung menulis kode. AI menyusun `implementation-plan.md` dan menunjukkannya kepada user.

## ⚖️ Langkah 2: Decision Making & Trade-offs
Dalam rencananya, AI memberikan beberapa pilihan strategi beserta trade-off-nya:

| Strategi | Kelebihan | Kekurangan | Rekomendasi |
|----------|-----------|------------|-------------|
| **Downtime Migration** | Mudah, tidak ada risiko data inkonsisten | Aplikasi mati 2-4 jam | ❌ |
| **Dual-Write (Live)** | Zero downtime, aman | Kode lebih kompleks | ✅ **Disarankan** |

## 🛡️ Langkah 3: Risk Assessment
AI juga menyertakan mitigasi risiko:
- **Risiko:** Aplikasi lama mencari file di lokal, padahal sudah dihapus.
- **Mitigasi:** Migrasi akan dilakukan bertahap (Dual-Write). Selama masa transisi, kode akan mengecek S3 terlebih dahulu, jika gagal (fallback) baca dari lokal.

## 🤝 Langkah 4: Collaboration (Eksekusi)
Setelah user menyetujui "Dual-Write strategy", AI mengeksekusi dengan *incremental fixes*:

1. **Iterasi 1:** Menambah AWS SDK dan membuat service S3 (Upload hanya sebagai background task).
2. **Iterasi 2:** Memodifikasi endpoint upload agar menulis ke lokal DAN ke S3.
3. **Iterasi 3:** Membuat script sinkronisasi (backfill) file lama ke S3.
4. **Iterasi 4:** Membalik logika pembacaan: baca S3, fallback ke lokal.

Pada setiap iterasi, AI memberikan **Progress Report** agar user tidak merasa ditinggalkan saat proses panjang berlangsung.

## 🗣️ Pola Komunikasi

Contoh interaksi AI dengan user di pertengahan proses:

> "🟢 **Status:** Iterasi 2 selesai. Dual-write sudah aktif. 
> 
> **Penemuan:** Saat saya mencoba menulis ke S3, region yang dikonfigurasi di `.env` adalah `us-east-1`, sedangkan bucket Anda ada di `ap-southeast-1`. Saya mendapat error `301 Moved Permanently`.
> 
> **Tindakan:** Saya telah menyesuaikan konfigurasi region di kode agar sesuai dengan bucket Anda.
> 
> ⏳ **Selanjutnya:** Memulai proses sinkronisasi 10.000 file lama. Proses ini memakan waktu sekitar 15 menit. Anda ingin saya berjalan di *background*, atau Anda ingin memantau lognya bersama saya?"
