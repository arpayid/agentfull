# 🔮 17 — Autonomous Agent Landscape & Benchmark Standards

> *"Membangun agen yang sukses membutuhkan pemahaman terhadap pola terbaik dari sistem agen otonom tingkat dunia."*

---

## 📋 Daftar Isi

1. [Filosofi Desain Agen](#-filosofi-desain-agen)
2. [Taksonomi Arsitektur Agen](#-taksonomi-arsitektur-agen)
3. [Standar Evaluasi Benchmarking](#-standar-evaluasi-benchmarking)
4. [Pedoman Implementasi SOP](#-pedoman-implementasi-sop)

---

## 🎯 Filosofi Desain Agen

Untuk bersaing di level tertinggi, sebuah agen AI tidak boleh dirancang secara acak. Agen harus mengadopsi standar arsitektur teruji seperti yang digunakan oleh pionir industri (*Aider, Devin, AutoGen*).

---

## 🏗️ Taksonomi Arsitektur Agen

1. **Single-Agent CLI Companion (Aider style)**:
   * Berjalan langsung di terminal lokal.
   * Berfokus pada integrasi cepat, auto-commit git, dan interaksi chatting pendek dengan developer.
2. **Modular Multi-Agent (AutoGen/CrewAI style)**:
   * Pembagian tugas spesifik berdasarkan persona (PM, QA, Dev).
   * Bagus untuk proyek jangka panjang yang membutuhkan koordinasi tim virtual.
3. **Structured SOP-based Agent (Agents/ChatDev style)**:
   * Agen dipandu oleh Standard Operating Procedure (SOP) kaku (Tahap 1: Desain $\rightarrow$ Tahap 2: Coding $\rightarrow$ Tahap 3: Review).

---

## 📊 Standar Evaluasi Benchmarking

Setiap pengembangan perilaku agen baru wajib diuji pada benchmark standar global:
*   **SWE-bench**: Menguji kemampuan agen menyelesaikan masalah/issue github nyata pada repositori open-source besar.
*   **HumanEval & MBPP**: Menguji kemampuan menulis fungsi python/js dasar secara sintaksis.
*   **Arena-Hard-Auto**: Menguji preferensi kualitas jawaban agen dibanding model baseline global.
