---
name: Scala Programming
description: Deep dive into JVM GC mechanics for Scala, functional programming futures, actors, and sbt build system.
---

# 🛠️ Scala Programming

## 1. Memory Management & Lifecycles
Scala berjalan di atas JVM (Java Virtual Machine), sehingga manajemen memorinya identik dengan Java. Namun, paradigma pemrograman fungsional (*functional programming*) di Scala membawa karakteristik unik terhadap alokasi memori.

### Impact of Functional Programming on GC
- **Immutability (Ketidakubahan)**: Karena Scala mendorong penggunaan data immutable, objek baru terus-menerus dibuat saat state berubah (misalnya memodifikasi struktur data case class).
- **High Object Allocation**: Hal ini menghasilkan tingkat alokasi objek yang sangat tinggi di Young Generation. Oleh karena itu, JVM Garbage Collector dengan performa GC Young Generation yang cepat (seperti G1GC atau ZGC dengan konfigurasi generasi) sangat disarankan untuk meredam overhead *allocation rate*.
- **Value Classes**: Scala menyediakan *Value Classes* (turunan dari `AnyVal`) yang meminimalkan overhead alokasi dengan menghindari pembuatan objek pembungkus (*wrapper*) di heap, dan menggantinya dengan tipe data primitif pada saat transpilasi bytecode.

---

## 2. Concurrency & Parallelism
Scala menyediakan model konkurensi fungsional yang kuat dan tingkat tinggi di atas platform multithreading JVM.

### Concurrency Primitives
- **`scala.concurrent.Future`**: Abstraksi asinkronus non-blocking yang mengikat komputasi di masa depan ke dalam konteks eksekusi (`ExecutionContext`, biasanya berupa thread pool JVM).
- **Akka / Pekko Actors**: Model konkurensi berbasis aktor (Actor Model) yang membatasi state internal ke dalam aktor dan berkomunikasi murni melalui pengiriman pesan asinkronus (*asynchronous message passing*), menghindari kebutuhan akan kunci (*locks*) manual.
- **Cats Effect / ZIO**: Pustaka efek fungsional (functional effect systems) modern yang memperkenalkan konsep *Fibers* (green threads/logical threads) untuk penjadwalan asinkronus ultra-ringan dengan konsumsi memori minimum.

---

## 3. Dependency & Build Systems
Sistem build standar industri untuk Scala adalah **sbt (Scala Build Tool)**.

### sbt Workflow
- `build.sbt`: Berisi definisi proyek, dependensi, opsi kompilasi compiler (`scalacOptions`), serta plugin build.
- Caching: sbt melacak perubahan kode secara inkremental untuk menghindari kompilasi ulang yang memakan waktu lama.
- Kompilator Scala (`scalac`) melakukan optimasi tingkat lanjut selama fase kompilasi, seperti *tail-call recursion optimization* dan *macro expansion*.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi scheduler asinkronus menggunakan Scala Futures dan Promises untuk membatasi tingkat konkuren tugas eksekusi.

```scala
import scala.concurrent.{Future, Promise, ExecutionContext}
import scala.util.{Success, Failure}
import java.util.concurrent.ConcurrentLinkedQueue
import java.util.concurrent.atomic.AtomicInteger

class ConcurrentTaskLimiter(limit: Int)(implicit ec: ExecutionContext) {
  private val activeTasks = new AtomicInteger(0)
  private val queue = new ConcurrentLinkedQueue[PendingTask[_]]()

  private case class PendingTask[T](task: () => Future[T], promise: Promise[T])

  def submit[T](task: () => Future[T]): Future[T] = {
    val promise = Promise[T]()
    queue.offer(PendingTask(task, promise))
    tryExecuteNext()
    promise.future
  }

  private def tryExecuteNext(): Unit = {
    if (activeTasks.get() < limit) {
      val pending = queue.poll()
      if (pending != null) {
        if (activeTasks.incrementAndGet() <= limit) {
          execute(pending)
        } else {
          activeTasks.decrementAndGet()
          queue.offer(pending) // Requeue
        }
      }
    }
  }

  private def execute[T](pending: PendingTask[T]): Unit = {
    pending.task().onComplete { result =>
      activeTasks.decrementAndGet()
      result match {
        case Success(v) => pending.promise.success(v)
        case Failure(e) => pending.promise.failure(e)
      }
      tryExecuteNext()
    }
  }
}

// Example Usage
object Main extends App {
  import scala.concurrent.ExecutionContext.Implicits.global
  import scala.concurrent.duration._
  import scala.concurrent.Await

  val limiter = new ConcurrentTaskLimiter(2)

  val tasks = (1 to 5).map { id =>
    () => Future {
      println(s"Task $id started on thread ${Thread.currentThread().getName}")
      Thread.sleep(200) // Simulate work
      println(s"Task $id completed")
      s"Result $id"
    }
  }

  val futures = tasks.map(t => limiter.submit(t))
  val combinedResult = Future.sequence(futures)

  val results = Await.result(combinedResult, 5.seconds)
  println(s"All tasks finished: $results")
}
```
