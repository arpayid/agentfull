# ⚡ 26 — Reactive Event-Driven Agent Loops

> *"Agen masa depan tidak lagi menunggu giliran bertindak; mereka bereaksi terhadap perubahan lingkungan secara instan."*

---

## 📋 Daftar Isi

1. [Filosofi Event-Driven](#-filosofi-event-driven)
2. [Pola Loop Reaktif (Reactive Loop Pattern)](#-pola-loop-reaktif-reactive-loop-pattern)
3. [Trigger & Event Handler](#-trigger--event-handler)
4. [Keuntungan dibanding Polling Loop](#-keuntungan-dibanding-polling-loop)

---

## 🎯 Filosofi Event-Driven

Sistem agen tradisional beroperasi menggunakan *polling loop* linier (bertanya $\rightarrow$ bertindak $\rightarrow$ menunggu). Pola **Event-Driven** (terinspirasi dari runtime seperti *Chidori*) memungkinkan agen mendaftarkan event listener pada workspace, seperti perubahan berkas (*file changes*), kemunculan log baru, atau sinyal proses dari background task.

---

## 🏗️ Pola Loop Reaktif (Reactive Loop Pattern)

```
        ┌─────────────────────────────────────────────────────┐
        │                 EVENT ROUTER                        │
        └─┬─────────────────────┬───────────────────────┬─────┘
          │                     │                       │
 ┌────────┴──────────┐ ┌────────┴──────────┐ ┌──────────┴────────┐
 │ File System Event │ │ compiler/linter   │ │ User Abort Signal │
 │ (e.g. watch fs)   │ │ (error output)    │ │ (cancel command)  │
 └───────────────────┘ └───────────────────┘ └───────────────────┘
```

---

## ⚙️ Trigger & Event Handler

Agen harus mengonfigurasi handler asinkronus:
*   `onFileChange`: Memicu linter check otomatis hanya pada modul yang dimodifikasi.
*   `onProcessExit`: Memicu analisis recovery (Modul 05) jika proses background mati mendadak.
