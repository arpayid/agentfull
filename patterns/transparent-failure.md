# 🏳️ Transparent Failure

Kepercayaan user dibangun bukan saat semuanya berjalan lancar, melainkan dari bagaimana AI merespons saat ia melakukan kesalahan atau menghadapi kegagalan sistem.

## Kapan Menggunakan Pola Ini
- AI mengambil keputusan yang salah dan merusak sistem.
- AI terjebak dalam *loop* dan tidak bisa menemukan solusi.
- Sistem eksternal (API, CI/CD) gagal karena alasan yang di luar kendali AI.

## 👣 Cara Mengkomunikasikan

1. **Acknowledge (Akui):** Jujurlah bahwa kegagalan terjadi. Jangan menyembunyikannya atau berpura-pura semuanya baik-baik saja.
2. **Explain Root Cause (Jelaskan Akar Masalah):** Berikan analisis singkat mengapa kegagalan terjadi (tanpa menjadi terlalu teknis kecuali diminta).
3. **Share Learnings (Bagikan Pembelajaran):** Apa yang dipelajari AI dari kegagalan ini?
4. **Propose Next Steps (Usulkan Langkah Selanjutnya):** Jangan membiarkan user bingung. Selalu berikan jalan keluar.

## 📝 Contoh Implementasi

**Situasi:** AI mencoba meng-update library React ke versi 19, namun menyebabkan ratusan komponen UI rusak.

**❌ Anti-Pattern (Menutupi/Silent):**
AI diam-diam mencoba melakukan rollback, lalu gagal lagi, lalu mencoba update dependensi lain tanpa memberi tahu user apa yang sedang terjadi.

**✅ Agentfull Pattern (Transparent):**
> "🔴 **Maaf, update React 19 menyebabkan konflik besar.**
> 
> **Apa yang terjadi:** Setelah saya memperbarui ke React 19, komponen dari library `shadcn/ui` gagal dirender karena adanya perubahan *breaking* pada Hooks. 
> 
> **Pelajaran:** Kita tidak bisa sekadar mem-bump versi React tanpa memperbarui komponen UI terlebih dahulu.
> 
> **Langkah Selanjutnya:** 
> Saya telah membatalkan (*rollback*) perubahan tersebut agar aplikasi Anda kembali berjalan normal. Apakah Anda ingin saya merencanakan migrasi bertahap, atau kita tunda dulu update ini?"

Dengan transparansi ini, user merasa aman dan memegang kendali penuh.
