---
name: C++ Systems Programming
description: Deep dive into C++ manual memory management, RAII, Smart Pointers, multi-threading, and CMake.
---

# 🛠️ C++ Systems Programming

## 1. Memory Management & Lifecycles
C++ memberikan kontrol penuh atas manajemen memori tanpa garbage collector (GC), sehingga pengembang memegang tanggung jawab atas alokasi dan deallokasi memori fisik.

### Stack vs Heap Allocation
- **Stack**: Variabel lokal dialokasikan di stack frame. Dialokasikan dan didealokasikan secara otomatis ketika keluar dari cakupan (scope).
- **Heap**: Alokasi dinamis menggunakan operator `new` atau fungsi standar C `malloc`. Memori ini harus didealokasikan secara eksplisit menggunakan `delete` atau `free` untuk mencegah kebocoran memori (*memory leaks*).

### RAII (Resource Acquisition Is Initialization)
RAII adalah teknik desain di mana kepemilikan sumber daya (seperti alokasi memori heap, file descriptor, database connection, mutex lock) diikat ke masa hidup objek stack. Saat objek stack keluar dari scope, destruktor objek akan dipanggil secara otomatis dan membebaskan sumber daya tersebut.

### Smart Pointers (C++11)
- **`std::unique_ptr<T>`**: Menjamin kepemilikan tunggal atas objek di heap. Tidak dapat disalin, hanya bisa dipindahkan (*move semantics*).
- **`std::shared_ptr<T>`**: Menggunakan penghitung referensi (*reference counting*). Memori heap dibebaskan ketika hitungan referensi mencapai nol.
- **`std::weak_ptr<T>`**: Referensi non-owning ke objek yang dikelola oleh `std::shared_ptr` untuk mencegah siklus ketergantungan melingkar (*circular reference*).

---

## 2. Concurrency & Parallelism
Sejak standar C++11, C++ menyediakan pustaka konkurensi bawaan yang memetakan langsung ke utas sistem operasi (OS thread).

### Utas dan Sinkronisasi
- **`std::thread` & `std::jthread` (C++20)**: Memulai eksekusi thread OS baru. `jthread` otomatis melakukan `join()` pada saat destruksi objek.
- **`std::mutex` & `std::lock_guard` / `std::unique_lock`**: Mencegah kondisi balapan (*data race*) dengan menjamin akses eksklusif ke data bersama.
- **`std::atomic<T>`**: Operasi baca-tulis tingkat rendah yang tidak memerlukan penguncian berat, memanfaatkan instruksi CPU atomic secara langsung.
- **Async & Futures (`std::async`, `std::future`)**: Abstraksi tingkat tinggi untuk mengeksekusi tugas asinkronus dan mendapatkan hasilnya nanti tanpa mengelola thread secara manual.

---

## 3. Dependency & Build Systems
C++ tidak memiliki package manager tunggal yang universal, namun ekosistem modern mengadopsi standar tertentu.
- **CMake**: Meta-build system yang menghasilkan file build platform-spesifik (seperti Makefiles di Unix atau project files Visual Studio di Windows).
- **Conan / vcpkg**: Package manager modern untuk C++ yang mempermudah instalasi dan pengelolaan dependensi pustaka eksternal.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi thread-safe ring buffer (circular queue) yang sering digunakan dalam aplikasi sistem real-time atau audio processing di C++.

```cpp
#include <iostream>
#include <vector>
#include <mutex>
#include <condition_variable>
#include <thread>

template <typename T>
class RingBuffer {
private:
    std::vector<T> buffer;
    size_t head = 0;
    size_t tail = 0;
    size_t capacity;
    size_t current_size = 0;
    std::mutex mtx;
    std::condition_variable not_full;
    std::condition_variable not_empty;

public:
    explicit RingBuffer(size_t max_size) : capacity(max_size) {
        buffer.resize(max_size);
    }

    void push(const T& item) {
        std::unique_lock<std::mutex> lock(mtx);
        not_full.wait(lock, [this]() { return current_size < capacity; });

        buffer[tail] = item;
        tail = (tail + 1) % capacity;
        current_size++;

        not_empty.notify_one();
    }

    T pop() {
        std::unique_lock<std::mutex> lock(mtx);
        not_empty.wait(lock, [this]() { return current_size > 0; });

        T item = buffer[head];
        head = (head + 1) % capacity;
        current_size--;

        not_full.notify_one();
        return item;
    }
};

int main() {
    RingBuffer<int> rb(5);

    // Consumer Thread
    std::thread consumer([&rb]() {
        for (int i = 0; i < 10; ++i) {
            int val = rb.pop();
            std::cout << "Consumed value: " << val << std::endl;
        }
    });

    // Producer Thread
    std::thread producer([&rb]() {
        for (int i = 0; i < 10; ++i) {
            rb.push(i * 10);
            std::cout << "Produced value: " << i * 10 << std::endl;
        }
    });

    producer.join();
    consumer.join();

    return 0;
}
```
