---
name: JavaScript Core Mechanics
description: Deep dive into JavaScript V8 engine, Event Loop, closures, and npm/pnpm.
---

# 🛠️ JavaScript Core Mechanics

## 1. Memory Management & Lifecycles
JavaScript dikelola secara otomatis oleh engine runtime (seperti V8 pada Node.js/Chrome) menggunakan skema heap memory yang diatur oleh **Generational Garbage Collector**.

### V8 Heap Segmentation
1. **New Space**: Area kecil untuk alokasi objek baru yang berumur pendek. Manajemen memori di sini sangat cepat menggunakan algoritma *Scavenge (Copy Semispace)*.
2. **Old Space**: Objek yang bertahan dari beberapa siklus di New Space dipindahkan ke sini. Menggunakan algoritma *Mark-Sweep-Compact* yang lebih lambat namun efisien untuk ruang besar.
3. **Large Object Space**: Objek yang ukurannya melebihi batas New Space dialokasikan langsung di sini tanpa dipindahkan oleh GC.

### Garbage Collector Mechanics
GC mendeteksi objek yang tidak terpakai menggunakan kriteria **Reachability** (keterjangkauan). Objek apa pun yang tidak dapat dicapai dari akar global (global root, call stack active frame) dianggap sebagai sampah (garbage) dan dibebaskan dari memori. Kebocoran memori (memory leaks) biasanya terjadi akibat closure yang menahan variabel besar secara tidak sengaja, event listener yang tidak dilepas, atau referensi global yang tertinggal.

---

## 2. Concurrency & Parallelism
JavaScript adalah bahasa pemrograman single-threaded, yang berarti ia hanya memiliki satu Call Stack untuk menjalankan kode sinkronus. Model konkurensinya diatur oleh **Event Loop**.

### The Event Loop Architecture
1. **Call Stack**: Menjalankan tugas sinkronus satu demi satu.
2. **Web APIs / Node APIs**: Operasi asinkronus (seperti network requests, file I/O, timers) didelegasikan ke latar belakang OS atau thread pool internal (seperti thread pool `libuv` di Node.js).
3. **Callback Queue (Task Queue / Macrotask Queue)**: Menampung callback dari operasi seperti `setTimeout`, `setInterval`, I/O.
4. **Microtask Queue**: Menampung callback dengan prioritas tinggi seperti `Promise` resolvers (`.then`, `.catch`, `.finally`), `process.nextTick` (Node.js), dan `MutationObserver`.
5. **Execution Order**: Event loop akan selalu membersihkan *Microtask Queue* secara penuh sebelum mengambil satu tugas berikutnya dari *Macrotask Queue*.

Untuk pemrosesan paralel murni yang memakan beban CPU tinggi, JavaScript menyediakan **Worker Threads** (Node.js) atau **Web Workers** (Browser) yang berjalan pada thread OS terpisah dan berkomunikasi lewat message passing (`postMessage`) atau memori bersama (`SharedArrayBuffer`).

---

## 3. Dependency & Build Systems
Sistem ekosistem JavaScript sangat bergantung pada registry paket NPM.
- **npm / pnpm / yarn**: Package manager untuk mengelola `package.json` dan `package-lock.json`. `pnpm` menonjol karena menggunakan *hard link* global untuk menghindari duplikasi package di hard drive.
- **Bundler (Vite, Webpack, Esbuild)**: Alat untuk mengompilasi dan mengoptimalkan kode (tree shaking, minification) untuk performa web browser.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi scheduler asinkronus dengan antrean terbatas (concurrent queue manager) menggunakan native JavaScript Promises tanpa library eksternal.

```javascript
class AsyncQueue {
  constructor(concurrencyLimit) {
    this.concurrencyLimit = concurrencyLimit;
    this.runningCount = 0;
    this.queue = [];
  }

  enqueue(asyncTask) {
    return new Promise((resolve, reject) => {
      this.queue.push({ asyncTask, resolve, reject });
      this.next();
    });
  }

  next() {
    if (this.runningCount >= this.concurrencyLimit || this.queue.length === 0) {
      return;
    }

    const { asyncTask, resolve, reject } = this.queue.shift();
    this.runningCount++;

    asyncTask()
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      })
      .finally(() => {
        this.runningCount--;
        this.next();
      });
  }
}

// Demo Usage:
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const queue = new AsyncQueue(2); // Limit limit 2 concurrent tasks

const createMockTask = (id, ms) => () => {
  console.log(`Task ${id} started`);
  return delay(ms).then(() => {
    console.log(`Task ${id} completed`);
    return `Result of ${id}`;
  });
};

Promise.all([
  queue.enqueue(createMockTask(1, 300)),
  queue.enqueue(createMockTask(2, 100)),
  queue.enqueue(createMockTask(3, 200)),
  queue.enqueue(createMockTask(4, 150)),
]).then((results) => {
  console.log("All tasks completed:", results);
});
```
