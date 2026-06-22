# 🪙 21 — Token Budgeting & Financial Controls

> *"Kecerdasan tinggi tidak boleh dibayar dengan tagihan API yang tak terkendali."*

---

## 📋 Daftar Isi

1. [Filosofi Kontrol Finansial](#-filosofi-kontrol-finansial)
2. [Kebijakan Token Ceiling](#-kebijakan-token-ceiling)
3. [Optimasi Biaya Model Reasoning](#-optimasi-biaya-model-reasoning)
4. [Tindakan Saat Limit Tercapai](#-tindakan-saat-limit-tercapai)

---

## 🎯 Filosofi Kontrol Finansial

Model penalaran masa kini (seperti *o3* atau *Claude Opus 4.8*) membutuhkan biaya token yang sangat tinggi. Sistem kontrol finansial ini mewajibkan agen melacak konsumsi akumulatif token dan **membatasi kedalaman loop berpikir** agar tetap efisien secara ekonomi.

---

## 📊 Kebijakan Token Ceiling

Agen harus mematuhi kebijakan alokasi budget berikut:

| Kategori Tugas | Maksimal Token per Sesi | Batas Maksimal Biaya (USD) | Fallback |
| :--- | :--- | :--- | :--- |
| **Pencarian File & Review** | 100,000 | $1.00 | Hentikan pencarian jika melebihi limit. |
| **Agentic Coding (RLEF)** | 500,000 | $5.00 | Turunkan ke model MoE yang lebih murah (DeepSeek). |
| **Deep Debugging Loop** | 1,000,000 | $10.00 | Meminta persetujuan otorisasi biaya tambahan dari pengguna. |

---

## ⚙️ Tindakan Saat Limit Tercapai

*   **Pemberitahuan Instan**: Segera hentikan pemrosesan dan berikan laporan biaya saat ini.
*   **Context Pruning**: Lakukan pemotongan log history yang tidak krusial secara radikal untuk memperkecil token input pada request berikutnya.
