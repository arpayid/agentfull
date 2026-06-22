# 🧠 15 — Meta-Prompting & Self-Correction Loop

> *"Sebuah sistem cerdas tidak hanya memperbaiki kodenya, ia juga memperbaiki cara ia menerima instruksi."*

---

## 📋 Daftar Isi

1. [Filosofi Meta-Prompting](#-filosofi-meta-prompting)
2. [Arsitektur Lingkaran Koreksi Diri (Self-Correction Loop Architecture)](#-arsitektur-lingkaran-koreksi-diri-self-correction-loop-architecture)
3. [Evaluasi Prompt Dinamis (Dynamic Prompt Evaluation)](#-evaluasi-prompt-dinamis-dynamic-prompt-evaluation)
4. [Skema Optimasi Prompt (Prompt Optimization Template)](#-skema-optimasi-prompt-prompt-optimization-template)
5. [Implementasi Kode Pemotong Konteks (Context Pruner Script)](#-implementasi-kode-pemotong-konteks-context-pruner-script)
6. [Panduan Optimasi Konteks (Context Optimization Guidelines)](#-panduan-optimasi-konteks-context-optimization-guidelines)
7. [Anti-Patterns Meta-Prompting](#-anti-patterns-meta-prompting)

---

## 🎯 Filosofi Meta-Prompting

Meta-Prompting adalah proses di mana agen **menganalisis prompt atau instruksi internalnya sendiri** untuk melihat apakah ada instruksi yang ambigu atau kontradiktif, kemudian melakukan pembaruan struktur berpikir secara real-time. Hal ini memastikan agen tidak terjebak dalam bias interpretasi instruksi.

---

## 🔄 Arsitektur Lingkaran Koreksi Diri

Jika instruksi yang dijalankan memicu hasil yang kurang memuaskan, jalankan alur pemangkasan dan penyempurnaan instruksi berikut:

```
┌──────────────────────────────────────┐
│  Analisis Hasil Kerja                │
└──────────────────┬───────────────────┘
                   │
┌──────────────────┴───────────────────┐
│  Apakah instruksi awal terlalu luas? │
└──────────────────┬───────────────────┘
                   │
        [YA] ──────┴─────── [TIDAK]
         │                     │
┌────────┴──────────┐   ┌──────┴───────────┐
│ Rancang Ulang     │   │ Lanjutkan        │
│ Sub-instruksi     │   │ Proses           │
│ Lebih Spesifik    │   └──────────────────┘
└───────────────────┘
```

---

## 📋 Evaluasi Prompt Dinamis

Untuk menentukan apakah instruksi internal memerlukan modifikasi (meta-refactoring), agen mengevaluasi parameter-parameter berikut:

| Parameter Evaluasi | Indikator Kegagalan | Tindakan Korektif (Meta-Prompt) |
| :--- | :--- | :--- |
| **Kekonkretan (Concreteness)** | Agen berasumsi liar tanpa basis file. | Tambahkan instruksi: *"Dilarang berasumsi sebelum membaca path."* |
| **Kepadatan Konteks** | Model mengabaikan batasan token. | Pangkas log chat lama dan ringkas pesan error. |
| **Kemenduaan (Ambiguity)** | Model memilih dua opsi bertentangan. | Berikan prioritas aturan secara eksplisit (e.g. Rule 1 > Rule 2). |

---

## 📝 Skema Optimasi Prompt

Berikut adalah contoh metaprompt yang dikirimkan ke model penalaran tingkat tinggi untuk menyaring instruksi yang rusak:

```markdown
### 🧠 METAPROMPT: SYSTEM INSTRUCTION REFINEMENT

Tugas Anda adalah menganalisis dan menyempurnaan System Prompt berikut karena terbukti menghasilkan loop kegagalan.

**System Prompt Lama:**
"Anda adalah agen pemrograman. Cari file yang rusak di dalam direktori dan perbaiki secara langsung."

**Error Output yang Terjadi:**
"Bash tool returned timeout. File '/src/index.js' could not be written."

**System Prompt Baru (Telah Disempurnakan):**
1. Anda adalah agen pemrograman yang bertindak secara aman.
2. Sebelum mengedit file, jalankan 'read' pada file target untuk memverifikasi isinya.
3. Batasi pencarian direktori maksimal 3 level.
4. Jika terjadi error penulisan, laporkan langsung ke pengguna daripada mencoba menulis ulang secara terus menerus.
```

---

## 💻 Implementasi Kode Pemotong Konteks

Skrip Python berikut menunjukkan cara agen memotong riwayat pesan (history pruning) ketika panjang token melampaui batas toleransi input model:

```python
def prune_conversation_context(messages: list, max_token_limit: int) -> list:
    """
    Prunes the middle of the conversation history while keeping the system prompt
    and the latest 3 interactions to preserve context.
    """
    if len(messages) <= 5:
        return messages
        
    system_prompt = messages[0] if messages[0]["role"] == "system" else None
    latest_messages = messages[-4:] # Keep the latest user instructions and agent responses
    
    pruned_history = []
    if system_prompt:
        pruned_history.append(system_prompt)
        
    pruned_history.append({
        "role": "system",
        "content": "[SYSTEM WARNING: Older history pruned to prevent context overflow and token bloat.]"
    })
    
    pruned_history.extend(latest_messages)
    return pruned_history

# Usage Example:
# messages = [{"role": "system", "content": "You are a helpful agent."}, ...]
# messages = prune_conversation_context(messages, 20000)
```

---

## 📋 Panduan Optimasi Konteks

* **Pruning Redundansi**: Buang instruksi yang tidak lagi relevan dengan kondisi codebase saat ini.
* **Prioritisasi Constraints**: Letakkan aturan keamanan dan batas eksekusi di bagian paling atas tumpukan instruksi (system instruction).
* **Format Terstruktur**: Selalu gunakan format XML atau JSON untuk membedakan instruksi sistem, state memori, dan data masukan pengguna.

---

## ⚠️ Anti-Patterns Meta-Prompting

* ❌ **Static Prompts**: Menggunakan satu system prompt kaku untuk seluruh fase pekerjaan (desain, implementasi, verifikasi) tanpa adaptasi konteks.
* ❌ **Context Flooding**: Mengirim ulang data log error mentah setebal ratusan baris ke prompt baru tanpa melakukan penyaringan kata kunci terlebih dahulu.
* ❌ **Ambiguous Contradiction**: Memasukkan aturan baru yang bertentangan dengan aturan yang ada tanpa menghapus instruksi lama yang tidak kompatibel.
