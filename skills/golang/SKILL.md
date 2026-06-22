---
name: Go Concurrency & Systems
description: Deep dive into Golang GC mechanics, goroutines, channels, interfaces, and go modules.
---

# 🛠️ Go Concurrency & Systems

## 1. Memory Management & Lifecycles
Go menggunakan sistem manajemen memori otomatis dengan **Garbage Collector (GC)** konkuren bertipe *tri-color mark-and-sweep*. 

### Garbage Collector Mechanics
1. **Tri-color Marking**: Objek di memori dikategorikan menjadi 3 warna:
   - *White*: Calon objek untuk dibersihkan (belum dikunjungi).
   - *Grey*: Objek telah dikunjungi, tetapi objek yang dirujuk belum diproses.
   - *Black*: Objek aktif dan semua objek yang dirujuk telah diproses.
2. **Write Barrier**: Selama fase mark aktif, runtime menjalankan write barrier untuk memastikan pointer baru yang dibuat oleh program tidak lolos dari pemindaian GC.
3. **Escape Analysis**: Compiler memutuskan apakah variabel ditempatkan di *Stack* atau *Heap*. Variabel yang masa hidupnya melebihi siklus hidup fungsi pemanggil (misal mengembalikan pointer ke variabel lokal) akan "escape" ke heap.

---

## 2. Concurrency & Parallelism
Go memiliki model konkurensi bawaan berbasis CSP (Communicating Sequential Processes) yang diimplementasikan menggunakan **Goroutines** dan **Channels**.

### Scheduler Go (M:N Scheduler)
Runtime Go menjadwalkan $N$ goroutines ke atas $M$ OS threads menggunakan konsep **GMP Model**:
- **G (Goroutine)**: Mewakili goroutine itu sendiri (stack dinamis, mulai dari 2KB).
- **M (Machine)**: Mewakili OS thread fisik yang dijalankan oleh OS kernel.
- **P (Processor)**: Konteks logis eksekusi yang menampung antrean goroutine lokal (Local Run Queue).
- **Work Stealing**: Jika sebuah P kehabisan goroutine untuk dijalankan, ia akan mencoba "mencuri" sebagian goroutine dari antrean P lain.
- **Preemption**: Go scheduler dapat melakukan preemption secara asinkronus terhadap goroutine yang berjalan terlalu lama (misal pada saat pemanggilan fungsi atau loop panjang).

---

## 3. Dependency & Build Systems
Sistem dependency resmi Go menggunakan **Go Modules** (`go mod`).

### Go Modules Workflow
- `go.mod`: Mendefinisikan modul utama beserta versi minimum dari dependensi langsung maupun tidak langsung.
- `go.sum`: Berisi hash kriptografis dari file dependensi untuk menjamin *reproducibility* dan *security integrity* agar kode dependensi tidak diubah di server remote.
- Kompilasi Go menghasilkan satu biner statis mandiri (statically linked binary) secara default, memudahkan deployment tanpa memerlukan runtime eksternal.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi thread-safe worker pool menggunakan goroutines, channels, dan `sync.WaitGroup` di Go.

```go
package main

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type Job struct {
	ID   int
	Data string
}

type Result struct {
	JobID int
	Err   error
}

func worker(ctx context.Context, id int, jobs <-chan Job, results chan<- Result, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case <-ctx.Done():
			return
		case job, ok := <-jobs:
			if !ok {
				return
			}
			fmt.Printf("Worker %d started job %d\n", id, job.ID)
			time.Sleep(100 * time.Millisecond) // Simulate work
			results <- Result{JobID: job.ID, Err: nil}
		}
	}
}

func main() {
	const numWorkers = 3
	const numJobs = 5

	jobs := make(chan Job, numJobs)
	results := make(chan Result, numJobs)
	
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	var wg sync.WaitGroup

	// Start workers
	for w := 1; w <= numWorkers; w++ {
		wg.Add(1)
		go worker(ctx, w, jobs, results, &wg)
	}

	// Send jobs
	for j := 1; j <= numJobs; j++ {
		jobs <- Job{ID: j, Data: fmt.Sprintf("Data-%d", j)}
	}
	close(jobs)

	// Wait for workers in a separate goroutine
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect results
	for result := range results {
		fmt.Printf("Job result collected for ID %d\n", result.JobID)
	}
}
```
