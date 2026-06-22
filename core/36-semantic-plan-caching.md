# 🗄️ 36 — Semantic Plan Caching

> *"Mengoptimalkan penggunaan token dan kecepatan respon melalui penggunaan kembali rencana semantik (semantic plan reusability) menggunakan pencarian Vector DB."*

---

## 📋 Daftar Isi
1. [Filosofi Caching Rencana Semantik](#-filosofi-caching-rencana-semantik)
2. [Pencarian Kemiripan Semantik (Semantic Similarity Search)](#-pencarian-kemiripan-semantik-semantic-similarity-search)
3. [Arsitektur Integrasi Vector DB (Vector DB Integration Architecture)](#-arsitektur-integrasi-vector-db-vector-db-integration-architecture)
4. [Optimasi Biaya Token & Latensi (Token Cost & Latency Optimization)](#-optimasi-biaya-token--latensi-token-cost--latency-optimization)
5. [Skema Penyimpanan Cache Semantik (Semantic Cache Storage Schema)](#-skema-penyimpanan-cache-semantik-semantic-cache-storage-schema)
6. [Implementasi Layanan Cache Semantik (Semantic Cache Service Implementation)](#-implementasi-layanan-cache-semantik-semantic-cache-service-implementation)

---

## 🎯 Filosofi Caching Rencana Semantik

Dalam eksekusi agen skala besar (SOTA 2026), memformulasikan rencana pemecahan masalah (*planning loop*) dari awal untuk setiap instruksi pengguna sangat memboroskan token dan meningkatkan latensi secara signifikan. Caching tradisional berbasis kunci string persis (*exact key-value*) sering gagal karena bahasa alami memiliki banyak variasi. Dengan memanfaatkan **Semantic Plan Caching**, agen membandingkan representasi vektor (embeddings) dari instruksi saat ini dengan instruksi yang sudah diselesaikan sebelumnya, menggunakan kembali rencana eksekusi yang sukses jika berada di atas ambang batas kemiripan (*similarity threshold*).

---

## 🧠 Pencarian Kemiripan Semantik (Semantic Similarity Search)

Kemiripan semantik dihitung menggunakan cosine similarity antara vektor embedding dari kueri saat ini dengan vektor kueri historis.

$$\text{Similarity} = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$$

Jika nilai similarity $> 0.88$ (tergantung tuning model), rencana eksekusi yang tersimpan dapat langsung diambil (*re-used*) dengan menyesuaikan parameter variabel dinamis (seperti nama berkas, path, atau nama modul).

---

## 🗺️ Arsitektur Integrasi Vector DB (Vector DB Integration Architecture)

```
        [User Query]
             │
             ▼
   [Generate Embeddings]
             │
             ▼
    [Query Vector DB] ──(Similarity > 0.88?)──► [Retrieve Cached Plan] ──► [Parameter Binder] ──► [Execute Plan]
             │                                                                                          ▲
             └───────────(No / Similarity < 0.88)──► [Run Full Planner] ──► [Store Plan in Vector DB] ──┘
```

---

## 💸 Optimasi Biaya Token & Latensi (Token Cost & Latency Optimization)

*   **Pengurangan Token Input**: Melewati langkah dekomposisi masalah (*chain-of-thought planning*) yang biasanya memakan 1000 - 3000 token per prompt.
*   **Akselerasi Latensi**: Pengambilan cache dari Vector DB lokal (seperti Qdrant atau Milvus) memakan waktu $< 15\text{ms}$, jauh lebih cepat dibandingkan memanggil LLM planner yang memakan waktu $3 - 8\text{ detik}$.
*   **Perlindungan Rate-Limit**: Membantu agen mempertahankan operasi otonom dalam kuota API yang ketat tanpa terkena *429 Too Many Requests*.

---

## 📄 Skema Penyimpanan Cache Semantik (Semantic Cache Storage Schema)

Skema JSON untuk dokumen metadata rencana semantik yang disimpan di database:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SemanticPlanCacheRecord",
  "type": "object",
  "properties": {
    "planId": { "type": "string", "format": "uuid" },
    "originalQuery": { "type": "string" },
    "embeddingVector": {
      "type": "array",
      "items": { "type": "number" }
    },
    "executionSteps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "stepIndex": { "type": "integer" },
          "toolName": { "type": "string" },
          "parameterTemplates": { "type": "object" },
          "expectedOutputFormat": { "type": "string" }
        },
        "required": ["stepIndex", "toolName", "parameterTemplates"]
      }
    },
    "averageSuccessRate": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "tokenCostSaved": { "type": "integer" }
  },
  "required": ["planId", "originalQuery", "embeddingVector", "executionSteps"]
}
```

---

## ⚙️ Implementasi Layanan Cache Semantik (Semantic Cache Service Implementation)

Berikut adalah implementasi TypeScript untuk berinteraksi dengan Vector Database client fiktif guna menyimpan dan mengambil rencana semantik:

```typescript
import { VectorDbClient, EmbeddingService } from './services-mock';

interface PlanStep {
  stepIndex: number;
  toolName: string;
  parameterTemplates: Record<string, string>;
}

interface PlanCachePayload {
  planId: string;
  originalQuery: string;
  executionSteps: PlanStep[];
}

export class SemanticCacheService {
  private vectorDb: VectorDbClient;
  private embedder: EmbeddingService;
  private similarityThreshold: number = 0.88;

  constructor(vectorDb: VectorDbClient, embedder: EmbeddingService) {
    self.vectorDb = vectorDb;
    self.embedder = embedder;
  }

  public async getCachedPlan(query: string): Promise<PlanCachePayload | null> {
    const queryVector = await self.embedder.generate(query);
    const searchResult = await self.vectorDb.searchNearest(queryVector, 1);

    if (searchResult.length > 0) {
      const match = searchResult[0];
      if (match.score >= self.similarityThreshold) {
        console.log(`[Semantic Cache] Cache hit! Similarity score: ${match.score}. Reusing plan.`);
        return match.metadata as PlanCachePayload;
      }
    }
    console.log('[Semantic Cache] Cache miss. Initiating planner module.');
    return null;
  }

  public async savePlan(query: string, payload: PlanCachePayload): Promise<void> {
    const vector = await self.embedder.generate(query);
    await self.vectorDb.insert({
      id: payload.planId,
      vector: vector,
      metadata: payload
    });
    console.log(`[Semantic Cache] Plan saved under ID: ${payload.planId}`);
  }
}
```
