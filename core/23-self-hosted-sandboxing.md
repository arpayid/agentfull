# 📦 23 — Self-Hosted Sandboxing & MicroVM Isolation

> *"Keamanan infrastruktur host pengguna adalah prioritas mutlak di atas seluruh pencapaian otonomi agen."*

---

## 📋 Daftar Isi

1. [Filosofi Sandbox Mandiri](#-filosofi-sandbox-mandiri)
2. [Pola Isolasi Lingkungan](#-pola-isolasi-lingkungan)
3. [Arsitektur Eksekusi Sandbox](#-arsitektur-eksekusi-sandbox)
4. [Langkah Pemulihan & Cleanup](#-langkah-pemulihan--cleanup)

---

## 🎯 Filosofi Sandbox Mandiri

Ketika agen memproses input eksternal (seperti menguji kode yang ditulis oleh kontributor publik), mengeksekusi kode tersebut secara langsung pada mesin host sangat berbahaya. Seluruh eksekusi runtime wajib diisolasi di dalam **MicroVM atau sandbox khusus**.

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

## ⚙️ Arsitektur Eksekusi Sandbox

*   **Stateless Operations**: Runtime pengujian harus dibuang (destroyed) setelah kompilasi selesai.
*   **No Network Access (Optional)**: Secara default, matikan akses internet luar (`--network none`) saat menjalankan file binary tidak dikenal demi mencegah serangan eksfiltrasi data.
