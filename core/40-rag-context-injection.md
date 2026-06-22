# 📚 40 — RAG Context Injection

> *"Menyuntikkan konteks dokumen/codebase secara dinamis melalui RAG (Retrieval-Augmented Generation) serta memitigasi degradasi pemahaman token."*

---

## 📋 Daftar Isi
1. [Filosofi RAG dalam Operasi Agen](#-filosofi-rag-dalam-operasi-agen)
2. [Penyuntikan Konteks Dinamis (Dynamic Context Injection)](#-penyuntikan-konteks-dinamis-dynamic-context-injection)
3. [Mitigasi Degradasi Token (Token Degradation Mitigation)](#-mitigasi-degradasi-token-token-degradation-mitigation)
4. [Strategi Chunking & Reranking (Chunking & Reranking Strategy)](#-strategi-chunking--reranking-chunking--reranking-strategy)
5. [Arsitektur Pemrosesan RAG (RAG Pipeline Architecture)](#-arsitektur-pemrosesan-rag-rag-pipeline-architecture)
6. [Skema Parameter RAG (RAG Configuration Parameter Schema)](#-skema-parameter-rag-rag-configuration-parameter-schema)

---

## 🎯 Filosofi RAG dalam Operasi Agen

Meskipun model LLM modern (SOTA 2026) memiliki jendela konteks (*context window*) yang sangat besar hingga 1M-2M token, menyuntikkan seluruh isi direktori proyek atau repositori berukuran gigabyte ke dalam satu prompt adalah tindakan yang sangat tidak efisien dan mahal. Selain itu, model LLM sering kali mengalami degradasi ingatan atau kehilangan fokus di tengah-tengah teks yang sangat panjang (*Lost in the Middle phenomenon*). Agen harus secara pintar menggunakan **RAG Context Injection** untuk mencari, menapis, dan hanya menyuntikkan fragmen kode atau dokumentasi yang paling relevan dengan status tugas saat ini.

---

## 🔍 Penyuntikan Konteks Dinamis (Dynamic Context Injection)

Penyuntikan konteks dinamis bekerja dengan cara mendeteksi entitas impor kelas, dependensi berkas, dan instruksi tugas pengguna, lalu mencarinya di repositori indeks lokal.

### Langkah Aliran Dinamis:
1.  **Dependency Analysis**: Melacak pohon impor file target (misal: jika mengedit `user.service.ts`, secara otomatis memindai `user.model.ts` dan `auth.middleware.ts`).
2.  **Vector Search**: Mengambil snippet dokumentasi API eksternal yang cocok dari Vector Store.
3.  **Dynamic Pruning**: Memotong dokumen yang diambil agar tidak melebihi batas target anggaran token (*Token Budget ceiling*).

---

## 📉 Mitigasi Degradasi Token (Token Degradation Mitigation)

Untuk mencegah model kehilangan presisi pemahaman akibat memori penuh, agen menerapkan mitigasi degradasi token:

*   **Needle-in-a-Haystack Optimization**: Menempatkan informasi paling penting di baris teratas (*prefix*) dan terbawah (*suffix*) dari context prompt, menghindari peletakan informasi penting di tengah.
*   **Context Compaction**: Mengompresi snippet kode dengan menghapus komentar developer lama dan docstrings yang tidak berkontribusi pada logika program.
*   **Dynamic Cache TTL**: Memberikan label waktu kadaluwarsa (Time To Live) untuk segmen konteks sekunder di dalam KV Cache model.

---

## ✂️ Strategi Chunking & Reranking (Chunking & Reranking Strategy)

Memecah kode sumber memerlukan pendekatan sintaksis khusus (*Syntax-aware Chunking*), berbeda dengan dokumen teks biasa.

*   **Syntax Chunking**: Membagi kode berdasarkan definisi blok kelas (`class`) atau fungsi (`function`), bukan berdasarkan baris baris acak.
*   **Semantic Reranking**: Menggunakan model Cross-Encoder untuk menyortir ulang fragmen kode hasil pencarian awal berdasarkan tingkat relevansi logika, bukan sekadar kecocokan kata kunci leksikal.

### Implementasi Chunking Kode di Python:

```python
import re
from typing import List

class CodeChunker:
    def __init__(self, target_chunk_size: int = 500):
        self.target_chunk_size = target_chunk_size

    def chunk_source_code(self, code: str) -> List[str]:
        """
        Chunks code by functions and classes using regex boundaries 
        to maintain semantic completeness.
        """
        # Split by top-level functions or classes
        pattern = r"(?=\b(?:class|def|function|async\s+function|export\s+class)\b)"
        raw_chunks = re.split(pattern, code)
        
        refined_chunks = []
        current_chunk = ""

        for chunk in raw_chunks:
            if not chunk.strip():
                continue
            # If combining exceeds target size, save previous and start fresh
            if len(current_chunk) + len(chunk) > self.target_chunk_size:
                if current_chunk:
                    refined_chunks.append(current_chunk)
                current_chunk = chunk
            else:
                current_chunk += "\n" + chunk
                
        if current_chunk:
            refined_chunks.append(current_chunk)
            
        return refined_chunks
```

---

## 🗺️ Arsitektur Pemrosesan RAG (RAG Pipeline Architecture)

```
       [Raw Source Code / API Docs]
                    │
                    ▼
          [Syntax-Aware Chunker]
                    │
                    ▼
          [Vector Embeddings DB]
                    │
   [Query] ──► [Hybrid Search]
                    │
                    ▼
           [Top K Results]
                    │
                    ▼
          [Cross-Encoder Reranker]
                    │
                    ▼
     [Token Budget Pruning Manager]
                    │
                    ▼
     [Inject Reordered Context Prompt]
```

---

## 📄 Skema Parameter RAG (RAG Configuration Parameter Schema)

Skema validasi JSON untuk konfigurasi modul RAG:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RagConfiguration",
  "type": "object",
  "properties": {
    "embeddingModel": { "type": "string" },
    "chunkSize": { "type": "integer", "default": 500 },
    "overlapSize": { "type": "integer", "default": 50 },
    "similarityThreshold": { "type": "number", "default": 0.75 },
    "maxTokensToInject": { "type": "integer", "default": 4096 },
    "rerankingEnabled": { "type": "boolean" },
    "rerankerModel": { "type": "string" }
  },
  "required": ["embeddingModel", "maxTokensToInject", "rerankingEnabled"]
}
```
