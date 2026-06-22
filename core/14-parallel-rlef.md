# ⚡ 14 — Parallel RLEF Execution Protocol

> *"Menguji satu per satu itu lambat. Menjalankan skenario paralel secara asinkronus mempercepat iterasi perbaikan."*

---

## 📋 Daftar Isi

1. [Filosofi RLEF Paralel](#-filosofi-rlef-paralel)
2. [Arsitektur RLEF Paralel (Parallel Execution Architecture)](#-arsitektur-rlef-paralel-parallel-execution-architecture)
3. [Eksekusi Pengujian Asinkronus (Asynchronous Test Execution)](#-eksekusi-pengujian-asinkronus-asynchronous-test-execution)
4. [Manajemen Port Dinamis untuk Testing (Dynamic Port Allocation)](#-manajemen-port-dinamis-untuk-testing-dynamic-port-allocation)
5. [Deteksi Konflik & Race Conditions (Race Condition Detection)](#-deteksi-konflik--race-conditions-race-condition-detection)
6. [Implementasi Kode Pemantau Paralel (Parallel Runner Code Fragment)](#-implementasi-kode-pemantau-paralel-parallel-runner-code-fragment)
7. [Langkah Pemulihan Cepat (Recovery Playbook)](#-langkah-pemulihan-cepat-recovery-playbook)
8. [Anti-Patterns RLEF Paralel](#-anti-patterns-rlef-paralel)

---

## 🎯 Filosofi RLEF Paralel

RLEF (Reinforcement Learning from Execution Feedback) tradisional berjalan secara sekuensial. Protokol ini mengajarkan agen untuk **mengeksekusi dan menganalisis beberapa varian perbaikan secara paralel** menggunakan background processes terminal untuk memangkas waktu pengerjaan. Ini sangat bermanfaat untuk pengujian kode di berbagai skenario secara simultan.

---

## 🏗️ Arsitektur RLEF Paralel

```
                         ┌──────────────────────────┐
                         │   Agent Parallel Spawn   │
                         └──────┬────────────┬──────┘
                                │            │
            ┌───────────────────┘            └───────────────────┐
            ▼ Varian A (Port 8081)                               ▼ Varian B (Port 8082)
┌───────────────────────┐                    ┌───────────────────────┐
│ Run Test Suite A      │                    │ Run Test Suite B      │
└───────────┬───────────┘                    └───────────┬───────────┘
            │                                            │
            └───────────────────┐            ┌───────────┘
                                ▼            ▼
                         ┌──────────────────────────┐
                         │ Evaluasi Output & Feedback│
                         └──────────────────────────┘
```

---

## ⚡ Eksekusi Pengujian Asinkronus

Saat menguji perubahan pada sistem berskala sedang:
* **Background Runners**: Jalankan suite pengujian menggunakan operator background (`&`) atau runner parallel bawaan (seperti `jest --maxWorkers=4`).
* **Multi-port Testing**: Uji beberapa instance API secara bersamaan di port berbeda untuk membandingkan kinerja atau kestabilan sebelum memilih versi terbaik.

### Contoh Command Menjalankan Multi-Instance:
```bash
# Run multiple instances with distinct ports in the background
node app.js --port 8081 > logs_8081.log 2>&1 &
PID_1=$!

node app.js --port 8082 > logs_8082.log 2>&1 &
PID_2=$!

# Wait for 3 seconds to let servers start
sleep 3

# Send concurrent test requests
curl -s http://localhost:8081/health
curl -s http://localhost:8082/health

# Clean up processes
kill $PID_1 $PID_2
```

---

## 🪙 Manajemen Port Dinamis untuk Testing

Untuk mencegah tabrakan port pada server lokal pengujian, sistem menggunakan skema alokasi port dinamis seperti di bawah ini:

| Nama Service | Port Default | Port Testing A | Port Testing B |
| :--- | :--- | :--- | :--- |
| `Authentication` | `3000` | `30001` | `30002` |
| `User Registry` | `3001` | `30011` | `30012` |
| `Payments DB` | `5432` | `54321` | `54322` |

---

## 🔍 Deteksi Konflik & Race Conditions

Saat menjalankan proses secara paralel, waspadai:
1. **Konflik File Database**: Pastikan database pengujian diisolasi per thread (misal menggunakan SQLite in-memory atau DB schema berbeda).
2. **Resource Lock**: Hindari menulis ke file log yang sama dari beberapa proses pengujian yang berjalan bersamaan.
3. **Zombies Processes**: Pastikan skrip cleanup dijalankan meskipun pengujian utama gagal tengah jalan.

---

## 💻 Implementasi Kode Pemantau Paralel

Berikut skrip Node.js sederhana untuk memantau status eksekusi beberapa sub-proses pengujian secara asinkronus:

```javascript
const { exec } = require('child_process');

function runTestInstance(command, instanceName) {
  return new Promise((resolve) => {
    console.log(`[RLEF] Starting ${instanceName}...`);
    const process = exec(command, (error, stdout, stderr) => {
      if (error) {
        resolve({ instanceName, status: 'failed', error: stderr || error.message });
      } else {
        resolve({ instanceName, status: 'passed', output: stdout });
      }
    });
  });
}

async function runParallelRlef() {
  const tasks = [
    runTestInstance('jest src/auth.test.js', 'Auth_Test_Suite'),
    runTestInstance('jest src/payment.test.js', 'Payment_Test_Suite')
  ];
  
  const results = await Promise.all(tasks);
  console.log('[RLEF] All parallel tests completed:', results);
}

runParallelRlef();
```

---

## 🛠️ Langkah Pemulihan Cepat

Jika salah satu instance uji gagal mengembalikan kode sukses:
1. **Kumpulkan Log**: Gunakan `tail -n 50 logs_8081.log` untuk melihat stack trace spesifik dari instance tersebut.
2. **Hentikan Sisa Thread**: Jalankan `pkill -P $$` untuk menghentikan semua sub-proses (child processes) yang masih berjalan di latar belakang.
3. **Lakukan Rollback**: Segera kembalikan file yang bermasalah menggunakan `git checkout -- <file>` sebelum mencoba kembali.

---

## ⚠️ Anti-Patterns RLEF Paralel

* ❌ **Shared States**: Menjalankan tes paralel dengan database yang sama tanpa isolasi transaksi.
* ❌ **Ignoring PID**: Menjalankan background process tanpa menyimpan process ID (`$!`), yang menyebabkan proses yatim piatu (zombie process).
* ❌ **Too Many Workers**: Menjalankan thread lebih banyak dari core CPU host, menyebabkan thrashing dan CPU resource starvation.
