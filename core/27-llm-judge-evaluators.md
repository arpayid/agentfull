# 🔍 27 — LLM-as-a-Judge Evaluation Framework

> *"Menilai kualitas keluaran menggunakan model penalaran khusus sebelum menyajikannya ke hadapan pengguna."*

---

## 📋 Daftar Isi

1. [Filosofi LLM-as-a-Judge](#-filosofi-llm-as-a-judge)
2. [Format Kriteria Penilaian](#-format-kriteria-penilaian)
3. [Alur Evaluasi Internal](#-alur-evaluasi-internal)
4. [Fallback Sistem Penilaian](#-fallback-sistem-penilaian)

---

## 🎯 Filosofi LLM-as-a-Judge

Sebelum agen menyajikan solusi akhir, ia memanggil **instansi model penalaran terpisah (Judge)** yang bertugas murni sebagai penilai kualitas (Code Reviewer otomatis). Model Judge mengevaluasi kode berdasarkan kriteria kekokohan logika, mitigasi edge-cases, dan kepatuhan constraints tanpa dipengaruhi oleh bias pembuat kode asli.

---

## 📊 Format Kriteria Penilaian

Model Judge memberikan skor numerik dan justifikasi:

| Kriteria Penilaian | Bobot | Target Minimal | Tindakan jika Gagal |
| :--- | :--- | :--- | :--- |
| **Logic Correctness** | 40% | $9.0 / 10$ | Kirim kembali ke implementer agent untuk diperbaiki. |
| **Security Auditing** | 30% | $10.0 / 10$ | Blokir kode dan jalankan static analyzer ulang. |
| **Clarity & Indentation** | 30% | $8.0 / 10$ | Jalankan auto-formatter lokal. |

---

## ⚙️ Alur Evaluasi Internal

Jika skor Judge di bawah batas minimal, agen secara otonom melakukan *backtracking* (Modul 08) ke tahap implementasi dengan menyertakan log review dari Judge sebagai konteks perbaikan.
