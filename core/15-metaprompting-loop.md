# 🧠 15 — Meta-Prompting & Self-Correction Loop

> *"Sebuah sistem cerdas tidak hanya memperbaiki kodenya, ia juga memperbaiki cara ia menerima instruksi."*

---

## 📋 Daftar Isi

1. [Filosofi Meta-Prompting](#-filosofi-meta-prompting)
2. [Evaluasi Prompt Dinamis](#-evaluasi-prompt-dinamis)
3. [Alur Koreksi Mandiri (Self-Correction Loop)](#-alur-koreksi-mandiri-self-correction-loop)
4. [Panduan Optimasi Konteks](#-panduan-optimasi-konteks)

---

## 🎯 Filosofi Meta-Prompting

Meta-Prompting adalah proses di mana agen **menganalisis prompt atau instruksi internalnya sendiri** untuk melihat apakah ada instruksi yang ambigu atau kontradiktif, kemudian melakukan pembaruan struktur berpikir secara real-time.

---

## 🔄 Alur Koreksi Mandiri (Self-Correction Loop)

Jika instruksi yang dijalankan memicu hasil yang kurang memuaskan, jalankan alur ini:

```
┌──────────────────────────────────────┐
│  Analisis Hasil Kerja                │
└──────────────────┬───────────────────┘
                   │
┌──────────────────┴───────────────────┐
│  Apakah instruksi awal terlalu luas? │
└──────────────────┬───────────────────┘
                   │
        [YA] ──────┴─────── [TIDAK]
         │                     │
┌────────┴──────────┐   ┌──────┴───────────┐
│ Rancang Ulang     │   │ Lanjutkan        │
│ Sub-instruksi     │   │ Proses           │
│ Lebih Spesifik    │   └──────────────────┘
└───────────────────┘
```

---

## 📋 Panduan Optimasi Konteks

* **Pruning Redundansi**: Buang instruksi yang tidak lagi relevan dengan kondisi codebase saat ini.
* **Prioritisasi Constraints**: Letakkan aturan keamanan dan batas eksekusi di bagian paling atas tumpukan instruksi (system instruction).
