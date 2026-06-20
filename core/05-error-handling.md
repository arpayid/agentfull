# 🔧 05 — Error Handling & Recovery

> *"Bug dan error bukan musuh — mereka adalah feedback dari system yang memberitahu
> kita apa yang perlu diperbaiki."*

---

## 📋 Daftar Isi

1. [Filosofi Error Handling](#-filosofi-error-handling)
2. [Log Reading Strategy](#-log-reading-strategy)
3. [Isolation Technique](#-isolation-technique)
4. [Incremental Fixes](#-incremental-fixes)
5. [Rollback Awareness](#-rollback-awareness)
6. [Post-Mortem Analysis](#-post-mortem-analysis)
7. [Error Communication](#-error-communication)
8. [Common Error Patterns](#-common-error-patterns)
9. [Recovery Playbooks](#-recovery-playbooks)
10. [Anti-Patterns](#-anti-patterns-dalam-error-handling)

---

## 🎯 Filosofi Error Handling

### Tiga Pilar Error Handling

```
              ┌──────────────┐
              │   DIAGNOSE   │  ← Temukan akar masalah
              │  (Identifikasi│
              │   root cause) │
              └──────┬───────┘
                     │
         ┌───────────┼───────────┐
         │                       │
  ┌──────┴───────┐      ┌───────┴──────┐
  │    RECOVER   │      │   PREVENT    │
  │  (Pulihkan   │      │  (Cegah      │
  │   ke normal) │      │   berulang)  │
  └──────────────┘      └──────────────┘
```

### Prinsip Utama

| Prinsip | Deskripsi |
|---------|-----------|
| **Fix the Root, Not the Symptom** | Jangan hanya matikan alarm — cari dan perbaiki sumber apinya |
| **One Change at a Time** | Ubah satu hal, test, lalu ubah hal berikutnya |
| **Always Have a Rollback** | Sebelum fix, pastikan bisa kembali ke state sebelumnya |
| **Document the Journey** | Catat apa yang dicoba dan hasilnya — termasuk yang gagal |
| **Communicate Early** | Beritahu user saat menemukan error, jangan diam-diam |
| **Learn from Errors** | Setiap error adalah kesempatan untuk improve sistem |

---

## 📖 Log Reading Strategy

Log adalah sumber kebenaran utama saat debugging. Tapi log yang banyak bisa overwhelming
tanpa strategi yang tepat.

### Strategi Membaca Log

**1. Start from the End (Reverse Chronological)**
```
Mulai dari error terakhir, lalu trace backward ke penyebabnya.

Log output:
[14:00:01] INFO  Server starting...
[14:00:02] INFO  Database connected
[14:00:03] INFO  Loading configuration...
[14:00:03] WARN  Config file not found, using defaults  ← 🔍 CLUE
[14:00:04] INFO  Starting HTTP server on :8080
[14:00:05] ERROR Connection refused on port 5432        ← ❌ ERROR
[14:00:05] FATAL Server shutdown: database unavailable   ← 💀 START HERE

Reading order: FATAL → ERROR → WARN (trace back sampai ketemu root cause)
```

**2. Filter by Severity**
```bash
# Lihat hanya error dan fatal
grep -E "(ERROR|FATAL)" application.log

# Lihat warning ke atas
grep -E "(WARN|ERROR|FATAL)" application.log

# Exclude noise (health checks, etc)
grep -v "health_check" application.log | grep -E "(ERROR|FATAL)"
```

**3. Time-Window Analysis**
```bash
# Lihat log sekitar waktu kejadian error (5 menit sebelum)
# Sesuaikan format timestamp dengan aplikasi kamu
grep "2024-01-15 14:0[0-5]" application.log
```

**4. Correlation ID Tracing**
```bash
# Trace satu request melalui multiple services
grep "req-id-abc123" *.log
```

### Log Reading Checklist

- [ ] Apa error message yang exact?
- [ ] Kapan pertama kali error ini muncul?
- [ ] Apakah ada pattern (interval, condition)?
- [ ] Apa yang terjadi sesaat sebelum error?
- [ ] Apakah ada warning yang mungkin related?
- [ ] Apakah error ini mempengaruhi seluruh system atau sebagian?

> [!TIP]
> **Heuristik**: Jika log tidak memberikan informasi yang cukup, itu sendiri
> adalah masalah — tambahkan logging yang lebih baik sebagai bagian dari fix.

---

## 🔬 Isolation Technique

Isolasi masalah untuk mempersempit area pencarian.

### Teknik Binary Search Debugging

```
Masalah: Suatu fitur tidak berjalan setelah beberapa perubahan.

Step 1: Identifikasi range perubahan
        → 10 commit terakhir

Step 2: Test di titik tengah (commit ke-5)
        → Masih berfungsi ✅

Step 3: Test di titik tengah atas (commit ke-8)
        → Rusak ❌

Step 4: Test commit ke-6
        → Masih berfungsi ✅

Step 5: Test commit ke-7
        → Rusak ❌ ← FOUND: Bug introduced di commit ke-7
```

Teknik ini mengurangi pencarian dari O(n) menjadi O(log n).

### Teknik Environment Isolation

```
Masalah terjadi di production tapi tidak di development?

┌──────────────────────────────────────────────┐
│ Bandingkan environment:                      │
│                                              │
│ Factor        │ Dev          │ Prod          │
│ ──────────────┼──────────────┼────────────── │
│ OS            │ macOS        │ Linux         │
│ DB version    │ 14.1         │ 14.8          │
│ Config        │ debug=true   │ debug=false   │
│ Data volume   │ 100 rows     │ 1M rows    ← │ SUSPECT
│ Concurrency   │ 1 user       │ 500 users  ← │ SUSPECT
│ Network       │ localhost     │ VPC          │
└──────────────────────────────────────────────┘
```

### Teknik Component Isolation

```
System tidak berfungsi — component mana yang bermasalah?

┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Frontend │────→│   API   │────→│  Cache  │────→│   DB    │
│          │     │         │     │         │     │         │
│  Test: ✅│     │ Test: ✅ │     │ Test: ❌│     │ Test: ✅ │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                     ↑
                              PROBLEM HERE

Cara test per component:
1. Frontend: Bisa render? Network requests ke API berhasil?
2. API: Response langsung (bypass cache) berhasil?
3. Cache: Manual get/set berhasil? Connection alive?
4. DB: Direct query berhasil? Connection pool healthy?
```

### Isolation Decision Tree

```
Masalah ditemukan
  │
  ├── Bisa direproduksi secara konsisten?
  │    ├── YES → Isolasi berdasarkan input/condition
  │    └── NO  → Kemungkinan race condition atau timing issue
  │             → Tambahkan logging, cari pattern
  │
  ├── Terjadi di semua environment?
  │    ├── YES → Bug di code logic
  │    └── NO  → Environment-specific issue (config, deps, data)
  │
  └── Terjadi untuk semua user/request?
       ├── YES → Systemic issue
       └── NO  → Data-dependent atau permission-related
```

---

## 🔨 Incremental Fixes

Jangan coba perbaiki semuanya sekaligus — lakukan satu langkah per waktu.

### The Incremental Fix Loop

```
┌──────────────────────────────────────────┐
│                                          │
│  1. Identify smallest possible fix       │
│         │                                │
│  2. Apply fix                            │
│         │                                │
│  3. Test — apakah berhasil?              │
│         │                                │
│    ┌────┴────┐                           │
│    │         │                           │
│   YES       NO                           │
│    │         │                           │
│  4.Done    5.Revert fix                  │
│             │                            │
│          6.Try next hypothesis           │
│             │                            │
│          └──→ (kembali ke step 1)        │
│                                          │
└──────────────────────────────────────────┘
```

### Contoh Incremental Debugging

```markdown
## Masalah: API returns 500 error

### Attempt 1: Check if server is running
- ✅ Server running, port listening
- → Bukan masalah server process

### Attempt 2: Check request format
- ✅ Request format valid (tested with cURL)
- → Bukan masalah client-side

### Attempt 3: Check database connection
- ❌ Database connection timeout!
- → ROOT CAUSE: Database connection pool exhausted

### Fix Applied
- Increased pool size from 5 to 20
- Added connection timeout of 5s
- Added connection release in finally block

### Verification
- ✅ API returns 200 with valid data
- ✅ No connection leaks after 100 requests
- ✅ Graceful error when pool is full (503 instead of 500)
```

### Aturan Incremental Fixing

| Aturan | Penjelasan |
|--------|-----------|
| **Satu perubahan per iterasi** | Jika ubah 3 hal sekaligus dan berhasil, kamu tidak tahu mana yang fix |
| **Test setelah setiap perubahan** | Jangan stack fixes tanpa verifikasi |
| **Revert jika tidak membantu** | Fix yang tidak solve problem = noise yang perlu di-clean up |
| **Document setiap attempt** | Termasuk yang gagal — agar tidak diulangi |
| **Prioritaskan fix yang paling likely** | Berdasarkan hypothesis-driven debugging |

---

## ⏮️ Rollback Awareness

Selalu tahu cara kembali ke state yang stabil.

### Rollback Readiness Checklist

```
Sebelum membuat perubahan apapun:

□ Apakah saya tahu state saat ini? (commit hash, config version)
□ Apakah saya punya backup/snapshot?
□ Apakah saya tahu cara rollback?
□ Berapa lama rollback membutuhkan waktu?
□ Apakah rollback akan menyebabkan data loss?
```

### Rollback Strategies per Tipe Perubahan

| Tipe Perubahan | Rollback Strategy | Complexity |
|----------------|-------------------|------------|
| Code change | `git revert <commit>` | 🟢 Easy |
| Config change | Restore previous config file | 🟢 Easy |
| Dependency update | Revert lockfile, reinstall | 🟡 Medium |
| Database schema (additive) | Down migration | 🟡 Medium |
| Database schema (destructive) | Restore from backup | 🔴 Hard |
| Data migration | Reverse migration script | 🔴 Hard |
| Infrastructure change | Terraform rollback / restore snapshot | 🟡 Medium |
| API contract change | Version the API, maintain old version | 🔴 Hard |

### Pre-Change Safety Net

```bash
# Sebelum mengubah code
git stash  # atau git commit (WIP)

# Sebelum mengubah database
# Buat backup/snapshot sesuai database yang digunakan
pg_dump dbname > backup_$(date +%Y%m%d_%H%M%S).sql  # PostgreSQL
mongodump --db=dbname --out=backup/                   # MongoDB

# Sebelum mengubah config
cp config.yaml config.yaml.backup

# Sebelum mengubah infrastructure
# Simpan state file / buat snapshot
terraform plan -out=planned_changes.tfplan
```

> [!CAUTION]
> **Rule of Thumb**: Jika kamu tidak bisa menjelaskan cara rollback dalam
> 30 detik, kamu belum cukup prepared untuk melakukan perubahan tersebut.

---

## 📋 Post-Mortem Analysis

Setelah error diselesaikan, lakukan post-mortem untuk mencegah berulang.

### Post-Mortem Template

```markdown
# Post-Mortem: [Judul Incident]

## Timeline
| Waktu | Event |
|-------|-------|
| 14:00 | Error pertama terdeteksi |
| 14:05 | Investigation dimulai |
| 14:15 | Root cause teridentifikasi |
| 14:20 | Fix diterapkan |
| 14:25 | Verifikasi berhasil |
| 14:30 | Monitoring: semua normal |

## Root Cause
[Penjelasan teknis tentang akar masalah]

## Impact
- Duration: [berapa lama]
- Users affected: [berapa banyak]
- Data loss: [ada/tidak]
- Revenue impact: [jika applicable]

## What Went Well
- [Hal positif selama incident response]

## What Went Wrong
- [Hal yang perlu diperbaiki]

## Action Items
| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | [preventive action] | [who] | [when] | [ ] |
| 2 | [monitoring improvement] | [who] | [when] | [ ] |
| 3 | [documentation update] | [who] | [when] | [ ] |

## Lessons Learned
- [Key takeaway 1]
- [Key takeaway 2]
```

### Post-Mortem Principles

- 🎯 **Blameless**: Fokus pada sistem dan proses, bukan individu
- 📊 **Data-driven**: Gunakan log, metrics, dan timeline — bukan ingatan
- 🔄 **Actionable**: Setiap finding harus punya action item
- 📚 **Shared**: Post-mortem harus bisa diakses dan dipelajari oleh tim
- ⏰ **Timely**: Lakukan segera selagi ingatan masih segar

---

## 📢 Error Communication

Cara menyampaikan error kepada user sangat menentukan pengalaman mereka.

### Framework Komunikasi Error

```
1. WHAT   → Apa yang terjadi? (singkat, jelas)
2. WHY    → Mengapa terjadi? (root cause)
3. IMPACT → Apa dampaknya? (apa yang terpengaruh)
4. FIX    → Apa yang sedang/sudah dilakukan?
5. NEXT   → Apa langkah selanjutnya?
```

### Contoh Komunikasi Error yang Baik

```markdown
❌ Buruk — Terlalu teknis & panik:
"CRITICAL ERROR: Unhandled promise rejection at Object.<anonymous>
(/app/src/controllers/user.js:42:15) TypeError: Cannot read property
'id' of undefined. Stack trace: [500 baris stack trace]"

❌ Buruk — Terlalu vague:
"Ada error. Coba lagi nanti."

✅ Baik — Jelas dan actionable:
"## ⚠️ Error pada User Registration

**Apa yang terjadi**: Proses registrasi gagal karena email validation
mengalami error saat memproses format email yang mengandung karakter '+'.

**Dampak**: User dengan email format 'user+tag@domain.com' tidak bisa
mendaftar. User dengan format email biasa tidak terpengaruh.

**Root cause**: Regex validation terlalu strict — tidak meng-handle
karakter '+' yang sebenarnya valid di email address.

**Fix**: Saya sudah update regex pattern untuk menerima karakter '+'.

**Verifikasi**: Email 'test+label@example.com' sekarang berhasil
divalidasi. Test suite: 15/15 passed ✅"
```

### Tone untuk Berbagai Tingkat Error

| Severity | Tone | Contoh Opening |
|----------|------|----------------|
| **Info** | Casual, informative | "Satu hal kecil yang perlu diperhatikan..." |
| **Warning** | Attentive, clear | "Saya menemukan potensi masalah yang perlu dicek..." |
| **Error** | Calm, solution-focused | "Ada error yang perlu diperbaiki. Ini analisis saya..." |
| **Critical** | Urgent, structured | "⚠️ Masalah kritis yang memerlukan tindakan segera..." |

---

## 🗺️ Common Error Patterns

### Pattern Reference Table

| # | Pattern | Gejala | Root Cause Umum | Solusi Umum |
|---|---------|--------|-----------------|-------------|
| 1 | **Connection Refused** | Cannot connect to host:port | Service not running / wrong port | Check service status, verify port |
| 2 | **Timeout** | Request hangs, then fails | Slow query / network issue / deadlock | Optimize query, check network, add timeout |
| 3 | **Out of Memory** | OOM killed, crash | Memory leak / unbounded data | Profile memory, add limits, pagination |
| 4 | **Permission Denied** | 403 / EACCES | Wrong user/role / missing chmod | Check ownership, permissions, IAM |
| 5 | **Module Not Found** | ImportError / require error | Missing dependency / wrong path | Install dependency, fix import path |
| 6 | **Encoding Error** | Garbled text / UnicodeError | Mixed encodings / missing UTF-8 | Normalize encoding, specify charset |
| 7 | **Race Condition** | Intermittent bugs | Concurrent access without sync | Mutex, transaction, idempotency key |
| 8 | **Null Reference** | NullPointerException / undefined | Missing null check / bad data | Defensive programming, optional chaining |
| 9 | **Stack Overflow** | Maximum call stack exceeded | Infinite recursion / deep nesting | Add base case, increase limit, iterative |
| 10 | **Disk Full** | Write errors / no space | Logs / temp files / large uploads | Clean up, rotate logs, add monitoring |

### Deep Dive: Top 3 Patterns

**Pattern 1: The Silent Failure**
```python
# ❌ Error ditelan — tidak ada yang tahu ada masalah
try:
    result = process_payment(order)
except Exception:
    pass  # "It's fine" — narrator: it was not fine

# ✅ Error ditangani dengan tepat
try:
    result = process_payment(order)
except PaymentGatewayError as e:
    logger.error(f"Payment failed for order {order.id}: {e}")
    notify_ops_team(severity="high", message=str(e))
    raise PaymentFailedError(f"Unable to process payment: {e}") from e
```

**Pattern 2: The Cascade Failure**
```
Service A down → Service B timeout (waiting for A) →
Service C fails (depends on B) → User sees error →
User retries → More load → Everything collapses

Solusi: Circuit breaker pattern
┌─────────────────────────────────────────────┐
│ Circuit Breaker States:                      │
│                                              │
│ CLOSED → (errors exceed threshold) → OPEN   │
│   ↑                                   │     │
│   └── (test succeeds) ← HALF-OPEN ←──┘     │
│                          (after timeout)     │
└─────────────────────────────────────────────┘
```

**Pattern 3: The Configuration Mismatch**
```yaml
# Dev config (works)
database:
  host: localhost
  port: 5432
  ssl: false

# Prod config (fails — tapi kenapa?)
database:
  host: db.internal
  port: 5432
  ssl: true           # ← SSL cert not configured!
  # pool_size: 5      # ← Default terlalu kecil untuk production
```

---

## 🎮 Recovery Playbooks

### Playbook 1: Application Won't Start

```
Step 1: Check logs → Apa error message-nya?
Step 2: Check config → Apakah semua config values valid?
Step 3: Check dependencies → Apakah semua services yang dibutuhkan running?
Step 4: Check ports → Apakah port sudah digunakan process lain?
Step 5: Check permissions → Apakah app punya akses ke file/directory yang dibutuhkan?
Step 6: Check disk space → Apakah disk penuh?
Step 7: Try clean start → Hapus cache/temp files, restart fresh
```

### Playbook 2: Database Issues

```
Step 1: Is the database reachable? → ping / telnet host port
Step 2: Can you authenticate? → Test connection with credentials
Step 3: Is the database overloaded? → Check active connections, CPU, memory
Step 4: Is the query the problem? → Run query directly, check EXPLAIN
Step 5: Is there a lock/deadlock? → Check lock tables
Step 6: Is disk space available? → Check tablespace usage
```

### Playbook 3: Performance Degradation

```
Step 1: Identify the bottleneck
        → CPU? Memory? I/O? Network? Database?

Step 2: Reproduce with profiling
        → Application profiler, database EXPLAIN, network trace

Step 3: Check for recent changes
        → New deployment? Config change? Traffic spike?

Step 4: Targeted fix
        → Optimize the specific bottleneck found

Step 5: Verify improvement
        → Compare before/after metrics
```

---

## 🚫 Anti-Patterns dalam Error Handling

### 1. Catch-All Swallow
```python
# ❌ Menelan semua error tanpa penanganan
try:
    do_something()
except Exception:
    pass
```

### 2. Error Message Without Context
```
# ❌ Pesan error tanpa konteks
raise Error("Failed")

# ✅ Pesan error yang informatif
raise Error(f"Failed to process order {order_id}: invalid quantity {qty}")
```

### 3. Retry Without Backoff
```python
# ❌ Retry aggressive — bisa membuat masalah lebih parah
while True:
    try:
        result = call_api()
        break
    except:
        continue  # Instant retry = DDoS on already-struggling service

# ✅ Retry with exponential backoff
for attempt in range(max_retries):
    try:
        result = call_api()
        break
    except TransientError:
        wait_time = (2 ** attempt) + random.uniform(0, 1)
        time.sleep(wait_time)
```

### 4. Fix Then Forget
```
❌ Fix error → move on → same error terjadi lagi 2 bulan kemudian
✅ Fix error → post-mortem → preventive action → monitoring
```

### 5. Blame the User
```
❌ "User memasukkan data yang salah, bukan bug kita"
✅ "Input validation kita harus lebih robust untuk mencegah ini"
```

### 6. Panic-Driven Fixing
```
❌ Mengubah banyak hal sekaligus karena panik
✅ Tenang, isolasi masalah, fix satu hal per waktu
```

---

## 📊 Error Severity Guide

```
┌────────────────────────────────────────────────────────┐
│ Severity Guide                                         │
├──────────┬──────────────────┬──────────────────────────┤
│ Level    │ Deskripsi        │ Expected Response Time   │
├──────────┼──────────────────┼──────────────────────────┤
│ 🔴 P0    │ System down      │ Immediate — drop everything│
│ 🟠 P1    │ Major feature    │ Within minutes            │
│          │ broken           │                           │
│ 🟡 P2    │ Feature degraded │ Within hours              │
│          │ but usable       │                           │
│ 🟢 P3    │ Minor issue      │ Within days (next sprint) │
│ ⚪ P4    │ Cosmetic /       │ When convenient           │
│          │ nice-to-have     │                           │
└──────────┴──────────────────┴──────────────────────────┘
```

---

*"Error handling yang baik bukan tentang menghindari error — tapi tentang menghadapinya
dengan tenang, memperbaikinya dengan tepat, dan mencegahnya terulang." 🛡️*
