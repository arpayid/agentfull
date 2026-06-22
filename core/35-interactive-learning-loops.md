# 🔄 35 — Interactive Learning Loops

> *"Pembelajaran dalam konteks (in-context reinforcement learning) secara dinamis menyesuaikan preferensi pengguna selama sesi runtime multi-turn."*

---

## 📋 Daftar Isi
1. [Filosofi Pembelajaran Interaktif Dynamic](#-filosofi-pembelajaran-interaktif-dynamic)
2. [Reinforcement Learning dalam Konteks (In-Context RL)](#-reinforcement-learning-dalam-konteks-in-context-rl)
3. [Adaptasi Preferensi Pengguna Dinamis (Dynamic User Preference Adaptation)](#-adaptasi-preferensi-pengguna-dinamis-dynamic-user-preference-adaptation)
4. [Mekanisme Umpan Balik Sesi Runtime (Runtime Session Feedback Mechanism)](#-mekanisme-umpan-balik-sesi-runtime-runtime-session-feedback-mechanism)
5. [Arsitektur Loop Umpan Balik Pengguna (User Feedback Loop Architecture)](#-arsitektur-loop-umpan-balik-pengguna-user-feedback-loop-architecture)
6. [Skema Penyimpanan Profil Preferensi (Preference Profile Storage Schema)](#-skema-penyimpanan-profil-preferensi-preference-profile-storage-schema)

---

## 🎯 Filosofi Pembelajaran Interaktif Dinamis

Sistem otonom tingkat lanjut (SOTA 2026) tidak boleh bersifat kaku atau statis. Setiap interaksi dengan pengguna (developer manusia) adalah sinyal data berharga. Melalui pembelajaran interaktif, agen menangkap koreksi eksplisit, preferensi implisit, dan gaya coding pengguna. Informasi ini kemudian digunakan untuk menyempurnakan strategi generasi berikutnya secara real-time tanpa perlu melakukan training ulang model parameter (*fine-tuning*), melainkan memanfaatkan optimasi *In-Context Learning*.

---

## 🧠 Reinforcement Learning dalam Konteks (In-Context RL)

In-Context RL menggunakan window memory agen untuk menyimpan riwayat koreksi masa lalu dalam sesi berjalan. Setiap kali pengguna menolak atau mengoreksi tindakan agen, agen memperbarui bobot perilaku internalnya (*virtual policy*) melalui manipulasi prompt instruksi kontekstual.

### Aturan In-Context RL:
1.  **Reward Positive Reinforcement**: Tindakan yang disetujui (diterima) dicatat sebagai pola sukses (*gold standard*).
2.  **Penalty Negative Reinforcement**: Tindakan yang ditolak atau dikoreksi dicatat sebagai batasan (*negative constraints*).
3.  **Dynamic Prompt Prefixing**: Menyisipkan ringkasan pembelajaran terakhir sebagai instruksi teratas pada pesan berikutnya.

---

## ⚙️ Adaptasi Preferensi Pengguna Dinamis (Dynamic User Preference Adaptation)

Agen melacak preferensi pengguna pada berbagai dimensi seperti:
*   **Verbosity**: Tingkat kedetailan penjelasan (sangat ringkas vs dokumentasi lengkap).
*   **Coding Style**: Preferensi fungsional vs berorientasi objek (OOP), penggunaan arrow function, atau library tertentu.
*   **Safety Threshold**: Keberanian memodifikasi file kritis vs meminta konfirmasi eksplisit terlebih dahulu.

### Kode Perekaman Preferensi Dinamis (Python):

```python
from typing import Dict, Any

class PreferenceTracker:
    def __init__(self):
        self.state = {
            "verbosity": "medium",
            "style": "functional",
            "confirmation_required": True,
            "error_tolerance": "strict"
        }
        self.interaction_history = []

    def log_interaction(self, action: str, feedback: str):
        """Logs user feedback and adapts properties dynamically."""
        self.interaction_history.append({"action": action, "feedback": feedback})
        
        # Analyze feedback for preference cues
        lowered_feedback = feedback.lower()
        if "don't explain" in lowered_feedback or "be concise" in lowered_feedback:
            self.state["verbosity"] = "low"
        elif "explain in detail" in lowered_feedback or "why" in lowered_feedback:
            self.state["verbosity"] = "high"
            
        if "use functional" in lowered_feedback:
            self.state["style"] = "functional"
        elif "use classes" in lowered_feedback or "oop" in lowered_feedback:
            self.state["style"] = "oop"

        if "don't ask" in lowered_feedback or "auto-approve" in lowered_feedback:
            self.state["confirmation_required"] = False
        elif "always ask" in lowered_feedback or "ask first" in lowered_feedback:
            self.state["confirmation_required"] = True

    def get_system_instruction_override(self) -> str:
        """Generates dynamic instructions for the agent based on compiled preferences."""
        return (
            f"[Preference Override]\n"
            f"- Output verbosity level: {self.state['verbosity'].upper()}\n"
            f"- Preferred coding style: {self.state['style'].upper()}\n"
            f"- Requires confirmation for modifications: {self.state['confirmation_required']}\n"
            f"- Strictness behavior: {self.state['error_tolerance'].upper()}"
        )
```

---

## 📥 Mekanisme Umpan Balik Sesi Runtime (Runtime Session Feedback Mechanism)

Selama sesi interaktif, agen mencatat data koreksi pengguna ke dalam penyimpanan sementara lokal (session cache). Data ini disarikan pada akhir setiap turn untuk menghasilkan metadata representasi preferensi.

```typescript
// TypeScript representation of runtime session feedback logger
interface FeedbackRecord {
  timestamp: string;
  turnIndex: number;
  userPrompt: string;
  agentResponse: string;
  userCorrectionType: 'ACCEPT' | 'REJECT' | 'PARTIAL_EDIT' | 'CANCELLATION';
  correctedCodeSnippet?: string;
}

export class RuntimeFeedbackLogger {
  private logs: FeedbackRecord[] = [];

  public logTurn(record: FeedbackRecord): void {
    this.logs.push(record);
    if (record.userCorrectionType === 'REJECT') {
      console.warn(`[Learning Loop] Negative feedback registered at turn ${record.turnIndex}. Adapting prompt constraints.`);
    }
  }

  public getLearningContext(): string {
    const rejections = this.logs.filter(log => log.userCorrectionType === 'REJECT');
    if (rejections.length === 0) return '';

    return rejections.map((rej, index) => 
      `Correction #${index + 1}: When presented with prompt "${rej.userPrompt}", the user rejected the output. Corrective feedback: "${rej.agentResponse}"`
    ).join('\n');
  }
}
```

---

## 🗺️ Arsitektur Loop Umpan Balik Pengguna (User Feedback Loop Architecture)

```
       [User Input Prompt]
                │
                ▼
      [LLM Agent Execution]
                │
                ▼
     [Agent Proposed Action]
                │
         ┌──────┴──────┐
         ▼             ▼
     [Accepted]    [Rejected/Corrected]
         │             │
         │             ▼
         │      [Log Failure Signal] ──► [Update Virtual Policy Cache]
         │             │                               │
         ▼             ▼                               ▼
    [Proceed]  [Apply Dynamic Rewrite] ◄── [Prefix Memory Injection]
```

---

## 📄 Skema Penyimpanan Profil Preferensi (Preference Profile Storage Schema)

Untuk memastikan persistensi preferensi lintas sesi, profil disimpan dan dibaca menggunakan format terstruktur berikut:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserPreferenceProfile",
  "type": "object",
  "properties": {
    "userId": { "type": "string" },
    "globalPreferences": {
      "type": "object",
      "properties": {
        "verbosity": { "type": "string", "enum": ["low", "medium", "high"] },
        "programmingLanguageStyle": { "type": "string" },
        "securityStrictness": { "type": "string", "enum": ["lax", "balanced", "paranoid"] }
      },
      "required": ["verbosity", "programmingLanguageStyle", "securityStrictness"]
    },
    "adaptedConstraints": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "contextTrigger": { "type": "string" },
          "resolvedConstraint": { "type": "string" }
        },
        "required": ["contextTrigger", "resolvedConstraint"]
      }
    }
  },
  "required": ["userId", "globalPreferences", "adaptedConstraints"]
}
```
