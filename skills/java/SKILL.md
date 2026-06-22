---
name: Java Development
description: Deep dive into JVM internals, GC mechanics, thread pools, and Gradle/Maven build systems.
---

# 🛠️ Java Development

## 1. Memory Management & Lifecycles
Java berjalan di atas Virtual Machine (JVM) yang secara otomatis mengelola siklus hidup memori objek di Heap menggunakan berbagai pilihan **Garbage Collector (GC)**.

### JVM Heap Structure
1. **Young Generation**:
   - **Eden Space**: Tempat di mana objek baru pertama kali dialokasikan.
   - **Survivor Spaces (S0 & S1)**: Objek yang lolos dari pembersihan Minor GC dipindahkan ke sini secara bergantian.
2. **Old (Tenured) Generation**: Objek yang berumur panjang (melewati ambang batas *tenuring threshold*) dipindahkan dari Survivor Space ke Old Generation. Area ini dibersihkan melalui Major GC.
3. **Metaspace**: Menyimpan metadata kelas (menggantikan PermGen sejak Java 8), dialokasikan langsung di memori native OS.

### GC Collectors
- **G1 (Garbage-First)**: Membagi heap menjadi wilayah berukuran sama dan membersihkan wilayah yang memiliki sampah paling banyak terlebih dahulu untuk meminimalkan waktu jeda (*pause time*).
- **ZGC (Z Garbage Collector)**: Collector ultra-low latency yang melakukan sebagian besar pekerjaannya secara konkuren dengan thread aplikasi, menjaga jeda berhenti-aplikasi (*Stop-the-World*) di bawah beberapa milidetik saja, terlepas dari ukuran heap.

---

## 2. Concurrency & Parallelism
Java menyediakan dukungan multithreading tingkat tinggi yang kaya melalui paket bawaan `java.util.concurrent`.

### Concurrency Utilities
- **Thread Pools (`ExecutorService`)**: Mengelola sekumpulan thread OS secara efisien untuk menghindari overhead pembuatan thread berulang kali.
- **`ForkJoinPool`**: Memecah tugas besar menjadi sub-tugas kecil secara rekursif (work-stealing algorithm), digunakan di balik layar oleh Java Streams API.
- **Virtual Threads (Project Loom)**: Diperkenalkan di Java 21, ini adalah thread ringan (user-space threads) yang dimount ke atas thread OS fisik. Mengizinkan jutaan thread konkuren tanpa membebani memori kernel.
- **Synchronization Primitives**: Kelas seperti `ReentrantLock`, `Semaphore`, dan `AtomicInteger` menyediakan mekanisme sinkronisasi thread-safe non-blocking dengan performa tinggi.

---

## 3. Dependency & Build Systems
Ekosistem Java didominasi oleh dua sistem build: **Maven** dan **Gradle**.
- **Gradle**: Menggunakan DSL berbasis Groovy atau Kotlin untuk mendefinisikan skrip build secara deklaratif. Gradle menonjol karena sistem caching build yang cerdas dan eksekusi tugas paralel yang sangat cepat.
- **Maven**: Berbasis file konfigurasi XML (`pom.xml`) dengan siklus hidup build (*build lifecycle*) yang kaku namun standar.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi REST Server sederhana menggunakan HTTP Server bawaan JDK (`com.sun.net.httpserver.HttpServer`) dengan multi-threading executor untuk menangani request secara konkuren.

```java
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class SimpleHttpServer {

    public static void main(String[] args) throws IOException {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        
        // Define a thread pool with fixed size
        ThreadPoolExecutor threadPoolExecutor = (ThreadPoolExecutor) Executors.newFixedThreadPool(10);
        server.setExecutor(threadPoolExecutor);
        
        // Context routing
        server.createContext("/api/hello", new HelloHandler());
        
        System.out.println("Starting simple HTTP server on port " + port);
        server.start();
    }

    static class HelloHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("GET".equals(exchange.getRequestMethod())) {
                String response = "{\"message\": \"Hello, World!\", \"thread\": \"" 
                                  + Thread.currentThread().getName() + "\"}";
                byte[] responseBytes = response.getBytes(StandardCharsets.UTF_8);
                
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, responseBytes.length);
                
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(responseBytes);
                }
            } else {
                exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            }
        }
    }
}
```
