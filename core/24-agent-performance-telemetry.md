# 📊 24 — Agent Performance & Execution Telemetry

> *"Apa yang tidak bisa diukur, tidak bisa ditingkatkan. Dokumentasikan setiap metrik eksekusi."*

---

## 📋 Daftar Isi

1. [Filosofi Telemetri Agen](#-filosofi-telemetri-agen)
2. [Arsitektur Pipeline Telemetri (Telemetry Pipeline Architecture)](#-arsitektur-pipeline-telemetri-telemetry-pipeline-architecture)
3. [Matriks Pengukuran Eksekusi (Execution Metrics Matrix)](#-matriks-pengukuran-eksekusi-execution-metrics-matrix)
4. [Format Pencatatan Log Telemetri (Telemetry YAML/JSON Format)](#-format-pencatatan-log-telemetri-telemetry-yamljson-format)
5. [Implementasi Kode Telemetri (Telemetry Logger Code Fragment)](#-implementasi-kode-telemetri-telemetry-logger-code-fragment)
6. [Analisis Bottleneck Runtime (Runtime Bottleneck Analysis)](#-analisis-bottleneck-runtime-runtime-bottleneck-analysis)
7. [Anti-Patterns Telemetri Kinerja](#-anti-patterns-telemetri-kinerja)

---

## 🎯 Filosofi Telemetri Agen

Agent Performance Telemetry adalah **sistem pencatatan dan visualisasi kinerja operasional agen**. Ini melacak berapa banyak tool call yang berhasil, durasi tunggu inferensi model, serta seberapa sering sistem mendeteksi/memotong loop anomali perilaku. Pengumpulan metrik terperinci membantu developer memantau kesehatan dan tingkat efisiensi sistem agen yang berjalan secara otonom.

---

## 🏗️ Arsitektur Pipeline Telemetri

Metrik dikumpulkan dari setiap pemanggilan alat dan dikompilasi ke penyimpanan data persisten:

```
┌──────────────────┐      ┌─────────────────────┐      ┌────────────────────────┐
│  Tool Execution  ├─────►│  Telemetry Collector├─────►│  YAML/JSON Local File  │
└──────────────────┘      └──────────┬──────────┘      └────────────────────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │ Real-time Dashboard │
                          └─────────────────────┘
```

---

## 📊 Matriks Pengukuran Eksekusi

Setiap langkah pengerjaan tugas oleh agen dipantau melalui parameter kinerja berikut:

| Nama Metrik | Satuan | Target Optimal | Mengapa? |
| :--- | :--- | :--- | :--- |
| **Tool Success Rate (TSR)** | Persentase (%) | $> 95\%$ | Mengurangi overhead pemanggilan ulang tool yang gagal. |
| **Reasoning Efficiency (RE)** | Token/detik | $> 50$ tokens/s | Mengukur kecepatan pemrosesan Chain of Thought internal. |
| **Task Completion Speed** | Menit | $< 15$ menit | Mengurangi durasi tunggu developer saat menunggu PR/fix. |
| **Loop Intervention Rate** | Jumlah | $0$ | Meminimalkan intervensi manual pemotongan infinite loop. |

---

## 📝 Format Pencatatan Log Telemetri

Setiap sesi berakhir, agen menulis laporan kinerja dinamis dalam berkas `.agentfull/telemetry/session-metrics.yml`:

```yaml
telemetry:
  session: "agy-202606"
  task_type: "refactoring"
  metrics:
    total_steps: 14
    total_tokens: 154000
    model_inference_seconds: 112.4
    tools_executed:
      bash: 8
      read: 4
      edit: 2
    success_rate: 100.0
    cost_usd: 1.25
    infinite_loops_detected: 0
  environment:
    os: "linux"
    node_version: "v18.16.0"
```

---

## 💻 Implementasi Kode Telemetri

Berikut skrip Node.js untuk merekam durasi eksekusi tool dan menyimpannya ke format file telemetri:

```javascript
const fs = require('fs');

class TelemetryLogger {
  constructor(sessionFile) {
    this.sessionFile = sessionFile;
    this.metrics = {
      startTime: Date.now(),
      steps: 0,
      tools: {}
    };
  }

  logToolExecution(toolName, elapsedMs, status) {
    this.metrics.steps++;
    if (!this.metrics.tools[toolName]) {
      this.metrics.tools[toolName] = { count: 0, failed: 0, totalMs: 0 };
    }
    this.metrics.tools[toolName].count++;
    this.metrics.tools[toolName].totalMs += elapsedMs;
    if (status === 'fail') {
      this.metrics.tools[toolName].failed++;
    }
  }

  saveReport() {
    const elapsedSeconds = (Date.now() - this.metrics.startTime) / 1000;
    const report = {
      session_duration_sec: elapsedSeconds,
      total_steps: this.metrics.steps,
      tools_metrics: this.metrics.tools
    };
    
    fs.writeFileSync(this.sessionFile, JSON.stringify(report, null, 2));
    console.log('[Telemetry] Performance report saved successfully.');
  }
}

// Usage Example
// const logger = new TelemetryLogger('/tmp/telemetry.json');
// logger.logToolExecution('bash', 450, 'success');
// logger.saveReport();
```

---

## ⚙️ Analisis Bottleneck Runtime

* **Identifikasi Latensi Tinggi**: Jika inferensi model memakan waktu lebih dari 15 detik per langkah, pertimbangkan untuk beralih ke model dengan latency rendah (misal: model MoE open-source).
* **Deteksi Kegagalan API**: Pantau status respons dari server hosting LLM. Tingkat error HTTP 5xx yang tinggi mengindikasikan perlunya implementasi retry dengan exponential backoff.

---

## ⚠️ Anti-Patterns Telemetri Kinerja

* ❌ **No Metrics Aggregation**: Hanya mencetak durasi ke terminal chat tanpa menyimpannya secara terstruktur untuk keperluan analisis pasca pengerjaan.
* ❌ **Blocking Instrumentation**: Menjalankan logger telemetri yang memblokir proses eksekusi kode utama (blocking synchronous call), sehingga meningkatkan total durasi tugas.
* ❌ **Ignoring Telemetry Data**: Tidak menggunakan metrik token untuk memperingatkan pengguna saat budget mendekati ambang batas limit (Token Budgeting).
