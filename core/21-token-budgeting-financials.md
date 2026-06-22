# 🪙 21 — Token Budgeting & Financial Controls

> *"Kecerdasan tinggi tidak boleh dibayar dengan tagihan API yang tak terkendali."*

---

## 📋 Daftar Isi

1. [Filosofi Kontrol Finansial](#-filosofi-kontrol-finansial)
2. [Alur Evaluasi Anggaran (Budget Evaluation Pipeline)](#-alur-evaluasi-anggaran-budget-evaluation-pipeline)
3. [Kebijakan Token Ceiling (Token Ceiling Policy)](#-kebijakan-token-ceiling-token-ceiling-policy)
4. [Optimasi Biaya Model Reasoning (Reasoning Cost Optimization)](#-optimasi-biaya-model-reasoning-reasoning-cost-optimization)
5. [Skema Log Keuangan JSON (Financial Log Schema)](#-skema-log-keuangan-json-financial-log-schema)
6. [Implementasi Pembatas Anggaran (Budget Guard Code Fragment)](#-implementasi-pembatas-anggaran-budget-guard-code-fragment)
7. [Tindakan Saat Limit Tercapai (Limit Exceeded Playbook)](#-tindakan-saat-limit-tercapai-limit-exceeded-playbook)
8. [Anti-Patterns Kontrol Finansial](#-anti-patterns-kontrol-finansial)

---

## 🎯 Filosofi Kontrol Finansial

Model penalaran masa kini (seperti *o3* atau *Claude Opus 4.8*) membutuhkan biaya token yang sangat tinggi. Sistem kontrol finansial ini mewajibkan agen melacak konsumsi akumulatif token dan **membatasi kedalaman loop berpikir** agar tetap efisien secara ekonomi. Agen harus menyadari biaya finansial dari setiap tool call yang dieksekusi.

---

## 🏗️ Alur Evaluasi Anggaran

Berikut skema keputusan evaluasi token secara proaktif sebelum memanggil API penyedia model:

```
    Kalkulasi Token Terpakai ──► Bandingkan dengan Batas Anggaran Sesi (USD)
                                           │
                             [Apakah Melebihi Batas?]
                              ├── YA  ──► Turunkan Model / Hentikan Sesi (Alert User)
                              └── TIDAK ──► Eksekusi LLM Call
```

---

## 📊 Kebijakan Token Ceiling

Agen harus mematuhi kebijakan alokasi budget yang didefinisikan di bawah ini:

| Kategori Tugas | Maksimal Token per Sesi | Batas Maksimal Biaya (USD) | Fallback |
| :--- | :--- | :--- | :--- |
| **Pencarian File & Review** | 100,000 | $1.00 | Hentikan pencarian jika melebihi limit. |
| **Agentic Coding (RLEF)** | 500,000 | $5.00 | Turunkan ke model MoE yang lebih murah (DeepSeek). |
| **Deep Debugging Loop** | 1,000,000 | $10.00 | Meminta persetujuan otorisasi biaya tambahan dari pengguna. |

---

## ⚙️ Optimasi Biaya Model Reasoning

Untuk menghemat biaya token pada model penalaran (reasoning models):
1. **Gunakan Input Caching**: Jangan mengubah input system prompt yang statis agar dapat memanfaatkan fitur prompt caching dari provider (seperti Anthropic Prompt Caching).
2. **Batasi Output Max Tokens**: Tetapkan parameter `max_tokens` yang sesuai pada API call daripada membiarkannya default tanpa batas.

---

## 📝 Skema Log Keuangan JSON

Agen menyimpan log keuangan sesi di `.agentfull/telemetry/financial.json` secara real-time:

```json
{
  "session_id": "session-123",
  "task_type": "coding",
  "cost_limit_usd": 5.00,
  "accumulated_cost_usd": 1.25,
  "usage_summary": {
    "prompt_tokens": 150000,
    "completion_tokens": 25000,
    "cached_tokens": 85000
  },
  "status": "active"
}
```

---

## 💻 Implementasi Pembatas Anggaran

Berikut skrip Python untuk mengontrol dan menguji apakah biaya transaksi API saat ini masih berada dalam batas aman:

```python
class FinancialBudgetGuard:
    def __init__(self, limit_usd: float):
        self.limit_usd = limit_usd
        self.total_spent = 0.0

    def estimate_and_add_cost(self, prompt_tokens: int, completion_tokens: int, model: str):
        # Pricing per 1M tokens (Mock prices)
        pricing = {
            "claude-3-5-sonnet": {"input": 3.0, "output": 15.0},
            "o3-mini": {"input": 1.1, "output": 4.4},
            "deepseek-coder": {"input": 0.14, "output": 0.28}
        }
        
        rates = pricing.get(model, {"input": 10.0, "output": 30.0})
        cost = (prompt_tokens / 1000000) * rates["input"] + (completion_tokens / 1000000) * rates["output"]
        self.total_spent += cost
        
        print(f"[BudgetGuard] Call Cost: ${cost:.4f}. Total Spent: ${self.total_spent:.4f}")
        return self.total_spent <= self.limit_usd

# Usage Example:
# guard = FinancialBudgetGuard(limit_usd=5.00)
# is_safe = guard.estimate_and_add_cost(100000, 20000, "claude-3-5-sonnet")
# if not is_safe:
#     print("Budget exceeded! Stop API execution.")
```

---

## 🛠️ Tindakan Saat Limit Tercapai

* **Pemberitahuan Instan**: Segera hentikan pemrosesan dan berikan laporan biaya saat ini.
* **Context Pruning**: Lakukan pemotongan log history yang tidak krusial secara radikal untuk memperkecil token input pada request berikutnya.
* **Minta Otorisasi Pengguna**: Berikan tombol konfirmasi atau teks prompt formal agar pengguna dapat menambah budget secara dinamis di runtime.

---

## ⚠️ Anti-Patterns Kontrol Finansial

* ❌ **Blind Execution**: Menjalankan loop iteratif tanpa melacak total pemakaian token di setiap langkahnya.
* ❌ **Missing Fallback**: Membiarkan program gagal total saat batas biaya tercapai tanpa memberikan opsi penurunan kualitas model (graceful degradation).
* ❌ **Uncached Payloads**: Sering memodifikasi baris teratas system prompt secara tidak berkala, sehingga merusak kegunaan cache token provider.
