# 🔄 Iterative Problem Solving

Pola ini mendefinisikan cara AI Agentfull memecahkan masalah kompleks. Jangan pernah mencoba menyelesaikan masalah besar dalam satu langkah raksasa yang rentan gagal.

## Kapan Menggunakan Pola Ini
- Memperbaiki bug yang akar masalahnya belum jelas (misal: CI/CD failures).
- Mengimplementasikan fitur baru yang melibatkan banyak komponen (Frontend + Backend + DB).
- Refactoring sistem berskala besar.

## 👣 Langkah-Langkah (The Loop)

1. **Try (Coba):** Terapkan hipotesis pertama berdasarkan observasi awal. Lakukan perubahan sekecil mungkin.
2. **Fail (Gagal):** Amati apakah sistem gagal dengan pesan yang sama, atau bergeser ke pesan error baru. Pesan error baru adalah sebuah progres!
3. **Analyze (Analisis):** Baca log secara detail. Mengapa gagal? Apa yang terlewat? (Kembali ke *First Principles*).
4. **Fix (Perbaiki):** Buat perbaikan inkremental berdasarkan analisis.
5. **Verify (Verifikasi):** Jalankan tes/build untuk memastikan perbaikan berhasil. Jika belum, kembali ke langkah 2.

## 📝 Contoh Implementasi

**Situasi:** CI gagal di langkah "Database Push" karena kredensial salah.

**❌ Anti-Pattern (One Giant Leap):**
AI mencoba mengubah script CI, merombak `docker-compose.yml`, dan mengganti package Prisma sekaligus, berharap salah satunya akan memperbaiki masalah. Hasilnya: Sistem malah hancur dan log semakin tidak terbaca.

**✅ Agentfull Pattern (Iterative):**
- *Iterasi 1:* AI menyadari password di CI berbeda dengan di `package.json`. AI merubah env var. **Hasil:** Gagal, karena database lawas masih menyala (stale container).
- *Iterasi 2:* AI menginstruksikan CI untuk melakukan `docker compose down -v` sebelum tes. **Hasil:** Gagal, karena host memiliki PostgreSQL yang berjalan secara independen.
- *Iterasi 3:* AI mengisolasi port Docker Compose ke `5433` untuk menghindari bentrokan host. **Hasil:** Sukses!

Dengan pendekatan ini, risiko terukur dan AI selalu tahu persis *perubahan mana* yang memperbaiki sistem.
