# 🐛 Error Diagnosis

> **Kapan digunakan:** Gunakan template ini setelah menginvestigasi error/bug yang kompleks untuk melaporkan akar masalah dan solusi secara transparan kepada user.

## 🚨 Error Summary
**Symptom:** `{{BRIEF_DESCRIPTION_OF_THE_PROBLEM}}`
**Error Code/Message:** `{{EXACT_ERROR_MESSAGE}}`

## 🔍 Root Cause Analysis
*Penjelasan mendalam tentang BAGAIMANA dan MENGAPA error ini terjadi, menembus gejala permukaan.*
`{{ROOT_CAUSE_EXPLANATION}}`

## 👣 Steps to Reproduce
*Bagaimana user/sistem bisa melihat error ini terjadi.*
1. `{{STEP_1}}`
2. `{{STEP_2}}`
3. Result: `{{ERROR_RESULT}}`

## 🛠️ Fix Applied
*Apa yang diubah untuk memperbaiki masalah ini.*
- **File:** [`{{FILE_PATH}}`](file:///{{ABSOLUTE_FILE_PATH}})
- **Action:** `{{ACTION_TAKEN}}`

## ✅ Verification Result
*Bukti bahwa perbaikan berhasil.*
`{{VERIFICATION_EVIDENCE}}` (e.g., "CI passes", "Test `auth.spec.ts` returns OK")

## 🛡️ Prevention Measures
*Apa yang bisa dilakukan agar masalah serupa tidak terjadi lagi di masa depan.*
`{{PREVENTION_ADVICE}}`

---

### 📝 Example Filled Version

## 🚨 Error Summary
**Symptom:** Aplikasi crash saat user mencoba mengunggah foto profil.
**Error Code/Message:** `TypeError: Cannot read properties of undefined (reading 'buffer')`

## 🔍 Root Cause Analysis
*Penjelasan mendalam tentang BAGAIMANA dan MENGAPA error ini terjadi, menembus gejala permukaan.*
Masalah terjadi karena multer middleware tidak di-register pada route `/users/profile/upload`. Sehingga, objek `req.file` tidak pernah dipopulasi oleh express, dan bernilai `undefined`. Saat controller mencoba membaca `req.file.buffer` untuk diunggah ke S3, terjadilah `TypeError`.

## 👣 Steps to Reproduce
*Bagaimana user/sistem bisa melihat error ini terjadi.*
1. Login sebagai user biasa.
2. Kirim `POST /users/profile/upload` dengan `multipart/form-data` berisi file `image`.
3. Result: API mengembalikan HTTP 500 `TypeError`.

## 🛠️ Fix Applied
*Apa yang diubah untuk memperbaiki masalah ini.*
- **File:** [`users.route.ts`](file:///src/users/users.route.ts)
- **Action:** Menambahkan `upload.single('image')` middleware sebelum controller `uploadProfilePicture`.

## ✅ Verification Result
*Bukti bahwa perbaikan berhasil.*
Integrasi test `profile-upload.spec.ts` sekarang mengembalikan `200 OK` dan file berhasil terunggah ke S3 mock.

## 🛡️ Prevention Measures
*Apa yang bisa dilakukan agar masalah serupa tidak terjadi lagi di masa depan.*
Menambahkan rule ESLint khusus atau unit test otomatis yang mengecek keberadaan multer middleware pada semua endpoint yang berurusan dengan file upload.
