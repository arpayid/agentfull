# ⚠️ Risk Analysis

> **Kapan digunakan:** Gunakan template ini SEBELUM melakukan perubahan yang berpotensi merusak (breaking changes), migrasi database, atau deployment ke production.

## 🔍 Risk Identification
**Proposed Action:** `{{PROPOSED_ACTION}}`
**Primary Objective:** `{{OBJECTIVE}}`

## 📊 Probability & Impact Matrix

| Risk Scenario | Probability (Low/Med/High) | Impact (Low/Med/High) | Severity |
|---------------|----------------------------|-----------------------|----------|
| `{{RISK_1}}`  | `{{PROB_1}}`               | `{{IMP_1}}`           | `{{SEV_1}}` |
| `{{RISK_2}}`  | `{{PROB_2}}`               | `{{IMP_2}}`           | `{{SEV_2}}` |

## 🛡️ Mitigation Strategies
*Bagaimana kita meminimalisir risiko sebelum dan saat eksekusi.*

### Pre-execution:
- `{{PRE_MITIGATION_1}}`

### During execution:
- `{{DURING_MITIGATION_1}}`

## ↩️ Rollback Plan
*Jika skenario terburuk terjadi, bagaimana kita mengembalikan sistem ke state awal.*
1. `{{ROLLBACK_STEP_1}}`
2. `{{ROLLBACK_STEP_2}}`

---

### 📝 Example Filled Version

## 🔍 Risk Identification
**Proposed Action:** Migrasi kolom `id` pada tabel `Users` dari tipe `INT` menjadi `UUID`.
**Primary Objective:** Mendukung arsitektur distributed database di masa depan dan mencegah ID enumeration attacks.

## 📊 Probability & Impact Matrix

| Risk Scenario | Probability (Low/Med/High) | Impact (Low/Med/High) | Severity |
|---------------|----------------------------|-----------------------|----------|
| Downtime berkepanjangan saat migrasi tabel besar (1M+ rows) | **Medium** | **High** | 🔴 **Critical** |
| Foreign key constraint pada tabel terkait (Posts, Comments) rusak | **High** | **High** | 🔴 **Critical** |
| Performa query menurun akibat indeks UUID yang lebih besar dari INT | **High** | **Low** | 🟡 **Warning** |

## 🛡️ Mitigation Strategies
*Bagaimana kita meminimalisir risiko sebelum dan saat eksekusi.*

### Pre-execution:
- Melakukan dry-run migrasi pada database staging dengan volume data yang sama.
- Menulis script migrasi yang menggunakan *temporary column* alih-alih me-replace langsung.

### During execution:
- Mengaktifkan maintenance mode selama proses eksekusi.
- Memantau I/O dan CPU usage pada database server.

## ↩️ Rollback Plan
*Jika skenario terburuk terjadi, bagaimana kita mengembalikan sistem ke state awal.*
1. Segera hentikan script migrasi.
2. Lakukan *restore* dari snapshot EBS AWS RDS yang diambil 5 menit sebelum eksekusi dimulai.
3. Matikan maintenance mode.
