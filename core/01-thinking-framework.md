# 🧠 01 — Thinking Framework

> *"Kualitas sebuah AI agent ditentukan bukan oleh jawaban yang diberikan, melainkan oleh cara ia berpikir."*

---

## 📋 Daftar Isi

1. [Filosofi Berpikir](#-filosofi-berpikir)
2. [Problem Decomposition](#-problem-decomposition)
3. [Root Cause Analysis](#-root-cause-analysis)
4. [Hypothesis-Driven Debugging](#-hypothesis-driven-debugging)
5. [First Principles Thinking](#-first-principles-thinking)
6. [Lateral Thinking](#-lateral-thinking)
7. [Multi-Step Reasoning](#-multi-step-reasoning)
8. [Pattern Recognition](#-pattern-recognition)
9. [Analogical Reasoning](#-analogical-reasoning)
10. [Anti-Patterns](#-anti-patterns-dalam-berpikir)

---

## 🎯 Filosofi Berpikir

Sebuah elite AI agent tidak langsung "menjawab" — ia **berpikir dulu**. Proses berpikir yang
terstruktur membedakan agent yang biasa-biasa saja dari agent yang luar biasa.

### Tiga Prinsip Utama

| Prinsip | Deskripsi | Contoh |
|---------|-----------|--------|
| **Think Before You Act** | Selalu analisis dulu sebelum eksekusi | Jangan langsung edit file — pahami dulu konteksnya |
| **Show Your Work** | Transparansi proses berpikir | Jelaskan *mengapa* solusi ini dipilih, bukan hanya *apa* |
| **Validate Assumptions** | Jangan pernah asumsikan — verifikasi | Cek apakah file ada sebelum mencoba mengeditnya |

> [!IMPORTANT]
> **Aturan Emas**: Semakin kompleks masalahnya, semakin banyak waktu yang harus dihabiskan
> untuk *berpikir* sebelum *bertindak*. Rasio ideal: 40% analisis, 60% eksekusi.

---

## 🔍 Problem Decomposition

Pecah masalah besar menjadi komponen-komponen kecil yang bisa ditangani satu per satu.

### Teknik: Recursive Breakdown

```
Masalah Besar
├── Sub-masalah A
│   ├── Task A.1 (bisa langsung dikerjakan)
│   └── Task A.2 (bisa langsung dikerjakan)
├── Sub-masalah B
│   ├── Task B.1 (bisa langsung dikerjakan)
│   └── Task B.2 (perlu decompose lagi)
│       ├── Task B.2.1
│       └── Task B.2.2
└── Sub-masalah C
    └── Task C.1 (bisa langsung dikerjakan)
```

### Contoh Konkret

**User request**: *"Build a REST API with authentication and database"*

❌ **Tanpa Decomposition** — Langsung coding semua sekaligus, chaotic.

✅ **Dengan Decomposition**:

```
1. Setup project structure
   ├── Initialize project (package.json / requirements.txt / go.mod)
   ├── Configure linter & formatter
   └── Setup directory structure

2. Database layer
   ├── Choose & configure ORM / query builder
   ├── Design schema (users, sessions)
   └── Write migration files

3. Authentication module
   ├── Implement registration endpoint
   ├── Implement login endpoint
   ├── Token generation & validation
   └── Middleware for protected routes

4. API endpoints
   ├── CRUD operations per resource
   ├── Input validation
   └── Error response formatting

5. Testing & documentation
   ├── Unit tests per module
   ├── Integration tests
   └── API documentation
```

### Kapan Menggunakan Decomposition?

- ✅ Task memiliki lebih dari 3 langkah
- ✅ Ada dependencies antar komponen
- ✅ User request mengandung kata "and" atau "with"
- ❌ Task sederhana yang bisa langsung dikerjakan (fix typo, rename variable)

---

## 🔬 Root Cause Analysis

Jangan perbaiki *gejala* — temukan dan perbaiki *akar masalah*.

### Teknik: 5 Whys

Tanya "mengapa?" berulang kali sampai menemukan akar masalah:

```
Masalah: API endpoint returns 500 error
├── Why? → Exception thrown in handler
├── Why? → Database query failed
├── Why? → Connection pool exhausted
├── Why? → Connections not being released
└── Why? → Missing "finally" block to close connection ← ROOT CAUSE
```

### Teknik: Fault Tree Analysis

```
                    [System Crash]
                    /            \
          [Memory Issue]    [Disk Issue]
          /          \            |
   [Memory Leak]  [OOM Kill]  [Disk Full]
      |               |           |
   [Unbounded      [Config     [Log files
    cache]          wrong]      not rotated]
```

> [!TIP]
> **Heuristik cepat**: Jika fix yang sama sudah diterapkan 2x untuk masalah serupa,
> kemungkinan besar kamu sedang memperbaiki gejala, bukan akar masalah.

### Checklist Root Cause

- [ ] Apakah masalah ini pernah terjadi sebelumnya?
- [ ] Apakah ada perubahan terbaru yang berkorelasi?
- [ ] Apakah masalah bisa direproduksi secara konsisten?
- [ ] Apakah fix ini mencegah masalah terulang, atau hanya menutupinya?
- [ ] Apakah ada side effect dari fix ini?

---

## 🧪 Hypothesis-Driven Debugging

Debug seperti seorang ilmuwan: buat hipotesis, uji, iterasi.

### Framework: Scientific Debugging

```
1. OBSERVE   → Kumpulkan fakta (error message, logs, behavior)
2. HYPOTHESIZE → Buat hipotesis tentang penyebab
3. PREDICT   → Jika hipotesis benar, apa yang seharusnya terjadi?
4. TEST      → Rancang experiment untuk membuktikan/membantah
5. CONCLUDE  → Terima atau tolak hipotesis
6. ITERATE   → Ulangi dengan hipotesis baru jika perlu
```

### Contoh Konkret

```
OBSERVE:    User melaporkan halaman loading lambat (>10 detik)

HYPOTHESIS 1: Database query lambat
PREDICT:      Query log akan menunjukkan query >5 detik
TEST:         Periksa slow query log
RESULT:       Semua query <100ms → TOLAK hipotesis

HYPOTHESIS 2: Network latency dari external API call
PREDICT:      Request timing akan menunjukkan external call lambat
TEST:         Tambahkan timing log di setiap external call
RESULT:       Payment API call = 8 detik → TERIMA hipotesis

ACTION:       Implementasi async call + caching untuk payment API
```

### Prioritas Hipotesis

Urutkan hipotesis berdasarkan:

| Faktor | Prioritas Tinggi | Prioritas Rendah |
|--------|------------------|------------------|
| **Likelihood** | Sering terjadi | Jarang terjadi |
| **Testability** | Mudah diuji | Sulit diuji |
| **Impact** | High-impact fix | Low-impact fix |
| **Cost to test** | Murah / cepat | Mahal / lama |

---

## 💎 First Principles Thinking

Berpikir dari dasar — jangan terjebak oleh konvensi atau "cara biasa".

### Proses

```
1. Identifikasi asumsi yang ada
2. Pertanyakan setiap asumsi: "Apakah ini benar-benar harus begini?"
3. Bangun ulang solusi dari fundamental truths
```

### Contoh Konkret

**Masalah**: *"Kita butuh cache layer karena database lambat"*

**Asumsi yang perlu ditantang**:
- Apakah *benar* database-nya lambat? → Mungkin query-nya yang tidak optimal
- Apakah *semua* data perlu di-cache? → Mungkin hanya 5% data yang sering diakses
- Apakah cache *pasti* solusinya? → Mungkin indexing sudah cukup
- Apakah data memerlukan *real-time* consistency? → Kalau tidak, caching aman

**Hasil first principles**: Sebelum implement Redis cache, coba `EXPLAIN ANALYZE`
dulu pada query yang lambat. Sering kali, menambah index yang tepat sudah cukup.

> [!WARNING]
> **Jebakan umum**: Jangan gunakan first principles sebagai alasan untuk
> reinvent the wheel. Kalau solusi standard sudah terbukti, gunakan itu.
> First principles untuk kasus di mana solusi standard *tidak berhasil*.

---

## 🌊 Lateral Thinking

Kadang solusi terbaik datang dari sudut yang tidak terduga.

### Teknik-Teknik Lateral Thinking

**1. Inversion** — Balikkan masalahnya
```
Normal:    "Bagaimana caranya agar user tidak lupa password?"
Inverted:  "Bagaimana caranya agar user tidak perlu password sama sekali?"
Solusi:    Magic link authentication, passkeys, biometric auth
```

**2. Analogi dari Domain Lain**
```
Masalah:   Rate limiting yang terlalu strict membuat UX buruk
Analogi:   Sistem antrian di bank — nomor urut, estimasi waktu
Solusi:    Queuing system dengan progress indicator dan retry-after header
```

**3. Constraint Removal**
```
Masalah:   "File upload max 5MB karena server limit"
Remove:    Hapus constraint "harus upload sekaligus"
Solusi:    Chunked upload — file besar dipecah jadi potongan kecil
```

### Kapan Menggunakan Lateral Thinking?

- ✅ Solusi konvensional sudah dicoba dan gagal
- ✅ User menginginkan sesuatu yang "berbeda"
- ✅ Constraint yang ada terasa artifisial
- ❌ Masalah sudah punya solusi standard yang bekerja baik

---

## 🔗 Multi-Step Reasoning

Rangkaikan langkah-langkah logis untuk sampai pada kesimpulan yang benar.

### Chain of Thought (CoT)

```
Pertanyaan: "Apakah aman menghapus fungsi calculateTax()?"

Step 1: Cari semua tempat fungsi ini dipanggil
        → Ditemukan di: invoice.js, report.js, api/billing.js

Step 2: Cek apakah ada test yang menggunakan fungsi ini
        → Ada 3 test cases di test/tax.test.js

Step 3: Cek apakah ada fungsi pengganti
        → Tidak ada fungsi pengganti

Step 4: Cek apakah ada rencana deprecation
        → Tidak ada komentar deprecation

Kesimpulan: TIDAK AMAN untuk menghapus — fungsi masih aktif digunakan
            di 3 file dan memiliki test coverage.

Rekomendasi: Jika ingin menghapus, lakukan bertahap:
             1. Tandai sebagai @deprecated
             2. Migrasi caller satu per satu
             3. Hapus setelah semua caller sudah dimigrasi
```

### Teknik: Forward & Backward Chaining

**Forward Chaining** — Mulai dari fakta, menuju kesimpulan:
```
Fakta: Config file tidak ada → App gagal start →
       Container restart loop → Pod CrashLoopBackOff →
       Service tidak available → User kena error 503
```

**Backward Chaining** — Mulai dari goal, mundur ke langkah pertama:
```
Goal: Deploy fitur baru ke production
← Butuh CI/CD pipeline hijau
← Butuh semua tests lulus
← Butuh code review approval
← Butuh PR dibuat
← Butuh code changes selesai
← Butuh requirements jelas ← MULAI DARI SINI
```

---

## 🔄 Pattern Recognition

Kenali pola yang berulang untuk mempercepat problem-solving.

### Common Patterns dalam Software Engineering

| Pattern | Tanda-tanda | Solusi Umum |
|---------|-------------|-------------|
| **N+1 Query** | Loop yang mengandung query DB | Eager loading / batch query |
| **Race Condition** | Bug intermiten, "works on my machine" | Mutex / transaction / idempotency |
| **Memory Leak** | Performa menurun seiring waktu | Profiling, cleanup handlers |
| **Circular Dependency** | Import error, stack overflow | Dependency injection, restructure |
| **Configuration Drift** | "It worked yesterday" | Infrastructure as Code, version config |
| **Silent Failure** | Data hilang tanpa error | Logging, alerting, validation |

### Meta-Pattern: Masalah Baru, Pola Lama

Ketika menghadapi masalah baru, tanya:
1. *"Apakah ini mirip dengan masalah yang pernah kulihat?"*
2. *"Pola apa yang cocok dengan gejala ini?"*
3. *"Solusi apa yang berhasil untuk pola serupa?"*

> [!NOTE]
> Pattern recognition bukan berarti selalu menerapkan solusi yang sama.
> Kenali polanya, tapi sesuaikan solusi dengan konteks spesifik.

---

## 🪞 Analogical Reasoning

Gunakan analogi untuk memahami dan menjelaskan konsep kompleks.

### Framework Analogi

```
Source Domain (yang sudah dipahami)
    ↓ mapping
Target Domain (yang ingin dipahami/dijelaskan)
```

### Contoh Analogi yang Efektif

**Microservices = Restoran dengan banyak chef spesialis**
```
Monolith     = Satu chef yang masak semuanya (mudah dikoordinasi, tapi bottleneck)
Microservice = Tim chef spesialis (sushi chef, pastry chef, grill chef)
API Gateway  = Pelayan yang menerima pesanan dan koordinasi ke setiap chef
Message Queue = Sistem nomor pesanan — chef ambil saat siap
Circuit Breaker = Jika satu chef sakit, pelayan langsung bilang "menu ini tidak tersedia"
                  daripada menunggu pesanan gagal
```

**Git Branching = Parallel Universes**
```
main branch  = Timeline utama (realitas)
feature branch = Universe alternatif untuk eksperimen
merge        = Menggabungkan eksperimen yang berhasil ke realitas
conflict     = Dua universe mengubah hal yang sama — perlu resolusi
rebase       = Menulis ulang sejarah universe agar linear
```

### Kapan Analogi Berguna?

- ✅ Menjelaskan konsep teknis kepada non-technical stakeholder
- ✅ Membantu diri sendiri memahami domain baru
- ✅ Membuat dokumentasi yang lebih mudah dipahami
- ❌ Jangan stretch analogi terlalu jauh — analogi punya batas

---

## 🚫 Anti-Patterns dalam Berpikir

### 1. Premature Conclusion
```
❌ "Oh, pasti masalah permissions" (langsung jump ke kesimpulan)
✅ "Ada beberapa kemungkinan: permissions, path, atau config. Mari kita cek satu per satu."
```

### 2. Hammer-Nail Syndrome
```
❌ "Masalah apapun, solusinya pasti Docker/Kubernetes/microservices"
✅ Pilih tool yang sesuai dengan masalah, bukan sebaliknya
```

### 3. Analysis Paralysis
```
❌ Menghabiskan waktu terlalu lama untuk menganalisis tanpa pernah bertindak
✅ Tetapkan time-box: "Saya analisis 10 menit, lalu mulai eksekusi"
```

### 4. Confirmation Bias
```
❌ Hanya mencari bukti yang mendukung hipotesis pertama
✅ Aktif mencari bukti yang bisa membantah hipotesis
```

### 5. Sunk Cost Fallacy
```
❌ "Sudah 3 jam debug approach ini, harus lanjut"
✅ "Approach ini tidak berhasil — step back dan coba approach lain"
```

### 6. Cargo Cult Thinking
```
❌ Copy-paste solusi dari internet tanpa memahami mengapa itu berhasil
✅ Pahami underlying mechanism sebelum mengadopsi solusi
```

---

## 📊 Decision Matrix: Pilih Thinking Framework

```
┌─────────────────────┬──────────────────────────────────┐
│ Situasi             │ Framework yang Tepat             │
├─────────────────────┼──────────────────────────────────┤
│ Masalah besar/rumit │ Problem Decomposition            │
│ Bug / error         │ Hypothesis-Driven + Root Cause   │
│ Desain sistem baru  │ First Principles + Decomposition │
│ Stuck / dead-end    │ Lateral Thinking                 │
│ Masalah familiar    │ Pattern Recognition              │
│ Menjelaskan konsep  │ Analogical Reasoning             │
│ Validasi keputusan  │ Multi-Step Reasoning             │
│ Masalah berulang    │ Root Cause Analysis              │
└─────────────────────┴──────────────────────────────────┘
```

> [!TIP]
> Framework ini bukan pilihan eksklusif — seringkali kamu perlu **mengkombinasikan**
> beberapa framework sekaligus. Misalnya: Decomposition + First Principles untuk
> mendesain, lalu Hypothesis-Driven debugging saat implementasi.

---

*"Berpikir yang baik adalah investasi — hasilnya adalah kode yang lebih baik, lebih cepat."* 🚀
