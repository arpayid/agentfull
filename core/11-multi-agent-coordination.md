# 🔀 11 — Multi-Agent Coordination & Delegation

> *"Ketika satu agen tidak cukup, kekuatan orkestrasi paralel memisahkan agen biasa dari sistem agen elit."*

---

## 📋 Daftar Isi

1. [Filosofi Multi-Agent](#-filosofi-multi-agent)
2. [Arsitektur Aliran Kerja Orkestrasi (Orchestration Workflow Architecture)](#-arsitektur-aliran-kerja-orkestrasi-orchestration-workflow-architecture)
3. [Delegasi Tugas & Pemisahan Scope (Task Delegation & Scope Separation)](#-delegasi-tugas--pemisahan-scope-task-delegation--scope-separation)
4. [Protokol Handoff Konteks Dinamis (Context Handoff Protocol)](#-protokol-handoff-konteks-dinamis-context-handoff-protocol)
5. [Skema Pertukaran Data JSON-RPC (Data Exchange Schema)](#-skema-pertukaran-data-json-rpc-data-exchange-schema)
6. [Implementasi Kode Orkestrator (Orchestrator Code Fragment)](#-implementasi-kode-orkestrator-orchestrator-code-fragment)
7. [Menggabungkan Hasil (Aggregation & Verification)](#-menggabungkan-hasil-aggregation--verification)
8. [Anti-Patterns Koordinasi](#-anti-patterns-koordinasi)

---

## 🎯 Filosofi Multi-Agent

Pada tugas skala besar, membagi pekerjaan ke beberapa sub-agent (spesialis) secara paralel menghemat waktu dan meningkatkan akurasi. Agen utama bertindak sebagai **Orchestrator** yang mengarahkan sub-agent, memantau kemajuan, dan melakukan sintesis akhir terhadap hasil kerja mereka.

---

## 🏗️ Arsitektur Aliran Kerja Orkestrasi

Berikut adalah visualisasi alur koordinasi dari main orchestrator ke sub-agent terspesialisasi:

```
                  ┌──────────────────────────┐
                  │ Main Orchestrator Agent  │
                  └──────────┬───┬───┬───────┘
                             │   │   │
          ┌──────────────────┘   │   └──────────────────┐
          ▼ Task 1               ▼ Task 2               ▼ Task 3
   ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
   │ Researcher   │       │ Implementer  │       │ QA Verifier  │
   │ Sub-Agent    │       │ Sub-Agent    │       │ Sub-Agent    │
   └──────┬───────┘       └──────┬───────┘       └──────┬───────┘
          │                      │                      │
          └─────────────────┐    │    ┌─────────────────┘
                            ▼    ▼    ▼
                  ┌──────────────────────────┐
                  │ Aggregator & Synthesizer │
                  └──────────────────────────┘
```

---

## 📋 Delegasi Tugas & Pemisahan Scope

Setiap sub-agent harus memiliki tugas yang terdefinisi dengan sangat spesifik untuk menghindari tumpang tindih pengerjaan dan pertikaian state file.

### Pembagian Peran Klasik:
* **Orchestrator (Main Agent)**: Merencanakan, membagi tugas, memvalidasi hasil akhir, dan berkomunikasi dengan pengguna.
* **Researcher/Explorer Sub-Agent**: Melakukan pencarian kode, membaca dokumentasi, dan memetakan struktur file.
* **Implementer Sub-Agent**: Menulis kode baru, melakukan refactoring, dan menulis tes.
* **Reviewer/Verifier Sub-Agent**: Menjalankan tes, memeriksa kualitas kode, dan melakukan linter check.

| Peran Agen | Target Output | Batasan Lingkup (Constraint) |
| :--- | :--- | :--- |
| `Orchestrator` | Final PR & User Report | Dilarang menulis/edit file secara langsung |
| `Researcher` | JSON file-map & search results | Read-only access ke workspace |
| `Implementer` | Modified source files & tests | Hanya mengedit modul target yang ditentukan |
| `Verifier` | Linter logs & Test suite output | Dilarang memodifikasi file fungsional |

---

## 🔄 Protokol Handoff Konteks Dinamis

Saat meluncurkan sub-agent, berikan instruksi yang jelas:
1. **Tujuan Konkret**: Apa output yang diharapkan (misal: "Kembalikan list path file yang menggunakan library X").
2. **Konteks Terbatas**: Jangan kirim seluruh riwayat chat jika tidak diperlukan. Hanya berikan potongan kode atau file yang relevan.
3. **Format Output**: Minta sub-agent mengembalikan format terstruktur (JSON atau Markdown ringkas).

---

## ⚙️ Skema Pertukaran Data JSON-RPC

Komunikasi antar agen harus terstruktur menggunakan format pertukaran data yang formal. Berikut adalah contoh payload request untuk mendelegasikan tugas analisis ke sub-agent:

```json
{
  "jsonrpc": "2.0",
  "method": "delegateTask",
  "params": {
    "sub_agent_role": "verifier",
    "task_id": "t-8812-lint",
    "context": {
      "target_directory": "/workspace/src/auth",
      "modified_files": [
        "src/auth/service.ts",
        "src/auth/controller.ts"
      ],
      "check_rules": ["no-explicit-any", "security-boundaries"]
    },
    "max_tokens_budget": 50000
  },
  "id": 102
}
```

---

## 💻 Implementasi Kode Orkestrator

Berikut adalah implementasi Python sederhana untuk mendelegasikan tugas ke sub-agent secara terstruktur:

```python
import json
import asyncio

class MultiAgentOrchestrator:
    def __init__(self, agent_endpoints):
        self.endpoints = agent_endpoints

    async def dispatch_task(self, sub_agent: str, payload: dict) -> dict:
        print(f"[Orchestrator] Dispatching task to {sub_agent}...")
        # Simulating HTTP / RPC call to the sub-agent service
        await asyncio.sleep(1.0) 
        
        response_payload = {
            "status": "success",
            "agent": sub_agent,
            "output": f"Executed {payload['method']} successfully.",
            "changes_applied": []
        }
        return response_payload

    async def execute_workflow(self):
        research_task = {
            "method": "analyze_dependencies",
            "path": "/src/core"
        }
        # Run research first
        research_result = await self.dispatch_task("researcher", research_task)
        
        # Then compile implementer task
        implementer_task = {
            "method": "apply_refactoring",
            "findings": research_result["output"]
        }
        await self.dispatch_task("implementer", implementer_task)

# Usage
# orchestrator = MultiAgentOrchestrator({"researcher": "http://localhost:8001"})
# asyncio.run(orchestrator.execute_workflow())
```

---

## ⚠️ Anti-Patterns Koordinasi

* ❌ **Redundant Operations**: Agen utama dan sub-agent melakukan pencarian file yang sama berulang kali.
* ❌ **Context Spamming**: Mengirimkan seluruh codebase ke sub-agent sehingga menghabiskan kuota token.
* ❌ **No Verification**: Langsung mempercayai kode dari sub-agent tanpa melakukan verifikasi kompilasi atau tes lokal terlebih dahulu.
* ❌ **Circular Delegation**: Sub-agent mendelegasikan kembali tugas ke sub-agent lain tanpa pengawasan orkestrator, menyebabkan loop delegasi tanpa akhir.
