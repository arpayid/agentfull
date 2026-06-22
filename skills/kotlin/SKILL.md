---
name: Kotlin Development
description: Deep dive into Kotlin coroutines, JVM GC mechanics, compile-time enhancements, and Gradle build.
---

# 🛠️ Kotlin Development

## 1. Memory Management & Lifecycles
Kotlin berjalan terutama di atas JVM (meskipun mendukung kompilasi ke JavaScript dan biner Native via Kotlin/Native), sehingga manajemen memori default-nya mengikuti arsitektur JVM Heap (Eden, Survivor, Old Gen).

### Kotlin-specific Memory Enhancements
- **Inline Functions**: Kotlin memperkenalkan keyword `inline`. Fungsi yang ditandai sebagai `inline` akan menyisipkan bytecodenya secara langsung ke lokasi pemanggil, menghindari alokasi objek instance dari closure/lambda yang biasanya dibuat saat runtime.
- **Null Safety**: Pemeriksaan null di Kotlin diselesaikan pada saat kompilasi. Kotlin membedakan tipe data nullable (`T?`) dan non-nullable (`T`). Compiler menyisipkan pemeriksaan bytecode statis (`Intrinsics.checkNotNullParameter`) untuk mencegah kebocoran referensi null ke memori runtime.

---

## 2. Concurrency & Parallelism
Kotlin menangani konkurensi modern melalui fitur bawaan bahasa yang sangat populer: **Coroutines**.

### Kotlin Coroutines Architecture
- **Suspension Points**: Coroutines dapat ditangguhkan (*suspended*) tanpa memblokir thread OS yang mendasarinya menggunakan keyword `suspend`.
- **Dispatcher**: Mengontrol thread mana yang digunakan untuk menjalankan coroutine:
  - `Dispatchers.Default`: Dioptimasikan untuk tugas-tugas intensif CPU (berbagi thread pool seukuran jumlah core CPU).
  - `Dispatchers.IO`: Dioptimasikan untuk tugas I/O-bound (disk/network) dengan pool thread yang elastis dan dapat bertambah.
  - `Dispatchers.Main`: Terikat ke thread UI utama (misalnya di Android).
- **Structured Concurrency**: Hubungan hierarkis antara *CoroutineScope* dan *Job* memastikan jika sebuah scope dibatalkan, semua coroutine anak di dalamnya otomatis ikut dibatalkan, mencegah kebocoran coroutine (*coroutine leaks*).

---

## 3. Dependency & Build Systems
Sistem build standar di ekosistem Kotlin adalah **Gradle** yang dikombinasikan dengan Kotlin DSL (`build.gradle.kts`).

### Gradle Kotlin DSL
- Menyediakan type safety dan autocompletion saat menulis konfigurasi build dibandingkan Groovy.
- Dependensi dideklarasikan di blok `dependencies` menggunakan konfigurasi modern seperti `implementation`, `api`, atau `kapt` (Kotlin Annotation Processing Tool) / `ksp` (Kotlin Symbol Processing) untuk pemrosesan anotasi compile-time yang lebih cepat.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi sinkronisasi data asinkronus menggunakan Kotlin Coroutines Flow untuk memproses aliran data secara konkuren.

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlin.system.measureTimeMillis

fun getEventStream(): Flow<Int> = flow {
    for (i in 1..5) {
        delay(100) // Simulate fetching event from network
        emit(i)
    }
}

fun main() = runBlocking {
    val time = measureTimeMillis {
        getEventStream()
            .map { request -> 
                // Process each event in CPU-bound pool
                withContext(Dispatchers.Default) {
                    delay(200) // Simulate processing delay
                    "Processed Event-$request"
                }
            }
            .collect { response ->
                println("$response on thread ${Thread.currentThread().name}")
            }
    }
    println("Completed in $time ms")
}
```
