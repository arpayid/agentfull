# 📊 Progress Report

> **Kapan digunakan:** Gunakan template ini untuk memberikan laporan berkala kepada user, terutama pada tugas yang memakan waktu lama (long-running tasks) atau saat terjadi pergantian sesi/konteks.

## 🟢 Status Overview
| Metric | Status |
|--------|--------|
| **Current Phase** | `{{PHASE_NAME}}` (e.g., Execution, Planning) |
| **Overall Health**| `{{HEALTH_EMOJI}}` (e.g., 🟢 On Track, 🟡 At Risk, 🔴 Blocked) |
| **Completion**    | `{{PERCENTAGE}}`% |

## ✅ What Was Accomplished
*Ringkasan pekerjaan yang sudah diselesaikan sejak update terakhir.*
- `{{ACCOMPLISHMENT_1}}` (with PR/commit link if applicable)
- `{{ACCOMPLISHMENT_2}}`

## ⏳ In Progress
*Apa yang sedang dikerjakan saat ini.*
- `{{CURRENT_TASK_1}}`

## 🛑 Blockers & Risks
*Hambatan atau risiko yang perlu diketahui oleh user.*
- **Blocker:** `{{BLOCKER_DESCRIPTION}}`
- **Mitigation/Need:** `{{WHAT_YOU_NEED_FROM_USER_OR_SYSTEM}}`

## ⏭️ Next Steps
*Apa yang akan dilakukan selanjutnya setelah blocker/current task selesai.*
1. `{{NEXT_STEP_1}}`
2. `{{NEXT_STEP_2}}`

---

### 📝 Example Filled Version

## 🟢 Status Overview
| Metric | Status |
|--------|--------|
| **Current Phase** | Execution: Authentication Module |
| **Overall Health**| 🟡 At Risk |
| **Completion**    | 65% |

## ✅ What Was Accomplished
*Ringkasan pekerjaan yang sudah diselesaikan sejak update terakhir.*
- ✅ Mengimplementasikan JWT verification middleware ([auth.middleware.ts](file:///src/auth/auth.middleware.ts))
- ✅ Menulis unit tests untuk login flow (100% coverage)

## ⏳ In Progress
*Apa yang sedang dikerjakan saat ini.*
- ⏳ Integrasi OAuth2 dengan Google Provider (menunggu API Key)

## 🛑 Blockers & Risks
*Hambatan atau risiko yang perlu diketahui oleh user.*
- **Blocker:** Tidak ada `GOOGLE_CLIENT_ID` dan `GOOGLE_CLIENT_SECRET` di `.env`.
- **Mitigation/Need:** Mohon berikan kredensial tersebut agar saya bisa melanjutkan pengujian OAuth.

## ⏭️ Next Steps
*Apa yang akan dilakukan selanjutnya setelah blocker/current task selesai.*
1. Selesaikan Google OAuth integrasi.
2. Buat dokumentasi Swagger untuk endpoint `/auth`.
