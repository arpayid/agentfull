# 🧭 06 — Context Management

> *"Sebuah agent yang kehilangan konteks seperti navigator tanpa peta — berjalan tapi
> tidak tahu arah. Context management adalah peta itu."*

---

## 📋 Daftar Isi

1. [Filosofi Context Management](#-filosofi-context-management)
2. [State Tracking](#-state-tracking)
3. [Preference Registry](#-preference-registry)
4. [Decision Log](#-decision-log)
5. [Handoff Protocol](#-handoff-protocol)
6. [Long Conversation Strategy](#-long-conversation-strategy)
7. [Context Window Optimization](#-context-window-optimization)
8. [Context Recovery](#-context-recovery)
9. [Anti-Patterns](#-anti-patterns-dalam-context-management)

---

## 🎯 Filosofi Context Management

Context adalah "working memory" dari sebuah AI agent. Tanpa context management yang baik,
agent akan:
- ❌ Mengulangi pertanyaan yang sudah dijawab
- ❌ Membuat keputusan yang bertentangan dengan keputusan sebelumnya
- ❌ Kehilangan track dari progress yang sudah dicapai
- ❌ Gagal memahami nuansa dan preferensi user

### Context Hierarchy

```
┌──────────────────────────────────────────────────┐
│ GLOBAL CONTEXT (Persistent)                      │
│ ├── User preferences & style                     │
│ ├── Project architecture & conventions           │
│ ├── Tech stack & tools                           │
│ └── Team/organizational context                  │
├──────────────────────────────────────────────────┤
│ SESSION CONTEXT (Per conversation)               │
│ ├── Current task & objectives                    │
│ ├── Decisions made so far                        │
│ ├── Files modified & their state                 │
│ ├── Errors encountered & resolutions             │
│ └── Pending items & blockers                     │
├──────────────────────────────────────────────────┤
│ IMMEDIATE CONTEXT (Current action)               │
│ ├── What am I doing right now?                   │
│ ├── What's the expected outcome?                 │
│ ├── What files/resources am I working with?      │
│ └── What's the next step after this?             │
└──────────────────────────────────────────────────┘
```

### Prinsip Utama

| Prinsip | Deskripsi |
|---------|-----------|
| **Capture Proactively** | Catat informasi penting saat ditemukan, bukan nanti |
| **Summarize Regularly** | Periodically summarize untuk menjaga kejelasan |
| **Prioritize Relevance** | Tidak semua informasi perlu disimpan — filter yang penting |
| **Make it Retrievable** | Konteks yang dicatat tapi tidak bisa ditemukan = tidak berguna |
| **Update Continuously** | Konteks yang outdated lebih berbahaya daripada tidak ada konteks |

---

## 📊 State Tracking

Selalu tahu "di mana kita sekarang" dalam setiap task.

### State Categories

```
1. TASK STATE
   ├── Overall objective (apa yang ingin dicapai)
   ├── Current phase (planning / implementing / testing / deploying)
   ├── Progress (3 of 7 steps completed)
   ├── Blockers (apa yang menghambat)
   └── Next action (apa yang harus dilakukan selanjutnya)

2. FILE STATE
   ├── Files created (baru dibuat)
   ├── Files modified (sudah diubah)
   ├── Files pending (perlu diubah tapi belum)
   └── File dependencies (file A tergantung pada file B)

3. ENVIRONMENT STATE
   ├── Current working directory
   ├── Running processes / services
   ├── Active connections (DB, API, etc.)
   └── Configuration state (env vars, config files)
```

### State Tracking Template

```markdown
## 📍 Current State

### Task Progress
- **Objective**: Implement user authentication
- **Phase**: Implementation (2/4)
- **Completed**:
  - ✅ Database schema for users table
  - ✅ Registration endpoint
- **In Progress**:
  - 🔄 Login endpoint (token generation done, validation pending)
- **Pending**:
  - ⏳ Password reset flow
  - ⏳ Email verification

### Modified Files
| File | Status | Notes |
|------|--------|-------|
| `src/models/user.js` | ✅ Done | Schema + validation |
| `src/routes/auth.js` | 🔄 WIP | Login endpoint 70% done |
| `src/middleware/auth.js` | ⏳ Pending | Needs login to be done first |

### Decisions Made
- Using bcrypt for password hashing (not argon2)
- JWT with 1 hour expiry + refresh token
- Email verification required before login

### Known Issues
- None so far
```

### Kapan Update State?

| Event | Action |
|-------|--------|
| Task dimulai | Initialize state dengan objective + plan |
| Setiap milestone selesai | Update progress, mark completed items |
| Error ditemukan | Log error, update blockers |
| Keputusan dibuat | Add to decision log |
| File diubah | Update file state |
| Arah berubah | Update objective/plan, note alasan perubahan |

---

## 🗃️ Preference Registry

Sistem untuk menangkap, menyimpan, dan menerapkan preferensi user.

### Preference Categories

```yaml
preferences:
  coding_style:
    indentation: "2 spaces"                    # or "4 spaces" / "tabs"
    quotes: "single"                           # or "double"
    semicolons: false                          # JavaScript specific
    naming_convention: "camelCase"             # or "snake_case" / "PascalCase"
    max_line_length: 100
    trailing_comma: true

  communication:
    language: "bilingual (ID + EN)"
    detail_level: "concise"                    # or "detailed"
    explanation_style: "code-first"            # or "explanation-first"
    emoji_usage: "moderate"                    # or "minimal" / "heavy"

  workflow:
    ask_before_changes: true
    auto_format: true
    test_approach: "test-after"                # or "TDD"
    commit_style: "conventional"               # or "freeform"
    branch_strategy: "feature-branch"

  tools:
    package_manager: "npm"                     # or "yarn" / "pnpm" / "bun"
    test_framework: "vitest"                   # or "jest" / "pytest" / "go test"
    linter: "eslint"                           # context-specific
    formatter: "prettier"                      # context-specific

  domain:
    architecture: "modular-monolith"
    database: "postgresql"
    error_handling: "explicit"                 # or "exception-based"
    logging: "structured-json"                 # or "plain-text"
```

### Cara Mendeteksi Preferensi

**Explicit Signals** — User langsung bilang:
```
"Tolong pakai 4 spaces untuk indentation"
"Saya prefer snake_case untuk Python"
"Jangan terlalu verbose ya"
```

**Implicit Signals** — Dari perilaku user:
```
Observasi: User selalu mengubah output agent dari double-quotes ke single-quotes
→ Preferensi: single quotes

Observasi: User selalu menambahkan type annotations ke kode agent
→ Preferensi: strongly typed code

Observasi: User langsung approve tanpa modifikasi saat agent memberi penjelasan singkat
→ Preferensi: concise communication
```

### Menerapkan Preferensi

```markdown
✅ Baik — Adaptive:
"Saya perhatikan kamu menggunakan single quotes dan 2 spaces.
Saya akan mengikuti style yang sama ke depannya."

✅ Baik — Confirming:
"Kamu lebih prefer penjelasan yang to-the-point ya? Saya sesuaikan."

❌ Buruk — Mengabaikan:
*User sudah 3x bilang prefer snake_case, agent masih pakai camelCase*

❌ Buruk — Over-asking:
"Apakah kamu mau 2 spaces atau 4 spaces?" (padahal sudah terlihat dari kode user)
```

### Preference Conflict Resolution

Ketika preferensi user bertentangan dengan best practice:

```
1. Ikuti preferensi user
2. KECUALI jika ada risiko keamanan/data loss
3. Dalam kasus tersebut, inform + suggest alternative + defer to user
```

---

## 📓 Decision Log

Catat setiap keputusan penting agar bisa di-reference dan tidak dilupakan.

### Decision Log Format

```markdown
## Decision Log

### DEC-001: Authentication Method
- **When**: Awal sesi
- **Decision**: JWT with refresh token
- **Alternatives**: Session-based auth, OAuth only
- **Reasoning**: Stateless, scalable, user sudah familiar
- **Status**: Active

### DEC-002: Database Choice
- **When**: Setelah requirement discussion
- **Decision**: PostgreSQL
- **Alternatives**: MySQL, MongoDB
- **Reasoning**: Relational data, ACID compliance needed, user preference
- **Status**: Active

### DEC-003: Code Style
- **When**: Detected from user's existing code
- **Decision**: ESLint + Prettier, 2 spaces, single quotes
- **Alternatives**: N/A (following existing codebase)
- **Reasoning**: Consistency with existing code
- **Status**: Active
```

### Kapan Membuat Decision Entry?

| Selalu Catat | Tidak Perlu Dicatat |
|-------------|---------------------|
| Architecture decisions | Trivial formatting choices |
| Technology choices | Obvious implementation details |
| Trade-offs yang signifikan | Decisions yang bisa di-infer dari context |
| User's explicit preferences | One-off, non-recurring decisions |
| Deviations dari rencana awal | Minor variations |

### Mereferensi Keputusan

```markdown
"Sesuai keputusan kita sebelumnya untuk menggunakan JWT (DEC-001),
saya akan implement token validation di middleware."

"Ini berubah dari rencana awal (DEC-002). Kita awalnya memilih PostgreSQL,
tapi berdasarkan discovery baru tentang requirement X, kita mungkin perlu
reconsider. Thoughts?"
```

---

## 🔀 Handoff Protocol

Ketika context perlu dipindahkan — antar session, antar agent, atau antar task.

### Handoff Package

```markdown
## 🔀 Context Handoff

### Project Summary
[1-2 kalimat tentang apa projectnya]

### Current State
- **Phase**: [di mana kita sekarang]
- **Last completed**: [terakhir yang selesai]
- **Next action**: [yang harus dikerjakan selanjutnya]
- **Blockers**: [jika ada]

### Key Files
| File | Role | Status |
|------|------|--------|
| `src/main.js` | Entry point | ✅ Stable |
| `src/api/auth.js` | Auth module | 🔄 WIP |
| `src/db/schema.sql` | DB schema | ✅ Stable |

### Decisions Made (Important Ones)
1. Using JWT for auth (bukan session-based)
2. PostgreSQL as database
3. Validation using library X

### User Preferences
- Prefers concise responses
- Uses conventional commits
- Likes code-first explanations
- snake_case for Python, camelCase for JavaScript

### Known Issues / Warnings
- Auth rate limiting belum implemented
- Error handling di endpoint Y masih basic
- Test coverage masih rendah (~40%)

### Pending Questions for User
- Apakah perlu email notification untuk password reset?
- Deployment target: cloud VM atau container?
```

### Kapan Membuat Handoff?

- 🔄 Sebelum conversation baru di-start (jika melanjutkan task)
- 👥 Ketika task didelegasikan ke agent lain
- ⏸️ Saat task di-pause dan akan dilanjutkan nanti
- 📋 Ketika scope besar dipecah menjadi sub-tasks

### Self-Handoff (Conversation Continuation)

Ketika melanjutkan conversation sebelumnya:

```markdown
"Berdasarkan conversation sebelumnya, ini summary konteks kita:

**Yang sudah selesai**: [list]
**Yang sedang dikerjakan**: [current task]
**Keputusan penting**: [key decisions]

Apakah masih akurat? Ada perubahan atau tambahan?"
```

---

## 🔄 Long Conversation Strategy

Conversation yang panjang memiliki tantangan unik.

### Tantangan Long Conversations

```
┌─────────────────────────────────────────────────────┐
│ Conversation Length vs Quality                       │
│                                                     │
│ Quality                                             │
│  ▲                                                  │
│  │ ████                                             │
│  │ ████████                                         │
│  │ ████████████                                     │
│  │ ████████████████                                 │
│  │ ████████████████▓▓▓▓                             │
│  │ ████████████████▓▓▓▓░░░░                         │
│  │ ████████████████▓▓▓▓░░░░░░░░                     │
│  └──────────────────────────────────────────► Length │
│                                                     │
│  ████ = Strong context                              │
│  ▓▓▓▓ = Weakening context                           │
│  ░░░░ = Context loss risk zone                      │
└─────────────────────────────────────────────────────┘
```

### Strategi untuk Long Conversations

**1. Periodic Summarization**
```markdown
Setiap 15-20 exchanges, buat checkpoint summary:

"## 📍 Checkpoint Summary (Exchange #20)

Sampai saat ini kita sudah:
1. Setup project structure ✅
2. Implement database layer ✅
3. Build auth module ✅
4. Current: building API endpoints (2/5 done)

Key decisions: [list]
Pending: [list]"
```

**2. Progressive Context Loading**
```
Jangan load semua konteks sekaligus.
Load hanya yang relevan untuk task saat ini.

Task: Fix bug di auth module
→ Load: auth module files, related tests, error logs
→ Skip: unrelated modules, deployment config, documentation
```

**3. Context Anchoring**
```markdown
Gunakan "anchor points" untuk referensi:

"Seperti yang kita diskusikan di bagian database setup,
kita menggunakan PostgreSQL dengan connection pooling.
Sekarang kita perlu menghubungkan itu dengan auth module."
```

**4. Task Decomposition with Context Boundaries**
```
Daripada satu conversation panjang:

Conversation 1: Setup + Database         ← Context: infra
Conversation 2: Authentication           ← Context: auth + DB
Conversation 3: API Endpoints            ← Context: API + auth + DB
Conversation 4: Testing + Deployment     ← Context: all (with summaries)

Setiap conversation dimulai dengan handoff summary dari sebelumnya.
```

### Long Conversation Checklist

- [ ] Apakah saya masih ingat objective utama?
- [ ] Apakah keputusan yang sudah dibuat masih konsisten?
- [ ] Apakah ada informasi yang sudah "hilang" dari konteks?
- [ ] Apakah perlu checkpoint summary?
- [ ] Apakah user perlu di-remind tentang status saat ini?

---

## 🎯 Context Window Optimization

Manfaatkan context window (memori kerja) secara efisien.

### Context Priority System

```
Priority 1 (Always in context): ████████████████████
├── Current task objective
├── Active file contents being edited
├── Most recent error/output
└── Critical user preferences

Priority 2 (Load when needed): ▓▓▓▓▓▓▓▓▓▓▓▓
├── Related file contents
├── Decision log entries
├── Test results
└── Architecture overview

Priority 3 (Reference only): ░░░░░░░░
├── Full project structure
├── Historical conversation
├── Documentation references
└── Alternative approaches considered
```

### Techniques untuk Menghemat Context

**1. Summarize, Don't Repeat**
```markdown
❌ Menyertakan full file content setiap kali:
"Ini isi lengkap file auth.js: [200 baris kode]"

✅ Summarize dan referensi:
"File auth.js sudah ter-update (line 42-58: token validation).
Perubahan utama: menambahkan expiry check."
```

**2. Reference by Location**
```markdown
❌ Copy-paste kode yang sedang didiskusikan:
"Lihat kode ini: [paste 50 baris]"

✅ Reference by file + line:
"Bug-nya di `src/auth.js:42` — fungsi validateToken()
tidak menangani case ketika token expired."
```

**3. Compress Historical Context**
```markdown
Conversation panjang → Compress menjadi summary:

"Context dari discussion sebelumnya:
- Project: REST API e-commerce
- Stack: Node.js + PostgreSQL + Redis
- Status: Auth done, working on product endpoints
- Key decision: Soft delete for all entities"
```

**4. Lazy Loading**
```markdown
Jangan baca semua file di awal. Baca file hanya ketika dibutuhkan:

Step 1: Pahami task → "Perlu fix bug di checkout"
Step 2: Identifikasi file yang relevan → checkout.js, cart.js
Step 3: Baca file-file tersebut
Step 4: Fix bug
Step 5: Baca test file hanya jika perlu verify
```

### Context Budget Allocation

```
Untuk sebuah coding task, alokasikan context window:

┌─────────────────────────────────────────┐
│ Context Window Budget                    │
├──────────────────────┬──────────────────┤
│ Task Description     │ 5%              │
│ Relevant Code        │ 40%             │
│ Working Space        │ 30%             │
│ Output/Reasoning     │ 20%             │
│ Metadata/Prefs       │ 5%              │
└──────────────────────┴──────────────────┘
```

---

## 🔄 Context Recovery

Ketika context hilang atau rusak, bagaimana cara recovery?

### Recovery Strategies

**1. Ask the User**
```markdown
"Saya ingin memastikan konteks kita masih sinkron.
Bisa tolong confirm:
- Kita sedang mengerjakan [X], benar?
- Keputusan terakhir yang kita buat adalah [Y]?
- Apakah ada perubahan yang saya lewatkan?"
```

**2. Re-read Source of Truth**
```markdown
Jika konteks hilang, baca kembali:
1. Project files (source code = source of truth)
2. Git log (history perubahan)
3. README dan documentation
4. Test files (specify expected behavior)
5. Config files (environment & settings)
```

**3. Reconstruct from Artifacts**
```markdown
Gunakan artifact yang sudah dibuat:
- Decision logs
- Progress summaries
- Handoff documents
- Previous conversation transcripts
```

### Context Loss Warning Signs

| Warning Sign | Likely Issue | Action |
|-------------|-------------|--------|
| Agent mengulang pertanyaan | Lost track of previous answers | Check conversation history |
| Keputusan inconsistent | Lost decision context | Review decision log |
| Working on wrong file | Lost task context | Re-read task description |
| Style inconsistency | Lost preference context | Check preference registry |
| Asking about solved problems | Lost resolution context | Check post-mortem/notes |

---

## 🚫 Anti-Patterns dalam Context Management

### 1. Context Hoarding
```
❌ Menyimpan SEMUA informasi tanpa prioritas — context window penuh
✅ Prioritaskan: simpan yang relevan, summarize sisanya, buang noise
```

### 2. Context Amnesia
```
❌ Tidak mencatat apa-apa — setiap interaksi dimulai dari nol
✅ Catat keputusan, preferensi, dan progress secara proaktif
```

### 3. Stale Context
```
❌ Mengandalkan informasi lama tanpa verifikasi
✅ Verifikasi asumsi jika konteks sudah lama: "Masih pakai config yang sama?"
```

### 4. Context Overload
```
❌ Membaca 50 file di awal task "just in case"
✅ Lazy loading — baca file hanya ketika relevan dengan task saat ini
```

### 5. Invisible Context
```
❌ Agent punya konteks di "kepala" tapi tidak dishare ke user
✅ Transparansi — sampaikan ke user apa yang agent "ingat" dan asumsikan
```

### 6. Single Source Dependency
```
❌ Mengandalkan satu sumber konteks (misalnya hanya conversation history)
✅ Multi-source: code, docs, logs, conversation, artifacts
```

### 7. No Checkpoint
```
❌ Conversation 3 jam tanpa checkpoint summary
✅ Checkpoint setiap major milestone atau setiap ~20 exchanges
```

---

## 📊 Context Management Checklist

Evaluasi berkala:

- [ ] **State Tracking**: Apakah saya tahu status terkini dari semua task?
- [ ] **Preferences**: Apakah preferensi user sudah dicatat dan diterapkan?
- [ ] **Decisions**: Apakah semua keputusan penting ter-log?
- [ ] **Handoff Ready**: Apakah saya bisa membuat handoff summary kapan saja?
- [ ] **Window Usage**: Apakah context window digunakan secara efisien?
- [ ] **Fresh Context**: Apakah konteks yang digunakan masih up-to-date?
- [ ] **Recoverability**: Apakah konteks bisa di-recover jika hilang?

---

*"Context yang baik membuat setiap interaksi terasa seperti kelanjutan, bukan permulaan baru." 🧭*
