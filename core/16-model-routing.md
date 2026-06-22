# 🔀 16 — Intelligent Model Routing for Agentic Tasks

> *"Tidak semua pekerjaan butuh model superkomputer. Pilihlah senjata yang tepat untuk target yang sesuai."*

---

## 📋 Daftar Isi

1. [Filosofi Model Routing](#-filosofi-model-routing)
2. [Arsitektur Router Dinamis (Dynamic Router Architecture)](#-arsitektur-router-dinamis-dynamic-router-architecture)
3. [Matriks Keputusan Routing (Routing Decision Matrix)](#-matriks-keputusan-routing-routing-decision-matrix)
4. [Algoritma Perutean Dinamis (Dynamic Routing Algorithm)](#-algoritma-perutean-dinamis-dynamic-routing-algorithm)
5. [Skema Konfigurasi Router (Router YAML Configuration)](#-skema-konfigurasi-router-router-yaml-configuration)
6. [Studi Kasus Eksekusi (Routing Case Studies)](#-studi-kasus-eksekusi-routing-case-studies)
7. [Anti-Patterns Model Routing](#-anti-patterns-model-routing)

---

## 🎯 Filosofi Model Routing

Intelligent Model Routing adalah **mekanisme pengalihan otomatis** tugas agen ke model LLM yang paling optimal berdasarkan tingkat kesulitan, biaya (cost), dan kebutuhan context window. Ini mencegah pemborosan token pada model proprietary berbiaya tinggi untuk tugas-tugas sepele seperti pemformatan regex atau pembuatan boilerplate kode dasar.

---

## 🏗️ Arsitektur Router Dinamis

Router mengevaluasi masukan tugas dan mengarahkannya ke model yang paling efisien:

```
                  ┌──────────────────────┐
                  │   KLASIFIKASI TASK   │
                  └──────────┬───────────┘
                             │
            [Apakah Task Butuh Banyak File?]
             ├── YA  → Route ke Claude Opus (Large Context)
             └── TIDAK → [Apakah Butuh Penalaran Rumit?]
                           ├── YA  → Route ke GPT-5.5 (o3 reasoning)
                           └── TIDAK → Route ke DeepSeek Coder (Fast & Cheap)
```

---

## 📊 Matriks Keputusan Routing

| Jenis Tugas | Persyaratan Teknis | Rekomendasi Model | Mengapa? |
| :--- | :--- | :--- | :--- |
| **Codebase Refactoring** | Context window besar (> 200K token) | **Claude Opus 4.8** | Pemahaman interface structural lintas file sangat konsisten. |
| **Logic & Algorithmic Debugging** | Penalaran mendalam (Chain-of-thought) | **GPT-5.5 / o3** | Unggul dalam memecahkan visual/logic loop buntu. |
| **Boilerplate & Test Generation** | Kecepatan & Biaya Rendah | **DeepSeek Coder V3** | Kecepatan inferensi tinggi dengan biaya minimal. |
| **Private/Local Development** | Keamanan Data Maksimal | **Llama 3.1 405B** | Model open-source terkuat tanpa koneksi internet. |

---

## 💻 Algoritma Perutean Dinamis

Berikut adalah skrip Python yang menunjukkan bagaimana sebuah agen menilai kompleksitas kode dan mengarahkan API call secara dinamis:

```python
import os

def determine_model_route(task_description: str, total_files: int, code_complexity: str) -> str:
    """
    Dynamically routes coding tasks to the most cost-effective and capable model.
    """
    # Lowercase description for keyword scanning
    task_desc = task_description.lower()
    
    # Rule 1: Large codebase integration goes to Claude
    if total_files > 15 or "refactor" in task_desc:
        return "claude-3-5-sonnet-v2"
        
    # Rule 2: Hard math or recursive logic goes to Reasoning models
    if "recursion" in task_desc or "optimize memory" in task_desc or code_complexity == "high":
        return "o3-mini"
        
    # Default fallback: Fast coding models
    return "deepseek-coder"

# Usage Example:
# model_to_call = determine_model_route(
#     task_description="Implement memory compaction in KV cache",
#     total_files=3,
#     code_complexity="high"
# )
# print(f"Routed to: {model_to_call}") # Outputs: o3-mini
```

---

## ⚙️ Skema Konfigurasi Router

Konfigurasi berikut menetapkan batas-batas operasional routing pada cluster backend agen:

```yaml
# model-routing-rules.yml
routing_rules:
  - rule_id: "r-01-bulk-files"
    condition: "payload.files.length > 20"
    target_model: "anthropic/claude-3-5-sonnet-v2"
    timeout_ms: 60000
    
  - rule_id: "r-02-critical-bugs"
    condition: "payload.severity == 'critical'"
    target_model: "openai/o3-mini"
    timeout_ms: 120000
    
  - rule_id: "r-03-fast-boilerplate"
    condition: "payload.complexity == 'low'"
    target_model: "deepseek/deepseek-coder"
    timeout_ms: 30000
    fallback: "openai/gpt-4o-mini"
```

---

## ⚠️ Anti-Patterns Model Routing

* ❌ **Monolithic Model Call**: Menjalankan seluruh pipeline instruksi (dari scanning direktori hingga kompilasi) menggunakan model termahal.
* ❌ **Ignoring Failures**: Mengabaikan status limit rate API tanpa menyediakan fallback model yang lebih murah atau lokal.
* ❌ **Over-engineering simple tasks**: Merutekan tugas penamaan variabel sederhana ke model penalaran berat, yang meningkatkan latensi dan biaya operasi.
