# 📦 23 — Self-Hosted Sandboxing & MicroVM Isolation

> *"Keamanan infrastruktur host pengguna adalah prioritas mutlak di atas seluruh pencapaian otonomi agen."*

---

## 📋 Daftar Isi

1. [Filosofi Sandbox Mandiri](#-filosofi-sandbox-mandiri)
2. [Pola Isolasi Lingkungan (Environment Isolation Patterns)](#-pola-isolasi-lingkungan-environment-isolation-patterns)
3. [Arsitektur Eksekusi Sandbox (Execution Architecture)](#-arsitektur-eksekusi-sandbox-execution-architecture)
4. [Konfigurasi Dockerfile Terisolasi (Dockerfile Isolation Snippet)](#-konfigurasi-dockerfile-terisolasi-dockerfile-isolation-snippet)
5. [Skrip Python Runner Sandbox (Sandbox Execution Script)](#-skrip-python-runner-sandbox-sandbox-execution-script)
6. [Langkah Pemulihan & Cleanup (Rollback & Clean-up Protocols)](#-langkah-pemulihan--cleanup-rollback--clean-up-protocols)
7. [Anti-Patterns Sandbox Mandiri](#-anti-patterns-sandbox-mandiri)

---

## 🎯 Filosofi Sandbox Mandiri

Ketika agen memproses input eksternal (seperti menguji kode yang ditulis oleh kontributor publik), mengeksekusi kode tersebut secara langsung pada mesin host sangat berbahaya. Seluruh eksekusi runtime wajib diisolasi di dalam **MicroVM atau sandbox khusus**. Keamanan data host tidak boleh dikompromikan demi kenyamanan pengerjaan tugas otonom.

---

## 🏗️ Pola Isolasi Lingkungan

Isolasi sistem dibagi menjadi 3 lapis perlindungan:

```
        ┌────────────────────────────────────────────────────────┐
        │ 1. Host Machine (Sistem Utama Pengguna - Aman)         │
        │    ┌──────────────────────────────────────────────┐    │
        │    │ 2. Docker / Podman (Isolasi OS Layer)        │    │
        │    │    ┌────────────────────────────────────┐    │    │
        │    │    │ 3. gVisor / Firecracker (MicroVM)  │    │    │
        │    │    │    (Eksekusi Agen Otonom - Sandbox)│    │    │
        │    │    └────────────────────────────────────┘    │    │
        │    └──────────────────────────────────────────────┘    │
        └────────────────────────────────────────────────────────┘
```

---

## 🛡️ Arsitektur Eksekusi Sandbox

* **Stateless Operations**: Runtime pengujian harus dibuang (destroyed) setelah kompilasi selesai.
* **No Network Access (Optional)**: Secara default, matikan akses internet luar (`--network none`) saat menjalankan file binary tidak dikenal demi mencegah serangan eksfiltrasi data.

| Lapisan Sandbox | Teknologi Utama | Tingkat Keamanan | Overhead Performa |
| :--- | :--- | :--- | :--- |
| **Lapis 1** | Docker Container | Sedang | Rendah |
| **Lapis 2** | gVisor Runtime | Tinggi | Sedang |
| **Lapis 3** | Firecracker MicroVM | Sangat Tinggi | Tinggi |

---

## 🐳 Konfigurasi Dockerfile Terisolasi

Untuk membuat lingkungan pengujian Node.js yang aman, gunakan Dockerfile non-root berikut:

```dockerfile
# Dockerfile.sandbox
FROM node:18-alpine

# Set secure working directory
WORKDIR /app

# Create a non-privileged system user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set environment vars for safety
ENV NODE_ENV=test
ENV DISABLE_OPENCOLLECTIVE=true

# Copy source with non-privileged user ownership
COPY --chown=appuser:appgroup . .

# Switch to the non-root user
USER appuser

# Disable network access within container during test running
CMD ["npm", "test"]
```

---

## 💻 Skrip Python Runner Sandbox

Berikut skrip Python untuk meluncurkan container sandbox secara aman dan menangkap stdout/stderr tanpa membiarkan container berjalan selamanya:

```python
import subprocess
import sys

def run_in_sandbox(command: str, timeout_sec: int = 30):
    print(f"[Sandbox] Launching command: {command}")
    
    # Run docker command with memory limit and disabled network
    docker_cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "256m",
        "--cpus", "0.5",
        "node-sandbox-image",
        "sh", "-c", command
    ]
    
    try:
        result = subprocess.run(
            docker_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print("[Sandbox] Execution timed out!")
        return -1, "", "TIMEOUT EXPIRED"

# Usage Example:
# code, out, err = run_in_sandbox("npm test")
```

---

## 🧹 Langkah Pemulihan & Cleanup

Setiap kali pengujian sandbox selesai:
1. **Hentikan Container Menggantung**: Cari container yatim piatu dengan perintah `docker ps -q --filter label=sandbox` lalu jalankan `docker kill`.
2. **Hapus Volume Sementara**: Bersihkan mount directory menggunakan `docker volume prune -f`.
3. **Reset State Direktori Host**: Pastikan tidak ada file log buangan container yang tertinggal di folder host menggunakan perintah clean-up lokal.

---

## ⚠️ Anti-Patterns Sandbox Mandiri

* ❌ **Mounting Host Root**: Melakukan mounting direktori root host `/` ke dalam container sandbox dengan hak akses tulis (`rw`).
* ❌ **Running as Root**: Menjalankan instruksi kompilasi di dalam container sebagai pengguna root, yang dapat mengeksploitasi celah keamanan kernel (container escape).
* ❌ **Persistent Data Pollution**: Membiarkan container uji menulis langsung ke disk host tanpa melakukan pembersihan (cleanup) volume pasca uji selesai.
