---
name: Ruby Performance
description: Deep dive into Ruby GC mechanics, Ractor concurrency, Fiber scheduler, and Bundler.
---

# 🛠️ Ruby Performance

## 1. Memory Management & Lifecycles
Ruby mengelola alokasi memori secara otomatis menggunakan **Garbage Collector (GC)** berbasis *Incremental and Generational GC* (dikenal sebagai RGenGC sejak Ruby 2.1).

### Garbage Collector Mechanics
1. **Ruby Heap & Slots**: Ruby mengalokasikan memori dalam blok besar yang dibagi menjadi ribuan *slots* berukuran sama. Setiap objek Ruby menempati satu slot (`RVALUE`).
2. **Generational Garbage Collection**: Objek dibagi menjadi dua generasi:
   - **Young Generation**: Objek baru. GC minor hanya memeriksa area ini untuk menjaga latensi tetap rendah.
   - **Old Generation**: Objek yang selamat dari beberapa siklus GC minor dipromosikan ke sini. GC major memeriksa area ini ketika memori penuh.
3. **Write Barrier**: Digunakan untuk memantau apakah objek generasi lama membuat referensi baru ke objek generasi baru, sehingga GC minor tetap dapat memindai referensi tersebut tanpa memindai seluruh old generation.

---

## 2. Concurrency & Parallelism
Sama seperti Python CPython, implementasi Ruby standar (CRuby) menggunakan **GVL (Global VM Lock)** yang membatasi eksekusi thread.

### Concurrency Primitives
- **GVL (Global VM Lock)**: Menjamin hanya satu thread Ruby yang mengeksekusi instruksi Ruby pada satu waktu. Thread tetap berguna untuk tugas I/O-bound.
- **Fibers**: Thread kooperatif ringan yang dikelola di tingkat pengguna (user-space). Sejak Ruby 3.0, *Fiber Scheduler* diperkenalkan untuk memungkinkan I/O non-blocking otomatis saat menggunakan Fibers.
- **Ractors (Ruby 3+)**: Model konkurensi berbasis aktor (Actor Model) yang dirancang untuk mencapai paralelisme sejati tanpa GVL. Ractor membatasi pembagian state memori; data harus dipindahkan (moved) atau disalin (copied) antar Ractor untuk menghindari kondisi balapan (*data race*).

---

## 3. Dependency & Build Systems
Sistem manajemen dependensi resmi Ruby adalah **Bundler**.

### Bundler & Gem Workflow
- `Gemfile`: Mendeklarasikan daftar pustaka (*gems*) yang dibutuhkan oleh proyek serta sumber repositorinya (misal RubyGems).
- `Gemfile.lock`: Merekam versi persis dari setiap gem yang terpasang bersama dengan dependensi transitifnya.
- **Rake**: Alat build bawaan Ruby untuk mengotomatisasi tugas-tugas administratif (seperti migrasi database atau menjalankan pengujian).

---

## 4. Real-world Code Implementation
Berikut adalah implementasi pengambil data (downloader) berkinerja tinggi yang memanfaatkan model paralel Ractor (tanpa GVL interference) untuk memproses data secara konkuren.

```ruby
# Requires Ruby 3.0+ for Ractor support
require 'net/http'
require 'json'

# Worker Ractor to process data
worker = Ractor.new do
  loop do
    # Receive job from main thread
    url = Ractor.receive
    
    begin
      uri = URI(url)
      response = Net::HTTP.get(uri)
      
      # Yield result back
      Ractor.yield({ status: "success", url: url, length: response.length })
    rescue => e
      Ractor.yield({ status: "error", url: url, error: e.message })
    end
  end
end

# Main orchestration logic
urls = [
  "https://www.ruby-lang.org/en/",
  "https://rubygems.org",
  "https://github.com"
]

# Send urls to worker Ractor
urls.each do |url|
  worker.send(url)
end

# Collect results
urls.each do |_|
  result = Ractor.select(worker)[1]
  puts "Result for #{result[:url]}: #{result[:status]} (Length: #{result[:length] || 0} bytes)"
  if result[:status] == "error"
    puts "  Error details: #{result[:error]}"
  end
end
```
