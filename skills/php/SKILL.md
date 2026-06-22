---
name: PHP Backend Engineering
description: Deep dive into PHP execution model, reference counting GC, Swoole concurrency, and Composer packaging.
---

# 🛠️ PHP Backend Engineering

## 1. Memory Management & Lifecycles
PHP secara tradisional beroperasi di bawah model eksekusi **Shared-Nothing**, di mana setiap request HTTP menginisialisasi seluruh state aplikasi dari awal dan membersihkan semua memori yang dialokasikan ketika request selesai (request lifecycle).

### Reference Counting
- PHP mengelola memori di dalam engine internal Zend menggunakan sistem *Reference Counting* pada struktur data `zval`.
- Setiap kali variabel disalin atau dirujuk, counter referensi (`refcount`) dinaikkan.
- Ketika variabel keluar dari scope atau dihancurkan dengan `unset()`, `refcount` diturunkan. Jika mencapai nol, memori dialokasikan ulang.

### Circular Reference Garbage Collector
Reference counting murni memiliki kelemahan jika terjadi referensi melingkar (misal objek A merujuk B, dan objek B merujuk A).
- Zend GC melacak objek-objek potensial ini dalam struktur antrean terpisah.
- Ketika antrean penuh (default 10.000 root elemen), GC menjalankan algoritma pemindaian untuk mendeteksi siklus melingkar yang terisolasi dari variabel aktif, lalu menghapusnya untuk mencegah kebocoran memori.

---

## 2. Concurrency & Parallelism
Secara historis, PHP adalah bahasa yang sinkronus dan dijalankan secara multi-process melalui PHP-FPM. Namun, ekosistem modern telah menyediakan alat konkurensi canggih.

### Async dan Coroutine
- **Swoole / RoadRunner**: Ekstensi PHP berkinerja tinggi yang mengubah model eksekusi PHP menjadi berbasis event loop yang persisten (mirip Node.js atau Go). Menggunakan coroutine untuk I/O non-blocking (database, file, network).
- **Fibers (PHP 8.1)**: Mekanisme konkurensi kooperatif tingkat rendah (green threads) yang diintegrasikan langsung ke core PHP. Serat (Fiber) memungkinkan pengembang menjeda eksekusi fungsi tanpa memblokir seluruh proses utama, membentuk fondasi framework async seperti Amphp atau ReactPHP.

---

## 3. Dependency & Build Systems
Satu-satunya sistem manajemen dependensi standar di PHP adalah **Composer**.

### Composer Workflow
- `composer.json`: Mendefinisikan paket eksternal yang dibutuhkan oleh proyek beserta aturan autoloading (seperti PSR-4).
- `composer.lock`: Mengunci versi paket dependensi secara spesifik dan menjamin semua tim menggunakan versi yang identik.
- Autoloading: Composer menghasilkan file autoloader berkinerja tinggi yang mendefinisikan pemetaan kelas ke file PHP fisik secara otomatis pada saat bootstrap awal.

---

## 4. Real-world Code Implementation
Berikut adalah contoh implementasi runtime asinkronus sederhana menggunakan Fibers di PHP 8.1 untuk melakukan query data secara non-blocking.

```php
<?php

class AsyncTask {
    private Fiber $fiber;

    public function __construct(callable $callback) {
        $this.fiber = new Fiber($callback);
    }

    public function start(): void {
        $this.fiber->start();
    }

    public function resume(mixed $value = null): void {
        if ($this.fiber->isSuspended()) {
            $this.fiber->resume($value);
        }
    }

    public function isFinished(): bool {
        return $this.fiber->isTerminated();
    }
}

class EventLoop {
    private array $tasks = [];

    public function add(AsyncTask $task): void {
        $this.tasks[] = $task;
    }

    public function run(): void {
        while (!empty($this.tasks)) {
            foreach ($this.tasks as $key => $task) {
                if (!$task->isFinished()) {
                    $task->resume();
                } else {
                    unset($this.tasks[$key]);
                }
            }
            // Small sleep to emulate polling event
            usleep(1000);
        }
    }
}

// Demo usage
$loop = new EventLoop();

$loop->add(new AsyncTask(function() {
    echo "Task 1: Fetching database query...\n";
    // Simulate non-blocking pause
    Fiber::suspend();
    echo "Task 1: Database query fetched!\n";
}));

$loop->add(new AsyncTask(function() {
    echo "Task 2: Downloading API response...\n";
    // Simulate non-blocking pause
    Fiber::suspend();
    echo "Task 2: API download completed!\n";
}));

echo "Starting event loop:\n";
$loop->run();
echo "Execution finished.\n";
```
