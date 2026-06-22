# 🤝 34 — Agent Consensus Debate

> *"Mengatur protokol debat resolusi multi-agen, membangun konsensus, dan menyelesaikan konflik output antara perancang kode, evaluator hakim, dan penjamin kualitas (QA)."*

---

## 📋 Daftar Isi
1. [Filosofi Konsensus Multi-Agen](#-filosofi-konsensus-multi-agen)
2. [Arsitektur Peran (Role Architecture: Code, Judge, QA)](#-arsitektur-peran-role-architecture-code-judge-qa)
3. [Protokol Resolusi Konflik & Debat (Conflict Resolution & Debate Protocol)](#-protokol-resolusi-konflik--debat-conflict-resolution--debate-protocol)
4. [Algoritma Pencapaian Konsensus (Consensus Building Algorithm)](#-algoritma-pencapaian-konsensus-consensus-building-algorithm)
5. [Diagram Alir Debat Agen (Agent Debate Flowchart)](#-diagram-alir-debat-agen-agent-debate-flowchart)
6. [Skema Pesan Protokol Konsensus (Consensus Protocol Message Schema)](#-skema-pesan-protokol-konsensus-consensus-protocol-message-schema)

---

## 🎯 Filosofi Konsensus Multi-Agen

Dalam sistem multi-agen modern (SOTA 2026), ketergantungan pada satu instansi LLM sering menimbulkan titik kegagalan tunggal (single point of failure). Untuk mencapai keandalan perangkat lunak tingkat korporat, diperlukan kerangka kerja perdebatan terstruktur. Melalui dialektika formal antara agen pengembang (*Code Generator*), agen penilai (*Judge LLM*), dan agen penguji (*QA Tester*), bias kognitif model dapat dikurangi secara signifikan dan solusi optimal dapat dikerucutkan melalui konsensus matematika.

---

## 🎭 Arsitektur Peran (Role Architecture: Code, Judge, QA)

Sistem ini membagi tanggung jawab secara ketat menjadi tiga agen otonom:

1.  **Code Agent (Coder)**: Berfokus pada kecepatan, efisiensi penulisan algoritma, keindahan sintaksis, dan kepatuhan terhadap dependensi proyek.
2.  **QA Agent (Tester)**: Berorientasi pada kegagalan. Bertugas mencari kelemahan kode, edge cases, kondisi balapan (race conditions), serta celah keamanan.
3.  **Judge Agent (Arbitrator)**: Bertindak sebagai wasit netral. Mengevaluasi argumen dari Coder dan QA, menimbang trade-off, dan memutuskan keputusan akhir berdasarkan metrics objektif.

---

## 💬 Protokol Resolusi Konflik & Debat (Conflict Resolution & Debate Protocol)

Ketika terjadi perbedaan pendapat (misalnya, Coder mengklaim fungsi sudah selesai sementara QA menemukan runtime leak), protokol debat dimulai secara otomatis.

### Aturan Debat:
*   **Putaran Terbatas**: Debat dibatasi maksimal 3 putaran untuk mencegah loop konsumsi token tak terbatas.
*   **Objektivitas Berbasis Bukti**: Setiap agen wajib menyertakan bukti nyata (seperti log stack trace, benchmark runtime, atau spesifikasi RFC) untuk mendukung argumennya.
*   **Skor Keyakinan (Confidence Score)**: Setiap agen memberikan skor keyakinan numerik (0.0 - 1.0) pada setiap argumen.

### Contoh Log Debat Dialektis:

```
[Round 1]
Coder: "Optimized memory footprint by removing caching layer. Conf Score: 0.9"
QA: "Rejection. Without cache, high-throughput mock benchmark exhibits latency spikes (>500ms). Conf Score: 0.95"
Judge: "Evaluation requested. Coder must provide alternative rate-limiter or restore selective memory-caching."
```

---

## 🧮 Algoritma Pencapaian Konsensus (Consensus Building Algorithm)

Berikut adalah implementasi Python sederhana untuk menghitung bobot konsensus dan menentukan apakah perdebatan dapat diselesaikan atau memerlukan eskalasi (HITL).

```python
from typing import List, Dict, Tuple

class ConsensusEngine:
    def __init__(self, weights: Dict[str, float]):
        # e.g., {'Coder': 0.3, 'QA': 0.4, 'Judge': 0.3}
        self.weights = weights

    def evaluate_consensus(self, votes: Dict[str, Tuple[bool, float]]) -> Tuple[bool, float]:
        """
        Evaluates agent votes. 
        votes: key=agent_role, value=(vote_approve_boolean, confidence_score)
        Returns: (is_consensus_reached, weighted_score)
        """
        weighted_sum = 0.0
        total_weight = sum(self.weights.values())

        for role, (vote, confidence) in votes.items():
            role_weight = self.weights.get(role, 0.0)
            # If vote is True (approve), positive contribution. If False, negative.
            vote_value = 1.0 if vote else -1.0
            weighted_sum += vote_value * confidence * role_weight

        # Normalize score between -1.0 and 1.0
        normalized_score = weighted_sum / total_weight
        
        # Consensus threshold is set to > 0.4 for approval, < -0.4 for rejection.
        # Values close to 0.0 indicate deadlock.
        if normalized_score > 0.4:
            return True, normalized_score  # Approved
        elif normalized_score < -0.4:
            return False, normalized_score # Rejected
        else:
            # Deadlock: require escalation
            return False, normalized_score
```

---

## 🗺️ Diagram Alir Debat Agen (Agent Debate Flowchart)

```
      [Code Agent Drafts Code]
                  │
                  ▼
         [QA Runs Test Suite]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
    [Passed]             [Failed]
        │                   │
        │                   ▼
        │          [Initiate Debate Loop]
        │                   │
        │                   ▼
        │          [Coder vs QA Debate]
        │                   │
        │                   ▼
        │          [Judge Evaluates]
        │                   │
        │         ┌─────────┴─────────┐
        │         ▼                   ▼
        │    [Consensus Reached]   [Deadlock]
        │         │                   │
        │         ├───────────────────┼──────────┐
        │         ▼                   ▼          ▼
[Merge/Deploy] [Re-code Loop] [HITL Escalation] [Fail Pipeline]
```

---

## 📄 Skema Pesan Protokol Konsensus (Consensus Protocol Message Schema)

Untuk memfasilitasi komunikasi antar-agen, pertukaran pesan harus mengikuti struktur skema yang divalidasi berikut:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DebateMessage",
  "type": "object",
  "properties": {
    "debateId": { "type": "string", "format": "uuid" },
    "round": { "type": "integer", "minimum": 1, "maximum": 5 },
    "sender": { "type": "string", "enum": ["CODER", "QA", "JUDGE"] },
    "vote": { "type": "boolean" },
    "confidenceScore": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "arguments": {
      "type": "array",
      "items": { "type": "string" }
    },
    "evidencePaths": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["debateId", "round", "sender", "vote", "confidenceScore", "arguments"]
}
```
