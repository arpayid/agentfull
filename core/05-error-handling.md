# 🔧 05 — Error Handling & Recovery (SOTA 2026)

> *"Error bukan sekadar pesan kegagalan, melainkan sinyal diagnostik berharga yang jika ditangani secara sistematis akan membawa sistem kembali ke kondisi stabil secara otonom."*

---

## 📋 Daftar Isi / Table of Contents
1. [Filosofi Manajemen Error](#-filosofi-manajemen-error)
2. [Diagnostic Log Scanning (Pemindaian Log Diagnostik)](#-diagnostic-log-scanning)
3. [Component Isolation & Boundary Testing](#-component-isolation)
4. [Incremental Fixing Protocol](#-incremental-fixing-protocol)
5. [Rollback Verification & Safeguards](#-rollback-verification)
6. [Anti-Patterns dalam Error Handling](#-anti-patterns)

---

## 🎯 Filosofi Manajemen Error

Pada standar SOTA 2026, penanganan *error* tidak hanya fokus pada penulisan blok `try-catch`, melainkan pada ketahanan sirkuit (*circuit resilience*), toleransi kesalahan (*fault tolerance*), dan pemulihan otomatis (*self-healing capability*).

```
                      ┌────────────────────────┐
                      │    ERROR ENCOUNTERED   │
                      └───────────┬────────────┘
                                  │
                                  ▼
                      ┌────────────────────────┐
                      │   CIRCUIT BREAKS /     │
                      │    GRACEFUL FALLBACK   │
                      └───────────┬────────────┘
                                  │
                                  ▼
                      ┌────────────────────────┐
                      │  ROOT CAUSE DIAGNOSIS  │
                      └───────────┬────────────┘
                                  │
                                  ▼
                      ┌────────────────────────┐
                      │   INCREMENTAL RECOVERY │
                      └────────────────────────┘
```

---

## 📖 Diagnostic Log Scanning (Pemindaian Log Diagnostik)

Jangan panik saat melihat ribuan baris log kesalahan. Gunakan alat penyaring berbasis terminal (*cli filters*) untuk memotong kebisingan log (*noise*) dan mencari pesan kesalahan utama (*root cause*).

### Perintah Pemindaian Log / Log Scanning Commands

```bash
# Contoh 1: Menyaring error level FATAL atau ERROR pada berkas log aplikasi
grep -E "FATAL|ERROR" /var/log/nginx/error.log | tail -n 50

# Contoh 2: Mencari entri transaksi berdasarkan Correlation ID unik
grep "tx-uuid-8890ab" /var/log/apps/payment-gateway.json | jq '.message, .timestamp, .level'

# Contoh 3: Memantau log container Docker secara real-time dengan filter pengecualian
docker logs --tail 100 -f api-service 2>&1 | grep -v "GET /healthz"
```

---

## 🔬 Component Isolation & Boundary Testing

Isolasi kesalahan dengan memotong rantai komunikasi (*inter-service dependencies*) untuk melokalisasi masalah pada satu komponen spesifik.

### Strategi Isolasi Batas / Boundary Isolation Strategy

- **Mock External APIs:** Ganti panggilan pihak ketiga (*third-party calls*) dengan respon buatan (*mock response*) untuk melihat apakah masalah ada pada layanan lokal.
- **Bypass Cache:** Paksa eksekusi langsung ke basis data dengan mem-bypass Redis cache layer untuk memverifikasi konsistensi data.
- **Dry-Run Mode:** Jalankan skrip eksekusi dalam mode simulasi (*dry-run*) untuk memeriksa validasi skema tanpa mengubah keadaan data sesungguhnya.

```bash
# Contoh dry-run migrasi database
npm run db:migrate -- --dry-run
```

---

## 🔨 Incremental Fixing Protocol

Jangan pernah mengubah banyak bagian kode secara bersamaan saat memperbaiki *bug*. Terapkan protokol satu perbaikan per iterasi (*one-fix-per-iteration*).

```
              ┌────────────────────────────────────────┐
              │          HYPOTHESIS FORMULATION        │
              └──────────────────┬─────────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │           APPLY SINGLE CHANGE          │
              └──────────────────┬─────────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │         VERIFY VIA AUTOMATED TEST      │
              └──────────────────┬─────────────────────┘
                                 │
                     ┌───────────┴───────────┐
                     │                       │
               [Test Passed]           [Test Failed]
                     │                       │
                     ▼                       ▼
              ┌──────────────┐        ┌──────────────┐
              │ Commit Fix   │        │ Revert Change│
              └──────────────┘        └──────────────┘
```

---

## ⏮️ Rollback Verification & Safeguards

Sebelum menerapkan perbaikan apapun ke server produksi (*production cluster*), pastikan ada prosedur pembatalan (*rollback*) yang terdokumentasi dan siap dijalankan seketika.

### Daftar Periksa Kesiapan Rollback / Rollback Checklist

- [ ] Simpan salinan cadangan status commit git saat ini: `git rev-parse HEAD`.
- [ ] Buat berkas dump basis data sebelum memodifikasi kolom tabel.
- [ ] Pastikan *monitoring alert* diaktifkan selama proses penerapan perbaikan.

```bash
# Backup database PostgreSQL sebelum tindakan darurat
pg_dump -U postgres -d payment_db -F c -b -v -f /tmp/backup_pre_fix.dump
```

---

## 🚫 Anti-Patterns dalam Error Handling

- **The Silent Swallower:** Menelan kesalahan secara diam-diam dalam kode dengan blok `catch(e) {}` kosong, tanpa log atau metrik pelaporan.
- **Cascading Outages:** Tidak menggunakan batas waktu koneksi (*timeout*) saat memanggil API luar, sehingga seluruh pool koneksi aplikasi habis menunggu respon eksternal.
- **Brute Force Debugging:** Terus menerus mengganti baris kode secara acak dengan harapan program akan berjalan tanpa mengetahui akar masalah yang sebenarnya.

---

*(Sistem yang tangguh bukanlah sistem yang bebas dari error, melainkan sistem yang mampu pulih dengan cepat tanpa kehilangan integritas data.)*
