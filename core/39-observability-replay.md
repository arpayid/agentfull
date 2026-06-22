# 📜 39 — Observability & Replay

> *"Menyimpan jejak eksekusi jangka panjang, menganalisis replay, dan melakukan audit pemutaran ulang (playback audits) dari lintasan masa lalu."*

---

## 📋 Daftar Isi
1. [Filosofi Observabilitas & Replay](#-filosofi-observabilitas--replay)
2. [Penyimpanan Trace Eksekusi Jangka Panjang (Long-Term Trace Storage)](#-penyimpanan-trace-eksekusi-jangka-panjang-long-term-trace-storage)
3. [Analisis Pemutaran Ulang (Replay Analytics)](#-analisis-pemutaran-ulang-replay-analytics)
4. [Audit Lintasan Agen (Playback Audits of Agent Trajectories)](#-audit-lintasan-agen-playback-audits-of-agent-trajectories)
5. [Arsitektur Perekaman Observabilitas (Observability Recorder Architecture)](#-arsitektur-perekaman-observabilitas-observability-recorder-architecture)
6. [Skema Dokumen Trace Eksekusi (Execution Trace Document Schema)](#-skema-dokumen-trace-eksekusi-execution-trace-document-schema)

---

## 🎯 Filosofi Observabilitas & Replay

Sistem otonom yang dapat dipercaya (SOTA 2026) harus sepenuhnya dapat diaudit. Ketika agen mengambil keputusan di luar dugaan, developer manusia harus dapat merekonstruksi setiap pemanggilan API, pembacaan file, modifikasi lingkungan, dan status mental internal agen (*metacognition step*). Melalui **Observability & Replay**, setiap sesi eksekusi disimpan sebagai rangkaian peristiwa temporal (*immutable time-series events*) yang dapat "diputar ulang" langkah demi langkah untuk debugging forensik.

---

## 💾 Penyimpanan Trace Eksekusi Jangka Panjang (Long-Term Trace Storage)

Trace eksekusi tidak boleh disimpan di memori volatile yang akan hilang setelah runtime selesai. Setiap aksi, input LLM, output LLM, dan status workspace harus dicatat ke dalam database append-only seperti SQLite atau PostgreSQL untuk kebutuhan jangka panjang.

### Skema Perekam Trace (Python):

```python
import json
import sqlite3
from typing import Dict, Any

class TraceRecorder:
    def __init__(self, db_path: str = "agent_traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS traces (
                    trace_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    timestamp TEXT,
                    agent_state TEXT,
                    action_taken TEXT,
                    observation TEXT
                )
            """)

    def record_step(self, trace_id: str, session_id: str, timestamp: str, state: Dict[str, Any], action: Dict[str, Any], observation: str):
        with self.conn:
            self.conn.execute(
                "INSERT INTO traces VALUES (?, ?, ?, ?, ?, ?)",
                (
                    trace_id,
                    session_id,
                    timestamp,
                    json.dumps(state),
                    json.dumps(action),
                    observation
                )
            )
            
    def close(self):
        self.conn.close()
```

---

## 📊 Analisis Pemutaran Ulang (Replay Analytics)

Dengan menganalisis lintasan (*trajectory*) yang tersimpan, mesin analitik dapat mendeteksi pola inefisiensi seperti:
*   **Action Loops**: Agen berulang kali memanggil perintah `ls` atau `cat` yang sama tanpa progres nyata.
*   **Stuck Subprocesses**: Proses background yang menggantung tanpa henti.
*   **Degrading Performance**: Penurunan rasio sukses tindakan seiring bertambahnya ukuran file kerja.

```typescript
// Analisis data replay di Node.js
interface TrajectoryStep {
  step: number;
  actionName: string;
  durationMs: number;
}

export function detectActionLoops(steps: TrajectoryStep[]): boolean {
  const windowSize = 3;
  if (steps.length < windowSize * 2) return false;

  for (let i = 0; i <= steps.length - (windowSize * 2); i++) {
    const pattern = steps.slice(i, i + windowSize).map(s => s.actionName).join(',');
    const comparison = steps.slice(i + windowSize, i + (windowSize * 2)).map(s => s.actionName).join(',');
    
    if (pattern === comparison) {
      console.warn(`[Replay Analytics] Infinite action loop detected pattern: "${pattern}"`);
      return true; // Redundant loop detected
    }
  }
  return false;
}
```

---

## 🔍 Audit Lintasan Agen (Playback Audits of Agent Trajectories)

Audit pemutaran ulang (playback audit) digunakan oleh tim QA dan administrator kepatuhan. Melalui visualisasi timeline langkah demi langkah, auditor dapat menghentikan, meninjau, dan mengubah parameter pada state historis tertentu untuk melihat bagaimana respon agen terhadap alternatif skenario (*what-if simulation*).

---

## 🗺️ Arsitektur Perekaman Observabilitas (Observability Recorder Architecture)

```
[Agent Execution Loop]
         │
         ├──► [State Snapshot Engine] ──┐
         │                              │
         ├──► [Action Logger] ──────────┼──► [Trace Recorder Service]
         │                              │               │
         └──► [Tool Outputs Capture] ───┘               ▼
                                            [Immutable SQLite DB Store]
                                                        │
                                                        ▼
                                            [Replay Analytics Engine]
                                                        │
                                       ┌────────────────┴────────────────┐
                                       ▼                                 ▼
                             [No Anomalies Found]              [Action Loops Found]
                                       │                                 │
                                       ▼                                 ▼
                               [Archive Session]               [Generate Correction]
```

---

## 📄 Skema Dokumen Trace Eksekusi (Execution Trace Document Schema)

Skema validasi JSON untuk format rekaman event trace:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentExecutionTrace",
  "type": "object",
  "properties": {
    "traceId": { "type": "string", "format": "uuid" },
    "sessionId": { "type": "string", "format": "uuid" },
    "stepNumber": { "type": "integer" },
    "executionTimestamp": { "type": "string", "format": "date-time" },
    "agentMentalState": {
      "type": "object",
      "properties": {
        "currentObjective": { "type": "string" },
        "confidenceScore": { "type": "number" },
        "assumptions": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["currentObjective", "confidenceScore"]
    },
    "actionExecuted": {
      "type": "object",
      "properties": {
        "tool": { "type": "string" },
        "arguments": { "type": "object" },
        "executionDurationMs": { "type": "integer" }
      },
      "required": ["tool", "arguments"]
    },
    "environmentObservation": { "type": "string" }
  },
  "required": ["traceId", "sessionId", "stepNumber", "executionTimestamp", "agentMentalState", "actionExecuted"]
}
```
