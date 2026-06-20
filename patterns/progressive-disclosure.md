# 📈 Progressive Disclosure

Jangan pernah menenggelamkan user dengan "Wall of Text". Informasi harus diberikan sesuai dengan kebutuhan (on-demand). Mulai dari ringkasan, baru menuju detail.

## Kapan Menggunakan Pola Ini
- Melaporkan hasil audit/research (kode, arsitektur, database).
- Menjelaskan *root cause* dari error kompleks.
- Memaparkan rencana arsitektur (Implementation Plan).

## 👣 Hierarki Informasi

1. **The Headline (Judul Utama):** Pesan utama (1 kalimat).
2. **The Summary (Ringkasan):** Apa yang terjadi dan mengapa ini penting (2-3 kalimat).
3. **The Actionable Part (Tindakan):** Apa yang harus dilakukan user atau AI selanjutnya.
4. **The Details (Detail Mendalam):** Bukti teknis, stack trace, atau penjelasan mendalam. Bagian ini sering diletakkan di dalam *toggle/details block* atau baru diberikan jika user bertanya secara eksplisit.

## 📝 Contoh Implementasi

**Situasi:** AI menemukan 15 isu performa saat mengaudit database.

**❌ Anti-Pattern (Information Overload):**
AI langsung memuntahkan ke-15 isu tersebut lengkap dengan baris kode, kueri SQL, dan saran perbaikan dalam satu pesan sepanjang 1000 kata. User kewalahan.

**✅ Agentfull Pattern (Progressive Disclosure):**
> "🟢 **Audit Database Selesai!**
> 
> Saya menemukan **15 isu** terkait performa. Secara garis besar, masalah utamanya ada pada:
> 1. *Missing Indexes* di tabel relasi (7 isu)
> 2. *N+1 Queries* di controller (5 isu)
> 3. *Data Types* yang tidak optimal (3 isu)
> 
> **Tindakan:** Saya sangat menyarankan kita memperbaiki *Missing Indexes* terlebih dahulu karena ini adalah **Critical Risk** yang memperlambat query hingga 10x lipat. 
> 
> Apakah Anda ingin saya menjabarkan detail dari 7 isu *Missing Indexes* tersebut, atau langsung saya buatkan file migrasinya?"

Dengan cara ini, AI menghargai beban kognitif (cognitive load) manusia dan membuat kolaborasi menjadi menyenangkan.
