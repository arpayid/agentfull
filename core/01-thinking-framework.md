# 🧠 01 — Thinking Framework (SOTA 2026)

> *"Kualitas sebuah AI agent ditentukan bukan oleh kecepatan responnya, melainkan oleh kedalaman dan rigoritas proses berpikirnya."*

---

## 📋 Daftar Isi / Table of Contents
1. [Filosofi Dual-System Thinking](#-filosofi-dual-system-thinking)
2. [Problem Decomposition (Pecah Masalah)](#-problem-decomposition)
3. [Hypothesis-Driven Reasoning & Diagnostic Tree](#-hypothesis-driven-reasoning)
4. [First Principles Thinking & Constraint Analysis](#-first-principles-thinking)
5. [Self-Correction Loops & Verification](#-self-correction-loops)
6. [Anti-Patterns dalam Proses Berpikir](#-anti-patterns)

---

## 🎯 Filosofi Dual-System Thinking

Pada standar SOTA 2026, agen cerdas mengadopsi model kognitif manusia yang terbagi menjadi dua sistem utama untuk mengoptimalkan token budget dan kualitas penalaran:

```
                  ┌────────────────────────────────────────┐
                  │           STIMULUS (Input)             │
                  └──────────────────┬─────────────────────┘
                                     │
                                     ▼
                  ┌────────────────────────────────────────┐
                  │        COGNITIVE ROUTER                │
                  └────────┬──────────────────────┬────────┘
                           │                      │
         [Simple / Repetitive]             [Complex / Novel]
                           │                      │
                           ▼                      ▼
                  ┌─────────────────┐    ┌─────────────────┐
                  │    SYSTEM 1     │    │    SYSTEM 2     │
                  │  Fast / Reactive│    │ Slow / Reasoning│
                  └─────────────────┘    └────────┬────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │  Tree of Thought │
                                         │  Self-Correcting│
                                         └─────────────────┘
```

- **System 1 (Reactive):** Digunakan untuk tugas-tugas berisiko rendah yang berulang (misalnya: *syntax formatting*, *renaming variables*, atau menulis *boilerplate code* sederhana). Menghemat token dan waktu eksekusi.
- **System 2 (Deliberative/Reasoning):** Diaktifkan saat menghadapi masalah arsitektural, optimasi algoritma kompleks, atau kegagalan sistem yang ambigu. Proses ini menggunakan *Tree of Thoughts* (ToT) dan eksplorasi *heuristic* secara mandiri.

---

## 🔍 Problem Decomposition

Gunakan *Recursive Decomposition* untuk memecah masalah besar menjadi tugas-tugas atomik yang dapat divalidasi secara terpisah.

### Langkah-Langkah Dekomposisi (Decomposition Workflow)

1. **State the Goal:** Definisikan objektif akhir dengan sangat spesifik.
2. **Identify Dependencies:** Tentukan bagian mana yang harus selesai terlebih dahulu (misal: *schema migration* sebelum menulis *API handler*).
3. **Draft the DAG (Directed Acyclic Graph):** Buat diagram alur dependensi tugas secara linear maupun paralel.

### Contoh Implementasi / Implementation Example

**Task:** *"Migrate our legacy express.js REST API to NestJS with TypeScript, keeping the existing database schema intact."*

```markdown
1. Phase 1: Environment & Setup
   ├── Initialize NestJS project template: `nest new project-name`
   ├── Configure ESLint, Prettier, and TypeScript tsconfig
   └── Set up environmental configuration via `@nestjs/config`

2. Phase 2: Core Database Integration
   ├── Map existing database tables to Prisma/TypeORM schemas
   └── Implement Database module and connection pool verification

3. Phase 3: Route Migration (Iterative)
   ├── Rewrite Authentication Middleware to NestJS Guards
   ├── Port `/api/v1/users` handlers to Controller-Service pattern
   └── Port `/api/v1/billing` handlers with transactional rollback

4. Phase 4: Verification & Integration Testing
   ├── Write integration tests using Jest and Supertest
   └── Run validation check: `npm run test:e2e`
```

---

## 🔬 Hypothesis-Driven Reasoning & Diagnostic Tree

Saat melakukan *debugging* sistem yang rusak, hindari tebakan acak. Gunakan pendekatan saintifik dengan merancang pohon diagnosis (*Diagnostic Tree*).

```
                            [System Outage]
                            /              \
            [Network Issues]                [Application Crash]
            /             \                  /               \
[Latency Spike]  [Packet Drop]      [Out of Memory]   [Database Timeout]
```

### Prosedur Uji Hipotesis (Hypothesis Verification Steps)

1. **Observation:** Kumpulkan bukti empiris (misalnya *stack trace* atau *system metrics*).
2. **Formulate Hypothesis:** Buat daftar kemungkinan penyebab beserta cara mengujinya secara cepat.
3. **Execution & Proof:** Jalankan perintah diagnostik untuk membuktikan atau membantah hipotesis tersebut.

```bash
# Contoh 1: Memeriksa latensi jaringan ke server basis data
ping -c 5 database.internal.net

# Contoh 2: Menganalisis konsumsi memori proses Node.js
node --inspect index.js
```

---

## 💎 First Principles Thinking & Constraint Analysis

Jangan menerima asumsi lama tanpa verifikasi. Bongkar masalah hingga mencapai kebenaran fundamental (*fundamental truths*).

### Studi Kasus: Optimasi Latensi Basis Data (Database Latency Optimization)

- **Asumsi Awal:** *"Kita membutuhkan Redis caching layer karena database PostgreSQL terlalu lambat memproses query pencarian."*
- **Bedah First Principles:**
  - Apakah query PostgreSQL *benar-benar* lambat secara inheren?
  - Jalankan `EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';`.
  - Temukan bahwa kolom `email` tidak memiliki indeks, sehingga PostgreSQL melakukan *Sequential Scan* penuh pada 10 juta baris data.
  - **Solusi Fundamental:** Cukup tambahkan indeks, tanpa perlu menambah kompleksitas operasional dengan Redis cache.

```sql
-- Solusi First Principles untuk menghindari kerumitan cache layer
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

---

## 🔄 Self-Correction Loops & Verification

Sistem SOTA 2026 mewajibkan adanya *feedback loop* internal sebelum kode atau keputusan diserahkan kepada pengguna.

```
                  ┌────────────────────────────────────────┐
                  │             GENERATE CODE              │
                  └──────────────────┬─────────────────────┘
                                     │
                                     ▼
                  ┌────────────────────────────────────────┐
                  │             AUTO-COMPILE               │
                  └──────────────────┬─────────────────────┘
                                     │
                           [Compilation Error]
                                     ├─────────────────────┐
                                     │                     │
                                     ▼                     ▼
                  ┌─────────────────────────────────┐   ┌──┴───────────────┐
                  │       RUN AUTOMATED TESTS       │   │ SELF-HEAL CODE   │
                  └──────────────────┬──────────────┘   └──────────────────┘
                                     │
                             [Test Failure]
                                     └─────────────────────┘
```

1. **Draft:** Tulis kode sesuai spesifikasi.
2. **Compile Check:** Jalankan *compiler* atau *linter* secara lokal (misal: `tsc --noEmit` atau `npm run lint`).
3. **Execution Test:** Jalankan *automated test* untuk memastikan tidak ada fungsi regresi yang rusak.
4. **Refactor:** Jika terjadi kegagalan, perbaiki kembali kode Anda sebelum merespons pengguna.

---

## 🚫 Anti-Patterns dalam Proses Berpikir

Berikut adalah beberapa pola pikir yang harus dihindari oleh agen otonom:

- **Cargo Cult Development:** Mengambil potongan kode dari proyek lain atau internet tanpa memahami cara kerja internalnya.
- **Premature Optimization:** Mengoptimalkan kode untuk performa ekstrim sebelum profil eksekusi menunjukkan adanya hambatan nyata (*bottleneck*).
- **Infinite Loop Reasoning:** Mengulangi langkah perbaikan yang sama sebanyak tiga kali secara berturut-turut tanpa mengubah strategi kognitif (*hard pivot*).

---

*(Dokumen ini merupakan panduan utama proses kognitif agen. Selalu prioritaskan kejelasan, validasi bukti, dan efisiensi penalaran.)*
