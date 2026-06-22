# 🔀 11 — Multi-Agent Coordination & Delegation

> *"Ketika satu agen tidak cukup, kekuatan orkestrasi paralel memisahkan agen biasa dari sistem agen elit."*

---

## 📋 Daftar Isi

1. [Filosofi Multi-Agent](#-filosofi-multi-agent)
2. [Delegasi Tugas & Pemisahan Scope](#-delegasi-tugas--pemisahan-scope)
3. [Transfer Konteks (Context Handoff)](#-transfer-konteks-context-handoff)
4. [Menggabungkan Hasil (Aggregation)](#-menggabungkan-hasil-aggregation)
5. [Anti-Patterns Koordinasi](#-anti-patterns-koordinasi)

---

## 🎯 Filosofi Multi-Agent

Pada tugas skala besar, membagi pekerjaan ke beberapa sub-agent (spesialis) secara paralel menghemat waktu dan meningkatkan akurasi. Agen utama bertindak sebagai **Orchestrator** yang mengarahkan sub-agent.

---

## 📋 Delegasi Tugas & Pemisahan Scope

Setiap sub-agent harus memiliki tugas yang terdefinisi dengan sangat spesifik untuk menghindari tumpang tindih.

### Pembagian Peran Klasik:
* **Orchestrator (Main Agent)**: Merencanakan, membagi tugas, memvalidasi hasil akhir, dan berkomunikasi dengan pengguna.
* **Researcher/Explorer Sub-Agent**: Melakukan pencarian kode, membaca dokumentasi, dan memetakan struktur file.
* **Implementer Sub-Agent**: Menulis kode baru, melakukan refactoring, dan menulis tes.
* **Reviewer/Verifier Sub-Agent**: Menjalankan tes, memeriksa kualitas kode, dan melakukan linter check.

---

## 🔄 Transfer Konteks (Context Handoff)

Saat meluncurkan sub-agent, berikan instruksi yang jelas:
1. **Tujuan Konkret**: Apa output yang diharapkan (misal: "Kembalikan list path file yang menggunakan library X").
2. **Konteks Terbatas**: Jangan kirim seluruh riwayat chat jika tidak diperlukan. Hanya berikan potongan kode atau file yang relevan.
3. **Format Output**: Minta sub-agent mengembalikan format terstruktur (JSON atau Markdown ringkas).

---

## ⚠️ Anti-Patterns Koordinasi

* ❌ **Redundant Operations**: Agen utama dan sub-agent melakukan pencarian file yang sama berulang kali.
* ❌ **Context Spamming**: Mengirimkan seluruh codebase ke sub-agent sehingga menghabiskan kuota token.
* ❌ **No Verification**: Langsung mempercayai kode dari sub-agent tanpa melakukan verifikasi kompilasi atau tes lokal terlebih dahulu.
