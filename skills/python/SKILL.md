---
name: Python Mastery
description: Deep dive into Python memory management, GIL, async/await, and project packaging.
---

# 🛠️ Python Mastery

## 1. Memory Management & Lifecycles
Python menggunakan sistem manajemen memori otomatis berbasis **Reference Counting** yang dikombinasikan dengan **Generational Garbage Collector** untuk mendeteksi siklus melingkar (cyclic references).

### Reference Counting
- Setiap objek Python memiliki header `ob_refcnt` yang mencatat jumlah referensi aktif ke objek tersebut.
- Ketika referensi bertambah (misal ditugaskan ke variabel baru atau dimasukkan ke list), `ob_refcnt` dinaikkan.
- Ketika variabel keluar dari scope atau dihapus dengan `del`, `ob_refcnt` diturunkan.
- Jika `ob_refcnt` mencapai 0, memori objek tersebut langsung dibebaskan.

### Generational Garbage Collector
Reference counting tidak dapat mendeteksi siklus melingkar (misal objek A merujuk B, dan B merujuk A, tetapi keduanya tidak dapat diakses dari variabel global/lokal).
- Garbage Collector Python melacak siklus ini menggunakan 3 generasi (Generation 0, 1, dan 2).
- Objek baru ditempatkan di Generation 0. Jika bertahan dari proses pembersihan GC, objek dipindahkan ke generasi berikutnya.
- Proses scanning generasi yang lebih tua dilakukan lebih jarang untuk menghemat overhead CPU.

---

## 2. Concurrency & Parallelism
Model eksekusi default Python (CPython) dibatasi oleh **GIL (Global Interpreter Lock)**.

### Global Interpreter Lock (GIL)
- GIL adalah mutex yang memastikan hanya ada satu thread OS yang mengeksekusi bytecode Python pada satu waktu.
- Hal ini dilakukan untuk melindungi struktur data internal CPython (seperti reference counting) dari data race.
- **Multithreading** cocok untuk tugas I/O-bound karena GIL dilepaskan selama pemanggilan operasi I/O (disk/network).
- **Multiprocessing** digunakan untuk tugas CPU-bound karena membuat proses OS baru dengan interpreter dan GIL terpisah.
- **Async/Await (`asyncio`)**: Model konkurensi kooperatif berbasis *Single-Threaded Event Loop*. Fungsi generator khusus (`coroutine`) menunda eksekusi secara sukarela menggunakan keyword `await`, melepaskan kontrol kembali ke event loop tanpa overhead context switching thread OS.

---

## 3. Dependency & Build Systems
Sistem build dan manajemen dependensi di Python telah berkembang pesat.
- **Pip**: Package installer default untuk Python.
- **Virtual Environments (`venv`)**: Digunakan untuk mengisolasi dependensi antar proyek agar tidak terjadi konflik dengan lib global sistem.
- **Pipenv / Poetry**: Menyediakan file lock (`poetry.lock`) berbasis grafik dependensi deterministik untuk merekam versi spesifik dari setiap pustaka.
- **Packaging (`pyproject.toml`)**: Mengikuti standar PEP 517/518 untuk menentukan backend build (misalnya `poetry-core`, `hatchling`, atau `setuptools`).

---

## 4. Real-world Code Implementation
Berikut adalah implementasi web scraper asinkronus menggunakan `asyncio` yang melakukan fetch data konkuren dengan pembatasan rate-limiting menggunakan `asyncio.Semaphore`.

```python
import asyncio
import time
from typing import List

async def fetch_url(sem: asyncio.Semaphore, url: str) -> str:
    async with sem:
        print(f"Starting fetch for {url}")
        # Simulate network latency
        await asyncio.sleep(0.5)
        print(f"Finished fetch for {url}")
        return f"Content of {url}"

async def main():
    urls = [
        "https://example.com/a",
        "https://example.com/b",
        "https://example.com/c",
        "https://example.com/d",
        "https://example.com/e",
    ]
    
    # Limit concurrency to 2 active fetches at a time
    sem = asyncio.Semaphore(2)
    
    start_time = time.monotonic()
    
    tasks = [fetch_url(sem, url) for url in urls]
    results: List[str] = await asyncio.gather(*tasks)
    
    duration = time.monotonic() - start_time
    print(f"All fetches completed in {duration:.2f} seconds")
    for res in results:
        print(f"Result: {res}")

if __name__ == "__main__":
    asyncio.run(main())
```
