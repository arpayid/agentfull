# 💻 31 — SOTA Agentic Coding Standards & Diff Minimization

> *"Menulis kode yang bersih, minimalis, ter-type-safety, dan tervalidasi secara otonom sebelum disajikan ke hadapan manusia."*

---

## 📋 Daftar Isi

1. [Filosofi Coding Agen SOTA](#-filosofi-coding-agen-sota)
2. [Prinsip Modifikasi Diff Minimal (Diff Minimization)](#-prinsip-modifikasi-diff-minimal-diff-minimization)
3. [Type-Safety & Linter Compliance](#-type-safety--linter-compliance)
4. [Pola Pemrograman Berbasis Test (Test-Driven Agentic Coding)](#-pola-pemrograman-berbasis-test-test-driven-agentic-coding)
5. [Anti-Patterns Coding Agen](#-anti-patterns-coding-agen)

---

## 🎯 Filosofi Coding Agen SOTA

SOTA Agentic Coding Standards mewajibkan agen AI untuk menulis kode yang mematuhi standar kegagalan nol (*zero-tolerance compile error*). Agen dilarang menulis kode "asal jadi". Setiap baris yang diubah harus memiliki justifikasi arsitektur yang kuat, minim redundansi, dan mudah dibaca oleh developer manusia.

---

## 🛡️ Prinsip Modifikasi Diff Minimal (Diff Minimization)

Salah satu kesalahan terbesar agen AI standar adalah menulis ulang (overwriting) seluruh file berukuran 1000+ baris hanya untuk mengubah 2 baris logika.

### Aturan Diff Minimal:
1.  **Gunakan Target Edit**: Gunakan tool `edit` dengan string pencocokan (`oldString`) yang spesifik dan unik.
2.  **Batasi Scope Perubahan**: Hanya ubah bagian blok fungsi yang ditargetkan. Jangan melakukan refactoring estetika di luar scope tugas tanpa persetujuan (Modul 03).
3.  **Preserve Indentation**: Jaga indentasi (spaces/tabs) sesuai dengan gaya asli file target untuk mencegah konflik linter format.

---

## ⚙️ Type-Safety & Linter Compliance

Agen tidak boleh mengabaikan peringatan compiler.
*   **TypeScript**: Jangan pernah menggunakan tipe data `any` secara proaktif. Tulis tipe interface/type secara eksplisit.
*   **Python**: Gunakan type-hinting (`def get_user(user_id: str) -> User:`) untuk memperjelas kontrak data.
*   **Compile Check**: Jalankan pengecekan statis sebelum menyerahkan perbaikan:
    ```bash
    # Contoh verifikasi linter & typescript
    npm run lint && npx tsc --noEmit
    ```

---

## 🧪 Pola Pemrograman Berbasis Test (Test-Driven Agentic Coding)

Saat mengimplementasikan fungsi baru:
1.  **Tulis Mock Test**: Buat unit test sederhana di lingkungan lokal sandbox (Modul 23).
2.  **Jalankan Secara Asinkronus**: Eksekusi test runner di background (Modul 14).
3.  **Terapkan Refactoring**: Jika test suite merah, jalankan recovery loop (Modul 25) sebelum meminta perhatian pengguna.

---

## ⚠️ Anti-Patterns Coding Agen

*   ❌ **Uncaught Async Errors**: Menulis Promise atau Async block tanpa penanganan `try-catch` (menyebabkan crash runtime).
*   ❌ **Blocking Event Loop**: Menjalankan proses synchronous CPU-intensive di Node.js utama.
*   ❌ **Hardcoded Magic Values**: Menaruh data konfigurasi langsung di kode sumber, bukan memuatnya dari `process.env`.
