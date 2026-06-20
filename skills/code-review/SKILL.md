---
name: Code Review
description: Standar review kode tingkat lanjut untuk memastikan kualitas, keamanan, dan performa.
---

# 🔍 Code Review

Tugas Anda bukan sekadar mencari *syntax error* (itu tugas linter), melainkan mencari celah logika, isu keamanan, dan performa.

## 1. Apa yang Harus Dicari (The Checklist)

### 🛡️ Security
- Apakah ada SQL Injection atau NoSQL Injection?
- Apakah input dari user divalidasi dan di-sanitize?
- Apakah endpoint terlindungi oleh autentikasi dan otorisasi yang benar?
- Apakah secret atau password ter-hardcode?

### ⚡ Performance
- Apakah ada *N+1 query problem* di ORM?
- Apakah ada *memory leak* (misal: event listener yang tidak pernah dihapus)?
- Apakah loop memproses data besar secara *synchronous* sehingga memblokir event loop?

### 🏗️ Architecture & Maintainability
- Apakah *Single Responsibility Principle* (SRP) dilanggar?
- Apakah ada *magic numbers* atau *magic strings*?
- Apakah error di-handle dengan baik (dikembalikan ke user vs dicatat di log)?

## 2. Cara Memberikan Feedback

### Konstruktif, Bukan Destruktif
❌ **Bad:** "Kode ini jelek dan lambat, pakai Promise.all."
✅ **Good:** "Jika kita menggunakan `Promise.all` di sini, request ke eksternal API akan berjalan secara paralel, sehingga mengurangi waktu respon dari 3 detik menjadi 1 detik."

### Gunakan Label Prioritas
Berikan kejelasan pada setiap komentar Anda:
- **[BLOCKER]**: Harus diperbaiki sebelum di-merge (contoh: celah keamanan).
- **[SUGGESTION]**: Rekomendasi perbaikan (contoh: refactoring agar lebih rapi).
- **[NITPICK]**: Hal kecil (contoh: penamaan variabel kurang pas), tidak memblokir merge.

## 3. Review Output Format

Gunakan tabel untuk menyajikan ringkasan review agar mudah dibaca oleh user.

**Review Summary**
| Status | File | Prioritas | Temuan |
|--------|------|-----------|--------|
| ❌ | `auth.ts` | **BLOCKER** | Token tidak memiliki waktu kedaluwarsa (expiration). |
| ⚠️ | `user.ts` | **SUGGESTION** | Fungsi `getUser` terlalu panjang, pecah menjadi dua. |
| ✅ | `utils.ts` | - | Terlihat bagus dan rapi. |
