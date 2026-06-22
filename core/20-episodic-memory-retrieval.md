# 🧠 20 — Episodic Memory Retrieval & Persistent State Sync

> *"Sebuah agen tidak boleh mengulang kesalahan yang sama hanya karena ia berada di sesi percakapan baru."*

---

## 📋 Daftar Isi

1. [Filosofi Memori Episodik](#-filosofi-memori-episodik)
2. [Arsitektur Sinkronisasi Memori (Memory Sync Architecture)](#-arsitektur-sinkronisasi-memori-memory-sync-architecture)
3. [Format Penyimpanan Ringkasan Episodik (Episodic Summary Format)](#-format-penyimpanan-ringkasan-episodik-episodic-summary-format)
4. [Skema Penyimpanan Vektor (Vector Storage Schema)](#-skema-penyimpanan-vektor-vector-storage-schema)
5. [Implementasi Kode Pengambilan Memori (Memory Retrieval Script)](#-implementasi-kode-pengambilan-memori-memory-retrieval-script)
6. [Mekanisme Retrieval Memori (Memory Retrieval Mechanisms)](#-mekanisme-retrieval-memori-memory-retrieval-mechanisms)
7. [Anti-Patterns Memori Episodik](#-anti-patterns-memori-episodik)

---

## 🎯 Filosofi Memori Episodik

Episodic Memory Retrieval adalah **sistem retensi informasi lintas sesi**. Saat sesi chat dimulai, agen secara dinamis mencari memori dari sesi sebelumnya terkait file konfigurasi, kegagalan compiler masa lalu, atau trade-off desain yang disepakati pengguna sebelumnya. Hal ini mencegah agen mengulangi proses pencarian (discovery) yang tidak perlu di setiap pergantian percakapan.

---

## 🏗️ Arsitektur Sinkronisasi Memori

Proses penarikan memori terintegrasi ke dalam inisialisasi context window:

```
Sesi Baru Dimulai ──► Ambil Konteks Sesi Terakhir ──► Embedding Match via Vector DB
                                                           │
                                                           ▼
                                               Suntikkan Temuan Penting 
                                               ke Immediate Context (Modul 06)
```

---

## 📝 Format Penyimpanan Ringkasan Episodik

Di akhir setiap sesi kerja, simpan file metadata memori terkompresi di folder `.agentfull/memory/`:

```json
{
  "session_id": "8bb63-agy",
  "knowledge_cutoff": "2026-06-22",
  "conventions_discovered": [
    "Project menggunakan space indentation (2 spaces)",
    "Linting ketat di typescript mewajibkan explicitly return types"
  ],
  "trapped_errors": [
    "Port 8080 dikunci oleh container docker lama, gunakan 8081"
  ],
  "associated_files": [
    "src/auth/service.ts",
    "package.json"
  ]
}
```

---

## 📊 Skema Penyimpanan Vektor

Gunakan representasi metadata berikut untuk mengindeks ringkasan sesi ke dalam database vektor seperti Chroma atau Pinecone:

| Key Metadata | Tipe Data | Deskripsi Fungsi |
| :--- | :--- | :--- |
| `project_name` | `string` | Membedakan memori antar proyek workspace yang berbeda. |
| `error_hash` | `string` | Mengidentifikasi kecocokan log error compiler spesifik. |
| `timestamp` | `integer` | Memberikan bobot relevansi waktu (recency bias) saat pencarian. |

---

## 💻 Implementasi Kode Pengambilan Memori

Skrip Python berikut menunjukkan cara agen menghitung cosine similarity secara lokal untuk mengambil memori episodic yang paling relevan dengan masalah saat ini:

```python
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

class LocalEpisodicMemory:
    def __init__(self):
        # Sample cached memories with mock 3-dimensional embeddings
        self.database = [
            {"summary": "Port 8080 is locked by old docker process", "embedding": [0.91, 0.12, 0.05]},
            {"summary": "Use tabs for indents in golang files", "embedding": [0.10, 0.88, 0.22]},
            {"summary": "Config key requires API prefix sk-", "embedding": [0.03, 0.11, 0.95]}
        ]

    def query_memory(self, query_embedding, threshold=0.7):
        results = []
        for mem in self.database:
            sim = cosine_similarity(query_embedding, mem["embedding"])
            if sim >= threshold:
                results.append((sim, mem["summary"]))
        # Sort by similarity descending
        results.sort(reverse=True, key=lambda x: x[0])
        return results

# Usage Example:
# memory_db = LocalEpisodicMemory()
# matched = memory_db.query_memory([0.88, 0.15, 0.08])
# print(matched) # Outputs matched memories related to Port 8080 lock
```

---

## ⚙️ Mekanisme Retrieval Memori

1. **Inisialisasi**: Saat start-up, baca file `.agentfull/memory/sessions.index`.
2. **Kueri Teks**: Kirim deskripsi tugas pengguna saat ini ke generator embedding lokal.
3. **Penyuntikan Konteks**: Ambil 2 memori dengan skor kecocokan tertinggi dan letakkan di header system prompt sebagai referensi pembelajaran masa lalu.

---

## ⚠️ Anti-Patterns Memori Episodik

* ❌ **Context Flooding**: Menyuntikkan seluruh ringkasan log sesi masa lalu tanpa filter skor kecocokan ke dalam working memory.
* ❌ **Ignoring File System Reality**: Memercayai data memori lama tanpa memverifikasi apakah berkas target masih ada di dalam direktori kerja saat ini.
* ❌ **Stale Cache**: Menyimpan rahasia sensitif (tokens/passwords) di dalam database embedding vektor yang tidak aman secara persisten.
