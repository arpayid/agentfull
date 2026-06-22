# 🔮 17 — Autonomous Agent Landscape & Benchmark Standards

> *"Membangun agen yang sukses membutuhkan pemahaman terhadap pola terbaik dari sistem agen otonom tingkat dunia."*

---

## 📋 Daftar Isi

1. [Filosofi Desain Agen](#-filosofi-desain-agen)
2. [Taksonomi Arsitektur Agen (Agent Architectures Taxonomy)](#-taksonomi-arsitektur-agen-agent-architectures-taxonomy)
3. [Standar Evaluasi Benchmarking (Benchmarking Standards)](#-standar-evaluasi-benchmarking-benchmarking-standards)
4. [Skema Metrik Keberhasilan (Evaluation Metrics Schema)](#-skema-metrik-keberhasilan-evaluation-metrics-schema)
5. [Skrip Pengujian Benchmarking (Test Execution Script)](#-skrip-pengujian-benchmarking-test-execution-script)
6. [Pedoman Implementasi SOP (Standard Operating Procedures)](#-pedoman-implementasi-sop-standard-operating-procedures)
7. [Anti-Patterns Evaluasi Agen](#-anti-patterns-evaluasi-agen)

---

## 🎯 Filosofi Desain Agen

Untuk bersaing di level tertinggi, sebuah agen AI tidak boleh dirancang secara acak. Agen harus mengadopsi standar arsitektur teruji seperti yang digunakan oleh pionir industri (*Aider, Devin, AutoGen*). Pengukuran kinerja harus dilakukan secara terstruktur menggunakan dataset evaluasi objektif demi memastikan keandalan perilaku agen.

---

## 🏗️ Taksonomi Arsitektur Agen

Sistem agen modern dikelompokkan ke dalam tiga arsitektur utama:

```
┌────────────────────────────────────────────────────────┐
│ 1. Single-Agent CLI (Aider style)                      │
│ - Fokus pada kecepatan iterasi & auto-commit git       │
└────────────────────────────────────────────────────────┘
                           ▲
                           │ Evolved into
┌──────────────────────────┴─────────────────────────────┐
│ 2. Modular Multi-Agent (AutoGen/CrewAI style)          │
│ - Pembagian tugas berdasarkan persona (PM, QA, Dev)    │
└────────────────────────────────────────────────────────┘
                           ▲
                           │ Evolved into
┌──────────────────────────┴─────────────────────────────┐
│ 3. Structured SOP-based Agent (ChatDev style)          │
│ - Alur kerja kaku terarah (Design -> Dev -> QA -> PR)  │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Standar Evaluasi Benchmarking

Setiap pengembangan perilaku agen baru wajib diuji pada benchmark standar global untuk mengukur kemampuan penalaran tingkat lanjut:

* **SWE-bench**: Menguji kemampuan agen menyelesaikan masalah/issue github nyata pada repositori open-source besar.
* **HumanEval & MBPP**: Menguji kemampuan menulis fungsi python/js dasar secara sintaksis.
* **Arena-Hard-Auto**: Menguji preferensi kualitas jawaban agen dibanding model baseline global.

---

## 📈 Skema Metrik Keberhasilan

Kualitas perilaku agen harus diukur berdasarkan parameter kuantitatif berikut:

| Nama Benchmark | Target Minimal | Target Ideal | Deskripsi Pengukuran |
| :--- | :--- | :--- | :--- |
| **SWE-bench Lite** | $> 25\%$ | $> 40\%$ | Persentase bug GitHub nyata yang berhasil diselesaikan secara otomatis. |
| **HumanEval** | $> 85\%$ | $> 95\%$ | Keberhasilan sintaksis dan fungsional dari tes unit Python dasar. |
| **Tool Execution Ratio** | $> 98\%$ | $100\%$ | Rasio keberhasilan pemanggilan tool tanpa kegagalan argumentasi. |

---

## 💻 Skrip Pengujian Benchmarking

Berikut adalah contoh skrip Node.js untuk mengeksekusi program benchmark lokal dan membandingkan akurasi output agen dengan ground truth:

```javascript
const fs = require('fs');
const { execSync } = require('child_process');

function runBenchmarkTest(testCaseFile, groundTruthFile) {
  console.log(`[Benchmark] Evaluating test case: ${testCaseFile}...`);
  
  // Read expected output
  const expected = fs.readFileSync(groundTruthFile, 'utf-8').trim();
  
  try {
    // Run the agent generator command
    const actual = execSync(`node /workspace/src/agent.js --task "${testCaseFile}"`, { encoding: 'utf-8' }).trim();
    
    // Simple exact match validation
    if (actual === expected) {
      return { status: 'pass', match: true };
    } else {
      return { status: 'fail', match: false, reason: 'Mismatch outputs' };
    }
  } catch (error) {
    return { status: 'error', error: error.message };
  }
}

// Example Execution
// const result = runBenchmarkTest('tests/cases/01_auth.txt', 'tests/truth/01_auth.txt');
// console.log(result);
```

---

## 📋 Pedoman Implementasi SOP

1. **Gunakan Baseline Valid**: Sebelum melakukan perbaikan core, jalankan test suite standar pada agen untuk mencatat performa awal.
2. **Review Kegagalan (Failure Analysis)**: Lakukan review manual pada file trajectory log ketika agen gagal memecahkan masalah SWE-bench.
3. **No Target Leakage**: Jangan pernah memasukkan file uji coba (test cases) dari SWE-bench ke dalam dataset pelatihan model atau memori jangka panjang agen.

---

## ⚠️ Anti-Patterns Evaluasi Agen

* ❌ **Vibe Coding Evaluation**: Mengandalkan perasaan ("rasanya bekerja lebih baik") daripada metrik numerik objektif.
* ❌ **Hardcoded Test Assertions**: Membuat tes benchmark yang sudah disesuaikan agar cocok dengan keluaran agen saat ini.
* ❌ **Ignoring Latency**: Hanya mengukur akurasi tanpa memedulikan latensi atau total token yang dihabiskan untuk menyelesaikan satu masalah.
