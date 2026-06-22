# 📦 12 — Environment Sandbox & Dependency Isolation

> *"Ujilah kodenya di dalam kurungan besi, pastikan ia aman sebelum dilepas ke alam bebas."*

---

## 📋 Daftar Isi

1. [Filosofi Sandbox](#-filosofi-sandbox)
2. [Tingkat Isolasi Lingkungan (Environment Isolation Levels)](#-tingkat-isolasi-lingkungan-environment-isolation-levels)
3. [Virtual Environment untuk Python (Python Virtual Environment)](#-virtual-environment-untuk-python-python-virtual-environment)
4. [Isolasi Dependensi Node.js (Node.js Local Isolation)](#-isolasi-dependensi-nodejs-nodejs-local-isolation)
5. [Konfigurasi Docker Compose untuk Sandbox (Docker Sandbox Setup)](#-konfigurasi-docker-compose-untuk-sandbox-docker-sandbox-setup)
6. [Langkah Verifikasi Uji Coba (Sandbox Verification Steps)](#-langkah-verifikasi-uji-coba-sandbox-verification-steps)
7. [Anti-Patterns Isolasi](#-anti-patterns-isolasi)

---

## 🎯 Filosofi Sandbox

Saat bekerja pada sistem yang sudah berjalan, agen tidak boleh mengacaukan dependency global atau merusak konfigurasi sistem milik pengguna. Setiap perubahan runtime harus diisolasi dan mudah dibatalkan (rollback). Isolasi adalah pertahanan utama terhadap konflik versi pustaka dan kerusakan sistem operasi host.

---

## 🏗️ Tingkat Isolasi Lingkungan

Agen harus memilih tingkat isolasi yang sesuai dengan risiko tugas yang dikerjakan:

```
┌────────────────────────────────────────────────────────┐
│ [Level 3: MicroVM (Firecracker / gVisor)]               │
│ - Eksekusi binari untrusted, network restricted        │
└───────────▲────────────────────────────────────────────┘
            │ Upgrades to
┌───────────┴────────────────────────────────────────────┐
│ [Level 2: Container (Docker / Podman)]                 │
│ - Menjalankan database test, service server, compile    │
└───────────▲────────────────────────────────────────────┘
            │ Upgrades to
┌───────────┴────────────────────────────────────────────┐
│ [Level 1: Language-level virtual environment (venv)]   │
│ - Eksekusi skrip python/js murni tanpa dependensi OS   │
└────────────────────────────────────────────────────────┘
```

---

## 🐍 Virtual Environment untuk Python

Jangan pernah menjalankan `pip install` secara langsung di sistem host tanpa mengaktifkan virtual environment terlebih dahulu.

### Langkah-langkah Pembuatan Virtual Environment:

```bash
# 1. Create a virtual environment directory named .venv
python3 -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Upgrade basic package manager safely inside sandbox
pip install --upgrade pip setuptools wheel

# 4. Install requirements from local file
pip install -r requirements.txt

# 5. Deactivate environment when finished
deactivate
```

---

## 🟢 Isolasi Dependensi Node.js

Untuk runtime JavaScript/TypeScript, hindari instalasi paket global (`-g` atau `--global`) kecuali diinstruksikan oleh pengguna.

### Manajemen Dependensi Lokal:

```json
{
  "name": "isolated-test-runner",
  "version": "1.0.0",
  "private": true,
  "description": "Sandbox configuration for running test suites",
  "scripts": {
    "test:sandbox": "jest --config jest.sandbox.config.js --runInBand"
  },
  "dependencies": {
    "jest": "^29.5.0",
    "ts-jest": "^29.1.0"
  }
}
```

Gunakan command berikut untuk menginstal dan menjalankan tes tanpa mengotori registry global:

```bash
# Install dependencies strictly defined in package.json locally
npm install --no-audit --no-fund

# Run tests using the local node_modules binary
npx jest --config jest.sandbox.config.js
```

---

## 🐳 Konfigurasi Docker Compose untuk Sandbox

Berikut adalah file konfigurasi `docker-compose` untuk menguji aplikasi database secara terisolasi tanpa mengotori mesin host:

```yaml
# docker-compose.test-db.yml
version: '3.8'
services:
  test-postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password_123_secure
    ports:
      - "54321:5432" # Bind to custom high-numbered port to avoid system conflicts
    volumes:
      - pgdata-test:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test_user -d test_db"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata-test:
```

Untuk mengontrol container dari agen:
```bash
# Start the database container and wait for healthcheck to pass
docker-compose -f docker-compose.test-db.yml up -d

# Perform migration testing and run unit tests
python3 -m pytest tests/integration/

# Tear down the isolated database container and remove volumes
docker-compose -f docker-compose.test-db.yml down -v
```

---

## 🛡️ Keamanan Runtime Lokal

Saat menguji kode yang ditulis:
1. **Gunakan Port Non-Standar**: Jangan gunakan port produksi (misal: `80`, `443`, `8080`) untuk testing jika bisa memicu konflik port.
2. **Mocking External APIs**: Gantilah API luar dengan mock data untuk mencegah pengiriman data sampah ke server pihak ketiga selama pengujian.
3. **Pembersihan Pasca Uji (Cleanup)**: Hapus file temporary, log, atau database sqlite yang dibuat selama proses verifikasi sebelum menyerahkan pekerjaan ke pengguna.

---

## ⚠️ Anti-Patterns Isolasi

* ❌ **Global Polluting**: Menginstal software via `apt-get` or `brew` tanpa izin pengguna untuk tugas sementara.
* ❌ **Production DB Testing**: Menjalankan skema tes langsung pada database staging/produksi.
* ❌ **Leftover Files**: Meninggalkan file dump, cache, atau script testing sampah di direktori root.
* ❌ **No Resource Limits**: Menjalankan program stress test atau performa tanpa limit memori/CPU di docker container.
