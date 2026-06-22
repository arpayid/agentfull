---
name: Rust System Programming
description: Deep dive into Rust ownership, borrowing, lifetimes, async safety, and cargo builds.
---

# 🛠️ Rust System Programming

## 1. Memory Management & Lifecycles
Rust tidak menggunakan garbage collector (GC) maupun alokasi/deallokasi manual secara eksplisit seperti C. Rust menjamin keamanan memori pada saat kompilasi melalui sistem **Ownership, Borrowing, dan Lifetimes**.

### Ownership Rules
1. Setiap nilai di Rust memiliki variabel yang disebut sebagai *owner* (pemiliknya).
2. Hanya boleh ada satu owner pada satu waktu.
3. Ketika owner keluar dari scope (`drop`), nilai tersebut akan otomatis dihapus dari memori.

### Borrowing (Peminjaman)
Kita dapat meminjam referensi ke data tanpa mengambil alih ownership. Aturan peminjaman sangat ketat untuk menghindari data race pada waktu kompilasi:
- Kita dapat memiliki banyak referensi yang tidak dapat diubah (immutable borrows: `&T`).
- Kita hanya dapat memiliki tepat satu referensi yang dapat diubah (mutable borrow: `&mut T`) pada satu waktu dalam scope tertentu.
- Immutable borrow dan mutable borrow tidak boleh ada secara bersamaan dalam scope yang tumpang tindih.

### Lifetimes
Lifetime adalah anotasi generik yang memberi tahu compiler (`rustc`) hubungan antara durasi hidup berbagai referensi. Tujuannya adalah mencegah *dangling references* (referensi ke memori yang sudah didealokasikan).

---

## 2. Concurrency & Parallelism
Rust menyediakan abstraksi konkurensi yang aman dengan motto "fearless concurrency". Hal ini didukung oleh type system melalui marker trait `Send` dan `Sync`.
- **`Send`**: Menandakan bahwa ownership dari tipe data tersebut aman dipindahkan antar thread.
- **`Sync`**: Menandakan bahwa aman untuk mengakses referensi data tersebut secara konkuren dari beberapa thread (`&T` adalah `Send`).

### Concurrency Primitives
- **`std::thread`**: Digunakan untuk parallelism berbasis OS thread.
- **`Arc<T>` (Atomic Reference Counted)**: Smart pointer untuk membagikan kepemilikan data antar thread secara aman.
- **`Mutex<T>` (Mutual Exclusion)** dan **`RwLock<T>`**: Menyediakan interior mutability untuk sinkronisasi data antar thread.
- **Async/Await & Futures**: Model konkurensi kooperatif berbasis *single or multi-threaded event loop* (executor seperti `tokio`). Masa hidup Future dievaluasi secara malas (lazy) hingga dijalankan oleh executor.

---

## 3. Dependency & Build Systems
Sistem build resmi Rust adalah **Cargo**. Cargo menangani manajemen dependensi, kompilasi, pembuatan dokumentasi, dan eksekusi test runner.

### Cargo Configuration (`Cargo.toml`)
- Dependensi dideklarasikan dengan versi semantik (semver).
- Mendukung fitur flags modular untuk optimasi build compile-time (`[features]`).
- Profile kompilasi dapat diatur secara detail untuk mode dev maupun release (`[profile.release]`) dengan opsi seperti `lto = true` (Link-Time Optimization) dan `codegen-units = 1` untuk ukuran biner minimum dan performa maksimum.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi thread-safe queue yang memanfaatkan `Arc`, `Mutex`, dan `Condvar` untuk sinkronisasi thread produsen-konsumen di Rust.

```rust
use std::collections::VecDeque;
use std::sync::{Arc, Condvar, Mutex};
use std::thread;

pub struct SharedQueue<T> {
    queue: Mutex<VecDeque<T>>,
    condvar: Condvar,
}

impl<T> SharedQueue<T> {
    pub fn new() -> Self {
        Self {
            queue: Mutex::new(VecDeque::new()),
            condvar: Condvar::new(),
        }
    }

    pub fn push(&self, item: T) {
        let mut q = self.queue.lock().unwrap();
        q.push_back(item);
        self.condvar.notify_one();
    }

    pub fn pop(&self) -> T {
        let mut q = self.queue.lock().unwrap();
        while q.is_empty() {
            q = self.condvar.wait(q).unwrap();
        }
        q.pop_front().unwrap()
    }
}

fn main() {
    let queue = Arc::new(SharedQueue::new());
    
    // Spawn Consumer Thread
    let q_clone = Arc::clone(&queue);
    let handle = thread::spawn(move || {
        for _ in 0..3 {
            let val = q_clone.pop();
            println!("Consumed: {}", val);
        }
    });

    // Producer logic in main thread
    queue.push(10);
    queue.push(20);
    queue.push(30);

    handle.join().unwrap();
}
```
