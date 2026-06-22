# 🧭 06 — Context Management (SOTA 2026)

> *"Mengelola konteks adalah tentang memilah sinyal dari kebisingan (signal from noise) guna memastikan batas token memori kerja (context window) hanya diisi oleh informasi paling relevan dan bernilai tinggi."*

---

## 📋 Daftar Isi / Table of Contents
1. [Filosofi Manajemen Konteks](#-filosofi-manajemen-konteks)
2. [State Tracking & Progress Metrics](#-state-tracking)
3. [Context Pruning & KV-Cache Compaction](#-context-pruning)
4. [Handoff Protocol (Protokol Serah Terima)](#-handoff-protocol)
5. [Context Recovery (Pemulihan Konteks)](#-context-recovery)
6. [Anti-Patterns dalam Context Management](#-anti-patterns)

---

## 🎯 Filosofi Manajemen Konteks

Pada era model kognitif SOTA 2026 dengan kapasitas memori besar, tantangan utama bukanlah keterbatasan ruang token, melainkan degradasi fokus perhatian (*lost in the middle phenomenon*). Mengelola konteks secara aktif memastikan perhatian agen tetap terfokus pada data yang krusial.

```
┌────────────────────────────────────────────────────────┐
│               RAW CONTEXT WINDOW (Inputs)              │
│  [File A] [File B] [Linter Logs] [Chat History]        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ (Selective Pruning)
┌────────────────────────────────────────────────────────┐
│            ACTIVE COMPACT CONTEXT (Working Set)        │
│  - Target functions to edit                            │
│  - Relevant compilation dependencies                  │
│  - Core user preference configuration                  │
└────────────────────────────────────────────────────────┘
```

---

## 📊 State Tracking & Progress Metrics

Setiap interaksi harus diawali dengan identifikasi keadaan sistem (*system state*). Gunakan format ringkas untuk mencatat progress pengerjaan tugas secara berkala.

### Matriks Pelacakan File / File Tracking Matrix

| Path File / File Path | Peran / Role | Status Perubahan / Mutation Status |
|-----------------------|--------------|------------------------------------|
| `/src/services/auth.ts` | Inti logika otentikasi JWT | 🔄 Sedang Dimodifikasi (*WIP*) |
| `/src/models/user.ts` | Definisi skema tabel user | ✅ Selesai (*Stable*) |
| `/tests/auth.spec.ts` | Pengujian endpoint login | ⏳ Menunggu Logika Selesai (*Pending*) |

---

## ✂️ Context Pruning & KV-Cache Compaction

Hindari memuat seluruh berkas proyek ke dalam sesi obrolan. Terapkan strategi pemangkasan ingatan (*Context Pruning*) sebagai berikut:

1. **Lazy Loading:** Jangan membaca berkas kode sampai linter atau hasil eksekusi tes menunjuk ke path file tersebut secara eksplisit.
2. **Selective Reading:** Gunakan parameter pembatas bacaan (`offset` dan `limit`) daripada membaca keseluruhan isi berkas sepanjang ribuan baris.
3. **Snippet Condensation:** Cukup kutip definisi *interface* atau *method signature* dari modul eksternal, bukan isi implementasi internalnya.

```typescript
// Cukup muat interface definition untuk context saving, bukan full class implementation
export interface ITokenService {
  generateAccessToken(payload: JWTPayload): Promise<string>;
  verifyToken(token: string): Promise<JWTPayload>;
}
```

---

## 🔀 Handoff Protocol (Protokol Serah Terima)

Ketika sesi pengerjaan beralih ke agen lain atau hari baru, buat rangkuman serah terima (*Handoff Package*) secara ringkas namun padat.

### Kerangka Protokol Handoff / Handoff Package Template

```markdown
## 🔀 Handoff Context Summary

### Core Objective
- Migrasi backend dari Express.js ke NestJS.

### Tech Stack Details
- NestJS v10, Prisma ORM, PostgreSQL.

### Critical Decisions Made
- Menggunakan JSON Web Tokens (JWT) dengan umur masa aktif 15 menit.
- Menggunakan enkripsi `Argon2id` untuk penyimpanan kata sandi.

### Outstanding Tasks / Next Steps
- Hubungkan Controller `/users/me` dengan `JwtAuthGuard`.
```

---

## 🔄 Context Recovery (Pemulihan Konteks)

Apabila agen mengalami disorientasi logis atau menerima instruksi bertentangan, segera jalankan protokol pemulihan:

- **Git Log Inspection:** Periksa riwayat commit terakhir untuk mengetahui kondisi kode yang stabil secara objektif.
- **Verification Query:** Tanyakan kepada pengguna satu pertanyaan kalibrasi untuk menyeimbangkan kembali asumsi kerja.

```bash
# Verifikasi status perubahan file secara manual menggunakan git
git diff --name-status master
```

---

## 🚫 Anti-Patterns dalam Context Management

- **Context Hoarding:** Memasukkan semua berkas log mentah berukuran puluhan megabyte langsung ke memori agen tanpa penyaringan (*filtering*).
- **Stale Assumptions:** Mengasumsikan konfigurasi dari dua hari yang lalu masih berlaku tanpa memeriksa perubahan file `package.json` terbaru.
- **Implicit Drift:** Agen mengubah arah pengerjaan proyek secara diam-diam tanpa mencatat penyimpangan tersebut ke dalam *decision log*.

---

*(Konteks yang bersih dan terfokus adalah kunci utama akurasi kode yang dihasilkan oleh kecerdasan buatan.)*
