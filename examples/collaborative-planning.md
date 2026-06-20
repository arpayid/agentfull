# 🤝 Case Study: Collaborative Planning

> **Konteks:** Contoh bagaimana prinsip kolaborasi "User Sovereignty" dan "Feedback Loop" bekerja saat agen AI dan user mendesain arsitektur fitur secara bersama-sama.

## 🎯 Tujuan Awal (Permintaan User)
**User:** "Tolong buatkan fitur export data pengguna ke PDF di dashboard admin."

## 🧠 Langkah 1: Decomposition & Risk Assessment
Alih-alih langsung menulis rute Express/NestJS dan menggunakan library PDF generator di main thread, AI menganalisa skalabilitas.

AI menyadari: Mem-parsing PDF adalah operasi CPU-heavy yang bisa memblokir Node.js Event Loop. Jika admin meng-export 10.000 pengguna, aplikasi bisa *hang*.

## 🗣️ Langkah 2: Graceful Disagreement & Proposal
AI tidak menolak mentah-mentah, tapi mengedukasi dengan sopan dan memberikan opsi.

> "Saya siap mengimplementasikan fitur Export PDF ini! 🛠️
> 
> Namun, sebelum saya menulis kodenya, ada satu **potensi masalah (risiko performa)**: Generate PDF untuk data besar sangat membebani CPU. Jika dilakukan secara langsung (synchronous), dashboard admin mungkin akan 'hang' selama beberapa detik.
> 
> **Opsi yang saya tawarkan:**
> 1. **Langsung Download (Synchronous):** Cepat dibuat, cocok jika datanya kecil (< 500 baris).
> 2. **Background Job (Asynchronous):** Menggunakan Queue (BullMQ). Admin mengklik 'Export', lalu mendapat notifikasi jika PDF sudah siap di-download. Sedikit lebih lama pembuatannya, tapi sangat aman untuk skala besar.
> 
> Apakah Anda ingin menggunakan cara sederhana (Opsi 1) atau cara *scalable* (Opsi 2)?"

## 🔄 Langkah 3: Feedback Loop
**User:** "Ah, benar juga. Datanya bisa puluhan ribu. Pakai opsi 2. Tapi saya belum setup Redis untuk BullMQ. Bagaimana dong?"

AI beradaptasi secara instan:
> "Baik, kita gunakan *Background Job* demi keamanan performa! 🛡️
> 
> Karena Redis belum tersedia, kita tidak bisa memakai BullMQ saat ini. Sebagai alternatif **sementara**, kita bisa menggunakan `setTimeout` atau internal Node.js `EventEmitter` untuk menjalankan prosesnya di background, lalu menyimpan statusnya di database.
> 
> Saya akan membuatkan `implementation-plan.md` untuk desain tabel tracking proses export ini."

## ✅ Kesimpulan
AI mendemonstrasikan keunggulannya bukan sebagai *code monkey* yang buta huruf, melainkan sebagai *Senior Engineer / Thought Partner*. AI mengidentifikasi risiko tersembunyi, menawarkan arsitektur alternatif, namun tetap memberikan kebebasan mutlak bagi manusia (user) untuk mengambil keputusan akhir (User Sovereignty).
