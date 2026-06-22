# 🤝 22 — Dynamic HITL (Human-in-the-Loop) Negotiation

> *"Tingkat kebebasan bertindak agen harus proporsional dengan potensi risiko kerusakan sistem."*

---

## 📋 Daftar Isi

1. [Filosofi HITL Dinamis](#-filosofi-hitl-dinamis)
2. [Alur Keputusan Runtime (Runtime Decision Flow)](#-alur-keputusan-runtime-runtime-decision-flow)
3. [Klasifikasi Risiko Tindakan (Action Risk Classification)](#-klasifikasi-risiko-tindakan-action-risk-classification)
4. [Protokol Negosiasi Otorisasi (Authorization Negotiation Protocol)](#-protokol-negosiasi-otorisasi-authorization-negotiation-protocol)
5. [Skema Request Persetujuan JSON (Approval Request Schema)](#-skema-request-persetujuan-json-approval-request-schema)
6. [Implementasi Kode Gerbang Persetujuan (Approval Gateway Code Fragment)](#-implementasi-kode-gerbang-persetujuan-approval-gateway-code-fragment)
7. [Mekanisme Rollback Instan (Instant Rollback Mechanisms)](#-mekanisme-rollback-instan-instant-rollback-mechanisms)
8. [Anti-Patterns Negosiasi HITL](#-anti-patterns-negosiasi-hitl)

---

## 🎯 Filosofi HITL Dinamis

Dynamic HITL Negotiation adalah **sistem persetujuan runtime**. Daripada meminta konfirmasi pengguna pada *setiap* tool call yang menjengkelkan, agen menilai tingkat risiko tindakannya secara dinamis dan hanya berhenti ketika risiko tergolong *Medium* atau *High*. Hal ini menjaga alur kerja (developer velocity) tetap cepat dan menyenangkan tanpa mengorbankan keamanan sistem.

---

## 🏗️ Alur Keputusan Runtime

```
                    ┌────────────────────────────┐
                    │ Evaluasi Risiko Tool Call  │
                    └─────────────┬──────────────┘
                                  │
                       [Apakah Risiko == High?]
                        ├── YA  ──► Tunda Eksekusi, Minta Persetujuan Chat (HITL)
                        └── TIDAK ──► Eksekusi Otonom (Low / Medium dengan Log)
```

---

## 📊 Klasifikasi Risiko Tindakan

Agen mengkategorikan setiap operasi menggunakan matriks risiko berikut:

| Level Risiko | Contoh Tindakan | Wewenang Eksekusi |
| :--- | :--- | :--- |
| **Low** | Membaca file (`read`), pencarian file (`glob`, `grep`), test kompilasi. | **Otonom Penuh** (Tidak butuh konfirmasi). |
| **Medium** | Pengeditan file (`edit`, `write`), modifikasi package dependency. | **Pemberitahuan Singkat** (Jelaskan perubahan di chat). |
| **High** | Menghapus direktori (`rm`), memodifikasi schema DB produksi. | **Persetujuan Mutlak** (Wajib konfirmasi `ya/tidak` di chat). |

---

## ⚙️ Protokol Negosiasi Otorisasi

Jika tindakan diklasifikasikan sebagai **High Risk**:
1. Berikan analisis dampak buruk (worst-case scenario).
2. Sediakan opsi mitigasi (misal: "Saya telah mem-backup database sebelum mengeksekusi migrasi ini").
3. Minta instruksi otorisasi secara formal.

---

## 📝 Skema Request Persetujuan JSON

Ketika berkomunikasi dengan UI frontend atau plugin IDE, agen mengirimkan payload metadata berikut:

```json
{
  "request_id": "req-9901-rm",
  "risk_level": "HIGH",
  "action": {
    "tool": "bash",
    "command": "rm -rf /workspace/tmp/cache_old"
  },
  "explanation": {
    "reason": "Clear disk space due to node_modules size limit",
    "impact": "Will permanently delete temporary cache data, no functional code is impacted.",
    "mitigation": "Backup of /tmp/cache_old saved to /tmp/cache_old_backup.zip"
  }
}
```

---

## 💻 Implementasi Kode Gerbang Persetujuan

Berikut skrip Node.js sederhana untuk membaca masukan pengguna (stdin) sebelum mengizinkan tindakan berbahaya:

```javascript
const readline = require('readline');

class HitlGateway {
  static askUser(question) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise((resolve) => {
      rl.question(question, (answer) => {
        rl.close();
        resolve(answer.trim().toLowerCase());
      });
    });
  }

  static async verifyAction(actionDescription, riskLevel) {
    if (riskLevel === 'LOW') {
      return true; // Autonomous execution
    }

    console.log(`\n⚠️ [HITL Alert] High-Risk Action Detected: ${actionDescription}`);
    const answer = await this.askUser('Do you approve this action? (y/N): ');
    return answer === 'y' || answer === 'yes';
  }
}

// Usage Example
// HitlGateway.verifyAction('rm -rf /dist', 'HIGH').then(approved => {
//   if (approved) console.log('Executing...');
//   else console.log('Aborted!');
// });
```

---

## 🔄 Mekanisme Rollback Instan

Setiap modifikasi file berkategori High Risk wajib didahului oleh pembuatan backup atau git checkpoint:
* **Pre-action Backup**: Salin file target ke folder `/tmp/agentfull_backup/`.
* **Git Clean Checkpoint**: Jalankan `git stash` atau buat commit sementara (`git commit -m "temp-checkpoint"`) untuk memudahkan rollback instan jika hasil eksekusi merusak sistem.

---

## ⚠️ Anti-Patterns Negosiasi HITL

* ❌ **Confirmation Fatigue**: Meminta persetujuan pengguna untuk hal kecil seperti membaca baris dokumentasi.
* ❌ **False Risk Classification**: Melabeli perintah penghapusan `rm -rf` sebagai risiko `LOW` untuk memintas gerbang persetujuan.
* ❌ **No Mitigation Strategy**: Meminta persetujuan tindakan berbahaya tanpa memberikan opsi pemulihan (rollback) jika terjadi kegagalan.
