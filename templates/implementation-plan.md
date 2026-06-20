# 🗺️ Implementation Plan

> **Kapan digunakan:** Digunakan saat agen berada di "Planning Mode" untuk merencanakan perubahan besar yang butuh persetujuan user. Biasa direpresentasikan sebagai artifact markdown.

# [Goal Description]
`{{BRIEF_DESCRIPTION_OF_PROBLEM_AND_SOLUTION}}`

## ⚠️ User Review Required
> [!IMPORTANT]
> `{{CRITICAL_ITEM_THAT_NEEDS_USER_APPROVAL}}`

## ❓ Open Questions
> [!WARNING]
> `{{QUESTIONS_FOR_USER_TO_CLARIFY_AMBIGUITY}}`

## 🛠️ Proposed Changes

### `{{COMPONENT_NAME_1}}`
*Summary of what will change.*

#### [NEW] [`{{NEW_FILE_NAME}}`](file:///{{PATH_TO_NEW_FILE}})
- `{{DESCRIPTION_OF_WHAT_WILL_BE_ADDED}}`

#### [MODIFY] [`{{MODIFIED_FILE_NAME}}`](file:///{{PATH_TO_MODIFIED_FILE}})
- `{{DESCRIPTION_OF_WHAT_WILL_BE_CHANGED}}`

#### [DELETE] [`{{DELETED_FILE_NAME}}`](file:///{{PATH_TO_DELETED_FILE}})
- `{{DESCRIPTION_OF_WHY_IT_IS_DELETED}}`

## ✅ Verification Plan

### Automated Tests
- `{{COMMAND_TO_RUN_TESTS}}`

### Manual Verification
- `{{STEPS_FOR_USER_OR_AGENT_TO_MANUALLY_VERIFY}}`

---

### 📝 Example Filled Version

# Implement Stripe Webhook Handling
Aplikasi saat ini belum bisa menerima notifikasi pembayaran dari Stripe secara real-time. Perubahan ini akan menambahkan endpoint webhook untuk menangani event `checkout.session.completed`.

## ⚠️ User Review Required
> [!IMPORTANT]
> Penambahan dependency baru `stripe` versi 14.x. Apakah ini sesuai standar project?

## ❓ Open Questions
> [!WARNING]
> Bagaimana kita ingin menangani jika webhook memakan waktu lebih dari 5 detik? Apakah kita perlu queue system seperti Redis/BullMQ, atau cukup sinkron?

## 🛠️ Proposed Changes

### API Routes & Controllers
*Menambahkan router dan controller khusus untuk webhook Stripe.*

#### [NEW] [`webhook.controller.ts`](file:///src/controllers/webhook.controller.ts)
- Akan memvalidasi signature Stripe menggunakan `STRIPE_WEBHOOK_SECRET`.
- Memparsing raw body untuk menghindari error JSON parser.

#### [MODIFY] [`app.ts`](file:///src/app.ts)
- Mendaftarkan endpoint `POST /api/webhooks/stripe`.
- Menonaktifkan global JSON parser khusus untuk route webhook ini.

## ✅ Verification Plan

### Automated Tests
- `npm run test -- webhook.controller.spec.ts`

### Manual Verification
- Menjalankan `stripe listen --forward-to localhost:3000/api/webhooks/stripe`
- Memicu event pembayaran dan memverifikasi log database.
