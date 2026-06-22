# 🔀 29 — Graph-based Associative Memory

> *"Menghubungkan potongan memori ke dalam relasi modular demi penalaran kontekstual yang lebih kaya."*

---

## 📋 Daftar Isi

1. [Filosofi Memori Asosiatif](#-filosofi-memori-asosiatif)
2. [Arsitektur Database Graf Memori (Graph Memory Architecture)](#-arsitektur-database-graf-memori-graph-memory-architecture)
3. [Aliran Navigasi Asosiatif (Associative Navigation Flow)](#-aliran-navigasi-asosiatif-associative-navigation-flow)
4. [Tabel Definisi Node dan Hubungan (Graph Schema Matrix)](#-tabel-definisi-node-dan-hubungan-graph-schema-matrix)
5. [Skema Payload Query Graph (JSON Graph Query Payload)](#-skema-payload-query-graph-json-graph-query-payload)
6. [Implementasi Kode Graf Lokal (Local Dependency Graph Python Fragment)](#-implementasi-kode-graf-lokal-local-dependency-graph-python-fragment)
7. [Pola Pengambilan Data (Data Retrieval Patterns)](#-pola-pengambilan-data-data-retrieval-patterns)
8. [Anti-Patterns Memori Asosiatif](#-anti-patterns-memori-asosiatif)

---

## 🎯 Filosofi Memori Asosiatif

Graph-based Associative Memory adalah **metode penyimpanan memori agen menggunakan skema graf**. Berbeda dengan basis data vektor yang murni mencari kemiripan teks (cosine similarity), graf memetakan hubungan ketergantungan antar modul logika (misal: "Mengubah `auth.service.ts` $\rightarrow$ berdampak pada `auth.controller.ts` dan tabel `sessions`"). Ini membantu agen memprediksi dampak perubahan kode secara holistik.

---

## 🏗️ Arsitektur Database Graf Memori

Relasi dependensi dan asosiasi logika dipetakan sebagai node dan edge:

```
          ┌────────────────┐
          │ auth.service   │
          └───────┬────────┘
             rel: modify_impacts
                   ▼
          ┌────────────────┐         rel: schema_depends       ┌──────────────┐
          │ auth.controller│ ────────────────────────────────► │ sessions tab │
          └────────────────┘                                   └──────────────┘
```

---

## 🔄 Aliran Navigasi Asosiatif

```
Input File Modifikasi ──► Cari Node Terkait ──► Tarik Node Tetangga (Neighbour nodes)
                                                      │
                                                      ▼
                                          Sertakan Dependensi ke 
                                          Context Window Uji Coba
```

---

## 📊 Tabel Definisi Node dan Hubungan

Agen menggunakan taksonomi berikut untuk memetakan keterkaitan kode:

| Jenis Hubungan (Edge) | Tipe Node Asal | Tipe Node Tujuan | Deskripsi Relasi |
| :--- | :--- | :--- | :--- |
| `imports` | File Kode (`.ts`) | File Pustaka (`npm`) | Modul memuat pustaka eksternal. |
| `modifies` | Tindakan Agen | File Kode (`.ts`) | Aktivitas penulisan file oleh agen. |
| `triggers_test` | File Kode (`.ts`) | File Uji (`.test.ts`) | Perubahan kode mewajibkan eksekusi tes terkait. |

---

## 📝 Skema Payload Query Graph

Berikut adalah representasi query graph untuk mengambil relasi file dependensi dari database lokal:

```json
{
  "query": "MATCH (f:File {name: 'auth.service.ts'})-[:triggers_test]->(t:TestFile) RETURN t.path",
  "params": {
    "file_name": "auth.service.ts"
  },
  "max_depth": 2
}
```

---

## 💻 Implementasi Kode Graf Lokal

Skrip Python berikut menunjukkan cara membuat relasi graf antar file kode dan menavigasi ketergantungan file sebelum eksekusi uji berjalan:

```python
class DependencyGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = {} # adjacency list

    def add_dependency(self, file_from: str, file_to: str, relation: str):
        self.nodes.add(file_from)
        self.nodes.add(file_to)
        if file_from not in self.edges:
            self.edges[file_from] = []
        self.edges[file_from].append((file_to, relation))

    def get_impacted_files(self, start_file: str) -> list:
        # Simple Breadth-First Search (BFS) to find dependencies
        if start_file not in self.edges:
            return []
            
        impacted = []
        visited = set()
        queue = [start_file]
        visited.add(start_file)
        
        while queue:
            current = queue.pop(0)
            for neighbor, rel in self.edges.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    impacted.append((neighbor, rel))
                    queue.append(neighbor)
        return impacted

# Usage Example:
# graph = DependencyGraph()
# graph.add_dependency("auth.service.ts", "auth.controller.ts", "modify_impacts")
# graph.add_dependency("auth.controller.ts", "auth.test.ts", "triggers_test")
# print(graph.get_impacted_files("auth.service.ts"))
```

---

## ⚙️ Pola Pengambilan Data

Saat agen diperintahkan memodifikasi berkas target, agen pertama-tama menanyakan graf asosiatif untuk menarik seluruh berkas yang memiliki relasi dependensi tinggi ke dalam working memory (Modul 06). Ini menjamin compiler tidak menghasilkan error tipe di file eksternal yang tidak disentuh secara langsung.

---

## ⚠️ Anti-Patterns Memori Asosiatif

* ❌ **Ignoring Relational Graph**: Mengedit modul inti (core module) tanpa memetakan atau memverifikasi berkas downstream yang mengimpor modul tersebut.
* ❌ **Cyclic Graph Overflow**: Membuat relasi melingkar (circular dependency) pada graf yang menyebabkan algoritma pencarian BFS mengalami stack overflow.
* ❌ **Outdated Graph Data**: Tidak memperbarui relasi graf setelah menghapus atau memindahkan letak file di dalam direktori workspace.
