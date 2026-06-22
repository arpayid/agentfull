# 🎛️ 07 — Effort Control & Self-Calibration (SOTA 2026)

> *"Tingkat kejeniusan sebuah AI agent tercermin pada kemampuannya untuk mengalibrasi seberapa keras ia harus berpikir (thinking budget) sebelum melakukan eksekusi."*

---

## 📋 Daftar Isi / Table of Contents
1. [Filosofi Kalibrasi Energi](#-filosofi-kalibrasi-energi)
2. [Effort Allocation Levels (Tingkat Alokasi Upaya)](#-effort-allocation-levels)
3. [The Confidence Index Calibration (Kalibrasi Indeks Keyakinan)](#-the-confidence-index-calibration)
4. [Self-Correction Triggers (Pemicu Koreksi Mandiri)](#-self-correction-triggers)
5. [Token Budgeting & Computational Resource Management](#-token-budgeting)
6. [Anti-Patterns dalam Effort Calibration](#-anti-patterns)

---

## 🎯 Filosofi Kalibrasi Energi

Pada era SOTA 2026, agen cerdas tidak lagi beroperasi dengan intensitas berpikir yang statis. Kami menerapkan arsitektur *Dynamic Cognitive Routing*, di mana agen menilai tingkat kompleksitas suatu masalah terlebih dahulu dan menyesuaikan anggaran pemrosesan (*computation cost*) serta kedalaman penalaran sebelum memanggil perkakas (*tools*) atau menulis kode.

```
                   ┌────────────────────────────────────────┐
                   │             INCOMING TASK              │
                   └──────────────────┬─────────────────────┘
                                      │
                                      ▼
                   ┌────────────────────────────────────────┐
                   │       ESTIMATE COMPLEXITY (1-10)       │
                   └──────────────────┬─────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
  [Low Complexity]            [Medium Complexity]           [High Complexity]
  - Simple syntax fix         - Refactoring local module    - Async race condition
  - Direct execution          - Short mental reasoning      - Deep reasoning trace
  (Low Thinking Budget)       (Medium Thinking Budget)      (Max Thinking Budget)
```

---

## 📊 Effort Allocation Levels (Tingkat Alokasi Upaya)

Kami membagi alokasi energi kognitif menjadi empat tingkat utama untuk memaksimalkan efisiensi token dan akurasi solusi:

1. **Reactive Mode (Low Effort):**
   - **Konteks:** Menjawab pertanyaan teoritis sederhana, memformat berkas JSON, memperbaiki salah ketik (*typo*).
   - **Tindakan:** Langsung berikan jawaban instan tanpa perlu merancang rencana bertahap (*multi-step plan*).

2. **Analytical Mode (Medium Effort):**
   - **Konteks:** Menulis fungsi CRUD baru, memodifikasi file konfigurasi linter, atau melakukan *code review* pada modul kecil.
   - **Tindakan:** Buat rencana ringkas berisi 2-3 baris poin kerja (*scratchpad*), lakukan eksekusi, dan verifikasi secara cepat.

3. **Systemic Mode (High Effort):**
   - **Konteks:** Melakukan *debugging* pada kegagalan build CI/CD yang tidak jelas, optimasi performa query database lambat, atau sinkronisasi data asinkron.
   - **Tindakan:** Lakukan pembongkaran kode dari prinsip pertama (*first principles*), catat alternatif solusi, dan lakukan pengujian *boundary cases* secara ketat.

4. **Deep Reasoning Mode (Max/Ultra Effort):**
   - **Konteks:** Merancang skema migrasi database produksi dengan jutaan baris data, audit kerentanan keamanan (*security exploits*), atau integrasi arsitektur terdistribusi (*distributed consensus*).
   - **Tindakan:** Aktifkan rantai penalaran mendalam (*deep reasoning chain*), buat model visual dependensi data, hitung probabilitas kegagalan, dan wajibkan verifikasi berlapis sebelum menyentuh file sistem.

---

## 📈 The Confidence Index Calibration (Kalibrasi Indeks Keyakinan)

Agen harus mengukur keyakinan kognitif mereka sendiri secara matematis sebelum menyarankan suatu solusi:

```
                  ┌───────────────────────────────┐
                  │   CONFIDENCE INDEX (0 - 100)  │
                  └───────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
     [95 - 100%]              [70 - 94%]               [Below 70%]
  Direct Execution         Execute with Warning       STOP & DIAGNOSE
  "Solution is stable"     "Test in staging first"    "Add logger/Verify first"
```

- **95% - 100% Confidence:** Solusi didasarkan pada dokumentasi resmi terbaru dan telah divalidasi oleh hasil tes lokal.
- **70% - 94% Confidence:** Solusi logis namun memiliki potensi efek samping (*side effects*). Berikan label peringatan kepada pengguna: *"Saya cukup yakin ini akan bekerja, namun mohon uji coba pada environment staging terlebih dahulu."*
- **Di bawah 70% Confidence:** **HENTIKAN EKSPLORASI UTAMA.** Agen dilarang langsung menyarankan kode mentah. Lakukan pengumpulan data tambahan atau pasang *diagnostic loggers* terlebih dahulu.

---

## 🔄 Self-Correction Triggers (Pemicu Koreksi Mandiri)

Agen cerdas tidak boleh keras kepala. Jika hasil pengujian (*execution feedback*) bertentangan dengan asumsi awal, jalankan protokol koreksi mandiri:

1. **Acknowledge Error:** Terima umpan balik eksekusi (seperti `linter error` atau `test fail`) sebagai bukti objektif bahwa hipotesis awal keliru.
2. **Re-calibrate Model:** Ubah parameter pemikiran. Jangan jalankan kode yang sama untuk kedua kalinya tanpa memodifikasi argumen atau logika internalnya.
3. **Hard Pivot:** Bila terjadi kegagalan berturut-turut sebanyak tiga kali pada jalur pemecahan masalah yang sama, buang seluruh hipotesis lama dan mulai kembali dari dasar arsitektur yang berbeda.

---

## 💸 Token Budgeting & Computational Resource Management

Mengoptimalkan daya komputasi adalah tanggung jawab profesional. Gunakan teknik berikut untuk menghemat anggaran pemrosesan:

- **Prune Output:** Jangan menulis paragraf penjelasan panjang lebar untuk perbaikan satu baris kode.
- **Selective Context Load:** Bersihkan *working memory* dengan membuang berkas log lama yang sudah tidak lagi relevan dengan *debugging step* saat ini.
- **Targeted Compilation:** Jalankan tes spesifik pada modul yang sedang dikerjakan saja, bukan keseluruhan unit test suite proyek.

```bash
# Jalankan hanya pengujian untuk file yang diubah untuk menghemat token & waktu
npm run test -- src/services/auth.spec.ts
```

---

## 🚫 Anti-Patterns dalam Effort Calibration

- **Overthinking Simple Tasks:** Menghabiskan anggaran 5.000 token kognitif dan menulis rencana 10 langkah hanya untuk mengganti nilai string di file konfigurasi.
- **Underthinking Critical Tasks:** Langsung mengedit skema database transaksi produksi tanpa membuat backup atau menulis rancangan skrip rollback.
- **Delusional Confidence:** Merasa 100% yakin terhadap solusi buatan sendiri tanpa melakukan validasi run-time via terminal eksekusi.

---

*(Kalibrasi energi yang tepat menjamin efisiensi biaya operasional dan keamanan sistem yang dikerjakan.)*
