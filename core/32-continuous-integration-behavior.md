# 🛠️ 32 — Continuous Integration Behavior

> *"Menjalankan siklus eksekusi CI/CD secara otonom, patuh terhadap kode keluar (exit codes), mengamankan artefak, dan memitigasi timeout eksekusi runner."*

---

## 📋 Daftar Isi
1. [Filosofi CI/CD Otonom](#-filosofi-cicd-otonom)
2. [Kepatuhan Kode Keluar (Exit Code Compliance)](#-kepatuhan-kode-keluar-exit-code-compliance)
3. [Manajemen & Unggah Artefak (Artifacts Upload)](#-manajemen--unggah-artefak-artifacts-upload)
4. [Mitigasi Timeout Eksekusi (Execution Timeout Mitigation)](#-mitigasi-timeout-eksekusi-execution-timeout-mitigation)
5. [Arsitektur Aliran CI/CD Agen (CI/CD Agent Pipeline Architecture)](#-arsitektur-aliran-cicd-agen-cicd-agent-pipeline-architecture)
6. [Skema & Konfigurasi Pipeline (Pipeline Configuration Schema)](#-skema--konfigurasi-pipeline-pipeline-configuration-schema)

---

## 🎯 Filosofi CI/CD Otonom

Dalam paradigma pengembangan perangkat lunak modern (SOTA 2026), agen AI tidak hanya menulis kode tetapi juga bertanggung jawab atas integrasi berkelanjutan (Continuous Integration). Agen harus bertindak sebagai operator yang cerdas di dalam lingkungan CI runner. Agen harus memahami siklus hidup build, mampu mengurai log kegagalan secara real-time, mengidentifikasi flakiness, serta memastikan pipeline berakhir dengan status sukses secara valid dan aman tanpa memicu tagihan komputasi tak terbatas.

---

## ⚙️ Kepatuhan Kode Keluar (Exit Code Compliance)

Setiap proses sistem operasi berkomunikasi melalui kode keluar (exit code). Agen harus menginterpretasikan dan merespons kode keluar ini secara presisi sesuai standar POSIX:

*   **Exit Code `0`**: Sukses. Lanjutkan ke tahap/job berikutnya.
*   **Exit Code `1`**: Kegagalan umum. Periksa syntax error atau kegagalan assertion unit test.
*   **Exit Code `127`**: Perintah tidak ditemukan. Agen harus menginstal dependensi yang hilang melalui package manager sebelum menjalankan ulang perintah.
*   **Exit Code `137`**: Proses dihentikan paksa (Out of Memory - OOM). Agen harus mengurangi footprint memori atau membatasi ukuran batch pengujian.

### Pola Pemrograman Command Execution Wrapper:

```python
import subprocess
import sys

def execute_ci_command(command: str, timeout_seconds: int = 300) -> int:
    """Executes a CI command inside the runner sandbox and catches exit codes."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        print(f"STDOUT:\n{result.stdout}")
        if result.returncode != 0:
            print(f"STDERR (Exit Code {result.returncode}):\n{result.stderr}", file=sys.stderr)
        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"Error: Command '{command}' timed out after {timeout_seconds}s.", file=sys.stderr)
        return 124  # Standard timeout exit code
```

---

## 📦 Manajemen & Unggah Artefak (Artifacts Upload)

Ketika pipeline gagal atau selesai, agen harus secara otonom mengemas dan mengunggah artefak penting seperti log diagnostik, heap dumps, test coverage report, dan snapshot visual untuk inspeksi lebih lanjut.

### Mekanisme Packaging & Upload:

1.  **Pencarian Berkas Terkait**: Gunakan utilitas glob untuk menemukan laporan kesalahan (`*.log`, `*junit.xml`, `coverage/`).
2.  **Kompresi Data**: Buat arsip `.tar.gz` atau `.zip` untuk menghemat bandwidth dan penyimpanan.
3.  **Unggah Otonom**: Kirim file ke Cloud Storage menggunakan REST API dengan kredensial berumur pendek (presigned URLs).

```bash
# GitHub Actions runner command pattern for artifact upload
tar -czf build-artifacts.tar.gz ./logs/ ./coverage/ ./test-results/
curl -X PUT -H "Content-Type: application/gzip" \
     --upload-file build-artifacts.tar.gz \
     "${SHORT_LIVED_PRESIGNED_S3_URL}"
```

---

## ⏱️ Mitigasi Timeout Eksekusi (Execution Timeout Mitigation)

Kegagalan menggantung (hangs) pada CI runner sangat mahal karena membuang resource komputasi. Agen harus mengimplementasikan pemantauan proaktif untuk mendeteksi kondisi hang.

### Strategi Mitigasi:
1.  **Keep-Alive Signals**: Menulis berkas heartbeat secara berkala selama eksekusi tugas yang panjang.
2.  **Graceful Degraded Shutdown**: Menggunakan sinyal `SIGTERM` terlebih dahulu sebelum memaksa dengan `SIGKILL` guna memberikan kesempatan bagi runner untuk mengamankan partial logs.
3.  **Incremental Test Suite Execution**: Membagi test suite besar menjadi chunks kecil untuk menghindari melebihi batas durasi maksimum runner tunggal.

```yaml
# SOTA GitHub Actions Runner Timeout Configuration
name: Agentic CI Pipeline
on: [push]
jobs:
  agent-run:
    runs-on: ubuntu-latest
    timeout-minutes: 15 # Avoid infinite hangs
    steps:
      - uses: actions/checkout@v4
      - name: Set up Environment
        run: |
          npm ci
      - name: Execute Tests with Agentic Timeout Wrapper
        run: |
          timeout --preserve-status --kill-after=30s 12m npm run test
```

---

## 🗺️ Arsitektur Aliran CI/CD Agen (CI/CD Agent Pipeline Architecture)

```
[Code Push/Trigger]
         │
         ▼
[CI Runner Initialization]
         │
         ▼
[Execution Command Wrapper] ──(Timeout Exceeded?)──► [SIGTERM/SIGKILL] ──► [Compress Logs] ──► [Upload Artifacts]
         │                                                                       ▲
         ├─► (Exit Code 0) ──► [Pipeline Success]                                │
         │                                                                       │
         └─► (Exit Code != 0) ──► [Log Parser Engine] ──► [Auto-Fix Attempt] ────┘
```

---

## 📄 Skema & Konfigurasi Pipeline (Pipeline Configuration Schema)

Berikut adalah contoh skema JSON untuk konfigurasi agen CI/CD otonom:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgenticCiConfig",
  "type": "object",
  "properties": {
    "pipelineId": {
      "type": "string",
      "format": "uuid"
    },
    "timeoutLimitSeconds": {
      "type": "integer",
      "minimum": 10,
      "maximum": 3600
    },
    "retryPolicy": {
      "type": "object",
      "properties": {
        "maxAttempts": { "type": "integer", "default": 3 },
        "backoffIntervalSeconds": { "type": "integer", "default": 5 }
      },
      "required": ["maxAttempts"]
    },
    "artifacts": {
      "type": "object",
      "properties": {
        "paths": {
          "type": "array",
          "items": { "type": "string" }
        },
        "targetStorageBucket": { "type": "string" }
      },
      "required": ["paths", "targetStorageBucket"]
    }
  },
  "required": ["pipelineId", "timeoutLimitSeconds", "artifacts"]
}
```
