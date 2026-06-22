# ⚡ 26 — Reactive Event-Driven Agent Loops

> *"Agen masa depan tidak lagi menunggu giliran bertindak; mereka bereaksi terhadap perubahan lingkungan secara instan."*

---

## 📋 Daftar Isi

1. [Filosofi Event-Driven](#-filosofi-event-driven)
2. [Pola Loop Reaktif (Reactive Loop Architecture)](#-pola-loop-reaktif-reactive-loop-architecture)
3. [Perbandingan dengan Polling Loop (Polling vs Reactive Loops)](#-perbandingan-dengan-polling-loop-polling-vs-reactive-loops)
4. [Skema Trigger & Event Handler (Trigger & Event Handler Schema)](#-skema-trigger--event-handler-trigger--event-handler-schema)
5. [Implementasi File Watcher Node.js (Node.js File System Watcher Script)](#-implementasi-file-watcher-nodejs-nodejs-file-system-watcher-script)
6. [Mekanisme Penanganan Event Asinkronus (Async Event Handling)](#-mekanisme-penanganan-event-asinkronus-async-event-handling)
7. [Anti-Patterns Loop Reaktif](#-anti-patterns-loop-reaktif)

---

## 🎯 Filosofi Event-Driven

Sistem agen tradisional beroperasi menggunakan *polling loop* linier (bertanya $\rightarrow$ bertindak $\rightarrow$ menunggu). Pola **Event-Driven** (terinspirasi dari runtime seperti *Chidori*) memungkinkan agen mendaftarkan event listener pada workspace, seperti perubahan berkas (*file changes*), kemunculan log baru, atau sinyal proses dari background task. Agen segera bertindak ketika trigger diaktifkan tanpa membuang token untuk memeriksa status secara terus-menerus.

---

## 🏗️ Pola Loop Reaktif

Event Router mendistribusikan sinyal masukan secara paralel ke sub-system handler yang sesuai:

```
         ┌─────────────────────────────────────────────────────┐
         │                 EVENT ROUTER                        │
         └─┬─────────────────────┬───────────────────────┬─────┘
           │                     │                       │
 ┌────────┴──────────┐ ┌────────┴──────────┐ ┌──────────┴────────┐
 │ File System Event │ │ compiler/linter   │ │ User Abort Signal │
 │ (e.g. watch fs)   │ │ (error output)    │ │ (cancel command)  │
 │                   │ │                   │ │                   │
 └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
           ▼                     ▼                     ▼
      [Re-compile]          [Self-heal]           [Rollback]
```

---

## 📊 Perbandingan dengan Polling Loop

| Parameter Pembanding | Polling Loop | Reactive Event Loop |
| :--- | :--- | :--- |
| **Konsumsi CPU** | Tinggi (Mengulang pembacaan disk) | Rendah (Menunggu event kernel OS) |
| **Respon Waktu (Latency)** | Lambat (Ditentukan interval polling) | Instan (Berdasarkan interrupt system) |
| **Peluang Token Bloat** | Tinggi (Status dikirim berkali-kali) | Rendah (Hanya dikirim saat ada perubahan) |

---

## ⚙️ Skema Trigger & Event Handler

Agen mengonfigurasi handler asinkronus untuk bereaksi terhadap perubahan state:

* `onFileChange`: Memicu linter check otomatis hanya pada modul yang dimodifikasi.
* `onProcessExit`: Memicu analisis recovery (Modul 05) jika proses background mati mendadak.
* `onResourceLimitAlert`: Menghentikan atau membatasi eksekusi model jika budget token bulanan/sesi habis (Modul 21).

---

## 💻 Implementasi File Watcher Node.js

Berikut adalah skrip Node.js menggunakan modul bawaan `fs` untuk memantau perubahan file kode secara real-time dan memicu tindakan otomatis dari agen:

```javascript
const fs = require('fs');
const { exec } = require('child_process');

class WorkspaceWatcher {
  constructor(watchDir) {
    this.watchDir = watchDir;
    this.debounceTimer = null;
  }

  start() {
    console.log(`[Watcher] Monitoring workspace changes in: ${this.watchDir}...`);
    
    fs.watch(this.watchDir, { recursive: true }, (eventType, filename) => {
      if (filename && filename.endsWith('.ts')) {
        // Debounce to prevent multiple triggers in short succession
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
          this.handleEvent('file_change', filename);
        }, 300);
      }
    });
  }

  handleEvent(event, details) {
    console.log(`\n⚡ [Event Triggered] Type: ${event}, Target: ${details}`);
    if (event === 'file_change') {
      // Trigger compiler check immediately
      exec('npm run lint', (err, stdout) => {
        if (err) {
          console.log('[Watcher] Lint error detected. Notify self-healing module.');
        } else {
          console.log('[Watcher] Lint passed. Environment is healthy.');
        }
      });
    }
  }
}

// Usage Example
// const watcher = new WorkspaceWatcher('./src');
// watcher.start();
```

---

## 🛠️ Mekanisme Penanganan Event Asinkronus

Ketika event reaktif memicu tindakan perbaikan:
1. **Mutex Lock**: Lock workspace agar sub-agent lain tidak mengubah file secara bersamaan selama proses build berjalan.
2. **Batching Events**: Kumpulkan beberapa modifikasi file dalam rentang waktu 1 detik menjadi satu event tunggal untuk menghemat konsumsi kompilasi.
3. **Queue Management**: Urutkan prioritas event. Sinyal pembatalan (User Abort) harus selalu diproses terlebih dahulu sebelum event kompilasi berjalan.

---

## ⚠️ Anti-Patterns Loop Reaktif

* ❌ **Watcher Loop Cascades**: File hasil kompilasi (misal `/dist/`) ikut dipantau oleh watcher, menyebabkan loop pemicu (trigger loop) tanpa akhir.
* ❌ **Missing Debounce**: Membiarkan trigger langsung menyala pada setiap karakter yang diketik, yang menyebabkan sistem kelebihan beban pemrosesan (CPU throttling).
* ❌ **Shared Non-Atomic State**: Mengedit state agen dari beberapa event listener secara simultan tanpa mekanisme penguncian (mutex locking).
