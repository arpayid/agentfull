# 🤝 22 — Dynamic HITL (Human-in-the-Loop) Negotiation

> *"Tingkat kebebasan bertindak agen harus proporsional dengan potensi risiko kerusakan sistem."*

---

## 📋 Daftar Isi

1. [Filosofi HITL Dinamis](#-filosofi-hitl-dinamis)
2. [Klasifikasi Risiko Tindakan](#-klasifikasi-risiko-tindakan)
3. [Alur Negosiasi Otorisasi](#-alur-negosiasi-otorisasi)
4. [Mekanisme Rollback Instan](#-mekanisme-rollback-instan)

---

## 🎯 Filosofi HITL Dinamis

Dynamic HITL Negotiation adalah **sistem persetujuan runtime**. Daripada meminta konfirmasi pengguna pada *setiap* tool call yang menjengkelkan, agen menilai tingkat risiko tindakannya secara dinamis dan hanya berhenti ketika risiko tergolong *Medium* atau *High*.

---

## 📊 Klasifikasi Risiko Tindakan

| Level Risiko | Contoh Tindakan | Wewenang Eksekusi |
| :--- | :--- | :--- |
| **Low** | Membaca file (`read`), pencarian file (`glob`, `grep`), test kompilasi. | **Otonom Penuh** (Tidak butuh konfirmasi). |
| **Medium** | Pengeditan file (`edit`, `write`), modifikasi package dependency. | **Pemberitahuan Singkat** (Jelaskan perubahan di chat). |
| **High** | Menghapus direktori (`rm`), memodifikasi schema DB produksi. | **Persetujuan Mutlak** (Wajib konfirmasi `ya/tidak` di chat). |

---

## ⚙️ Alur Negosiasi Otorisasi

Jika tindakan diklasifikasikan sebagai **High Risk**:
1. Berikan analisis dampak buruk (worst-case scenario).
2. Sediakan opsi mitigasi (misal: "Saya telah mem-backup database sebelum mengeksekusi migrasi ini").
3. Minta instruksi otorisasi secara formal.
