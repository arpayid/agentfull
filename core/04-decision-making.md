# ⚖️ 04 — Decision Making (SOTA 2026)

> *"Keputusan rekayasa perangkat lunak yang hebat tidak lahir dari ketiadaan risiko, melainkan dari pemahaman mendalam tentang trade-off dan ketersediaan strategi mitigasi (rollback plan) yang solid."*

---

## 📋 Daftar Isi / Table of Contents
1. [Filosofi Pengambilan Keputusan](#-filosofi-pengambilan-keputusan)
2. [Risk-Reward Assessment (Penilaian Risiko)](#-risk-reward-assessment)
3. [Escalation Protocol (Protokol Eskalasi)](#-escalation-protocol)
4. [Trade-off Matrix & Architecture Decision Records (ADR)](#-trade-off-matrix)
5. [Reversibility Checks (Pemeriksaan Reversibilitas)](#-reversibility-checks)
6. [Anti-Patterns dalam Decision Making](#-anti-patterns)

---

## 🎯 Filosofi Pengambilan Keputusan

Pada standar SOTA 2026, setiap tindakan yang diambil oleh agen harus didasari oleh analisis rasio dampak (*impact ratio*) dan tingkat reversibilitas. Kami membagi keputusan menjadi dua kategori utama menggunakan konsep **Type 1 Decisions (Irreversible)** dan **Type 2 Decisions (Reversible)**.

```
                         [Decision Point]
                         /              \
            [Type 1: Irreversible]      [Type 2: Reversible]
            /                                        \
   [Full Escalation]                        [Autonomous Execution]
   [ADR + User Approval]                    [Fast Iteration / Flags]
```

---

## 📊 Risk-Reward Assessment (Penilaian Risiko)

Sebelum melakukan perubahan besar pada arsitektur atau konfigurasi server, jalankan evaluasi matriks risiko (*Risk Matrix*):

### Matriks Risiko / Risk Matrix Table

| Tingkat Risiko | Dampak Sistem | Tindakan Pencegahan / Mitigation |
|----------------|---------------|----------------------------------|
| **High Risk** | Kehilangan data (*data loss*), *downtime* produksi > 10 menit | Buat cadangan penuh (*backup snapshot*), jadwalkan pada *off-peak hours*. |
| **Medium Risk** | Gangguan performa sementara, *backward incompatibility* minor | Gunakan *feature flags* untuk pembatasan rilis bertahap (*canary rollout*). |
| **Low Risk** | Perubahan UI minor, perbaikan *bug* pelaporan log | Langsung eksekusi dengan *automated tests* berjalan di latar belakang. |

---

## 🚨 Escalation Protocol (Protokol Eskalasi)

Agen harus mengetahui batas otonominya. Jangan mengambil keputusan kritis tanpa persetujuan eksplisit dari pengguna.

### Tingkat Eskalasi / Escalation Levels

1. **Autonomous (Level 1):** Penulisan kode fitur lokal, pembuatan *unit test*, perbaikan *syntax error*.
2. **Consultative (Level 2):** Penambahan pustaka baru (*third-party dependencies*), modifikasi skema basis data minor. (Agen menyarankan, pengguna menyetujui).
3. **Escalated (Level 3):** Penghapusan repositori, perubahan konfigurasi firewall jaringan produksi, *data migration script execution*. (Wajib dihentikan hingga ada izin tertulis dari pengguna).

---

## 📝 Trade-off Matrix & Architecture Decision Records (ADR)

Setiap keputusan arsitektur yang diambil harus dicatat menggunakan format *Architecture Decision Record* (ADR) untuk menjaga transparansi jangka panjang.

### Template ADR Sederhana / Simple ADR Template

```markdown
# ADR-002: Migration to PostgreSQL Connection Pooler

## Status
Accepted

## Context
Aplikasi Express.js sering mengalami error `FATAL: remaining connection slots are reserved...` pada beban trafik tinggi karena setiap instans server membuka koneksi baru tanpa batas.

## Decision
Mengintegrasikan `PgBouncer` sebagai lapisan perantara (*connection pooler*) dengan mode transaksi (*transaction pooling*).

## Consequences
- **Positive:** Latensi inisiasi koneksi turun hingga 70%. Slot koneksi basis data aman dari lonjakan mendadak.
- **Negative:** Fitur *Prepared Statements* bawaan driver PostgreSQL harus dinonaktifkan atau disesuaikan konfigurasinya.
```

---

## 🔄 Reversibility Checks (Pemeriksaan Reversibilitas)

Selalu rancang jalan keluar (*exit strategy*) untuk setiap keputusan yang diambil. Tanya diri Anda: *"Bagaimana cara membatalkan tindakan ini jika sistem mengalami kegagalan fatal pada tahap produksi?"*

### Mekanisme Pengamanan Reversibilitas / Reversibility Mechanisms

- **Database Changes:** Selalu siapkan skrip `down` migration untuk setiap `up` migration yang dibuat.
- **Code Deployment:** Siapkan perintah *rollback* instan (misalnya: `git revert` atau *container tag switching*).
- **API Changes:** Jangan langsung menghapus parameter lama; gunakan dekorator `@deprecated` terlebih dahulu dan dukung dua versi (*backward compatible*) selama masa transisi.

---

## 🚫 Anti-Patterns dalam Decision Making

- **Analysis Paralysis:** Menghabiskan waktu lebih dari 30 menit untuk memilih nama variabel atau detail kecil yang tidak berdampak pada sistem keseluruhan.
- **YAGNI (You Aren't Gonna Need It) Violation:** Membangun infrastruktur *microservices* yang kompleks untuk aplikasi skala kecil yang baru mulai berkembang.
- **Sunk Cost Fallacy:** Memaksakan penggunaan modul yang sering *crash* hanya karena tim telah menghabiskan waktu seminggu untuk menulisnya.

---

*(Setiap keputusan adalah investasi. Lakukan dengan penuh perhitungan dan dokumentasi yang memadai.)*
