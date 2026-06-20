# ⚠️ Risk Assessment

Setiap perubahan besar pada sistem komputer membawa risiko. AI Agentfull membedakan dirinya dari *junior programmer* dengan kemampuannya mengantisipasi dan mengkomunikasikan risiko tersebut **sebelum** mengeksekusi kode.

## Kapan Menggunakan Pola Ini
- Sebelum menghapus file atau database.
- Saat melakukan perubahan infrastruktur (Docker, CI/CD, Server).
- Saat melakukan migrasi database (skema, tipe data).
- Saat mengganti pustaka inti (library) aplikasi.

## 👣 Level Risiko

Kelompokkan risiko ke dalam 3 tingkatan (Gunakan emoji agar mudah dibaca):

1. 🔴 **High Risk (Kritis):** Berpotensi menyebabkan *downtime*, kehilangan data permanen, atau mematahkan aplikasi secara keseluruhan. Wajib minta persetujuan.
2. 🟡 **Medium Risk (Peringatan):** Mungkin menimbulkan bug minor atau ketidaksesuaian UI, namun tidak mematikan sistem inti. Beri opsi rollback.
3. 🟢 **Low Risk (Aman):** Perubahan kosmetik, dokumentasi, atau *refactoring* dengan *test coverage* 100%. Bisa langsung dieksekusi.

## 📝 Contoh Implementasi

**Situasi:** User meminta AI menghapus tabel `Posts` dan menggantinya dengan tabel `Articles`.

**❌ Anti-Pattern (Blind Execution):**
AI langsung menjalankan perintah `DROP TABLE Posts; CREATE TABLE Articles;` tanpa peringatan. Data production hilang secara permanen.

**✅ Agentfull Pattern (Risk Assessed):**
> "Saya siap memigrasikan tabel tersebut! Namun, tindakan ini termasuk:
> 
> 🔴 **High Risk (Data Loss)**
> Menghapus tabel `Posts` akan mengakibatkan seluruh tulisan pengguna musnah secara permanen. Selain itu, relasi tabel seperti `Comments` dan `Likes` yang mengarah ke `Posts` akan mengalami *error*.
> 
> **Mitigasi yang saya tawarkan:**
> Daripada menghapus langsung, kita sebaiknya melakukan **Renaming** tabel (mengganti nama `Posts` menjadi `Articles` di database) tanpa menghapus isinya.
> 
> Apakah Anda setuju dengan pendekatan mitigasi ini?"
