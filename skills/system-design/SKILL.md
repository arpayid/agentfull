---
name: System Design & Scalability
description: Horizontal scaling, load balancing, caching strategies, partitioning, dan message queues.
---

# 🛠️ System Design & Scalability

## 1. CAP Theorem Trade-offs
Dalam merancang sistem terdistribusi, kita harus memilih dua dari tiga jaminan: Consistency (Konsistensi), Availability (Ketersediaan), dan Partition Tolerance (Toleransi Partisi). Karena partisi jaringan tidak dapat dihindari di dunia nyata, trade-off sebenarnya adalah antara CP (Consistency & Partition Tolerance) atau AP (Availability & Partition Tolerance).

- **CP (Consistency & Partition Tolerance)**: Sistem menolak request jika tidak dapat menjamin data terbaru di semua node. Digunakan pada sistem finansial.
- **AP (Availability & Partition Tolerance)**: Sistem tetap merespons request dengan data yang mungkin usang (stale data). Digunakan pada sistem media sosial atau shopping cart.

### PACELC Theorem Extension
Jika ada partisi (P), pilih Availability (A) atau Consistency (C); jika tidak (E), pilih Latency (L) atau Consistency (C).

```text
                  +-----------------------+
                  |  CAP Theorem (under   |
                  |   network partition)  |
                  +-----------+-----------+
                              |
              +---------------+---------------+
              |                               |
      [ Choose CP ]                   [ Choose AP ]
      Consistency & Partition         Availability & Partition
      e.g., Raft, Paxos,              e.g., DynamoDB, Cassandra,
      RDBMS (strict replica)          DNS, Eventual Consistency
```

## 2. Horizontal Scaling & Load Balancing
Penskalaan horizontal melibatkan penambahan lebih banyak mesin ke dalam resource pool.

- **Load Balancer (LB) Algorithms**:
  - Consistent Hashing: Meminimalkan reorganisasi key saat jumlah node berubah.
  - Least Connections: Mengarahkan request ke server dengan beban koneksi paling sedikit.
  - Round Robin / Weighted Round Robin.

```nginx
# Example: Nginx Load Balancer Configuration with Least Connections
http {
    upstream backend_servers {
        least_conn;
        server backend1.example.com:8080 weight=3;
        server backend2.example.com:8080;
        server backend3.example.com:8080 backup;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://backend_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 3. Database Sharding & Federation
Untuk mengatasi keterbatasan kapasitas penyimpanan dan throughput pada single instance database:

- **Database Federation**: Membagi database berdasarkan fungsionalitas/skema (misal: memisahkan DB User dan DB Order).
- **Database Sharding**: Membagi baris data dari tabel tunggal ke beberapa database berdasarkan Shard Key.
  - **Horizontal Partitioning (Range, Hash, Directory-based)**.

```sql
-- Example: Horizontal Sharding Strategy using Hash-based partitioning on User ID
-- Partitioning a large users table across multiple physical shards
CREATE TABLE users (
    user_id BIGINT NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id)
) PARTITION BY HASH (user_id);

-- Defining partition shards
CREATE TABLE users_shard_0 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE users_shard_1 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE users_shard_2 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE users_shard_3 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

## 4. Multi-level Caching Strategies
Caching digunakan untuk mengurangi latensi pembacaan data. Strategi caching multi-level meliputi:
1. **Edge/CDN**: Menyimpan aset statis close to user.
2. **Reverse Proxy/Gateway Caching**: Menyimpan HTTP responses (Varnish, Nginx).
3. **Application/In-Memory Cache**: Memori lokal aplikasi (Guava, EHCache).
4. **Distributed Cache**: Redis/Memcached.

### Cache Eviction Policies & Write Patterns
- **Policies**: LRU (Least Recently Used), LFU (Least Frequently Used), FIFO.
- **Patterns**:
  - Cache-Aside (Lazy Loading)
  - Write-Through
  - Write-Behind (Write-Back)

```typescript
// Example: Cache-Aside Pattern Implementation
import Redis from 'ioredis';

const redis = new Redis();

async function getUserData(userId: string): Promise<any> {
    const cacheKey = `user:${userId}`;
    
    // 1. Read from distributed cache
    const cachedData = await redis.get(cacheKey);
    if (cachedData) {
        return JSON.parse(cachedData);
    }
    
    // 2. Fetch from primary database if cache miss
    const dbData = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
    if (!dbData) {
        return null;
    }
    
    // 3. Write to cache with TTL (Time-To-Live)
    await redis.set(cacheKey, JSON.stringify(dbData), 'EX', 3600);
    
    return dbData;
}
```

## 5. Message Queue Back-pressure
Dalam arsitektur event-driven, produsen dapat memproduksi pesan lebih cepat daripada yang bisa diproses oleh konsumen. Mekanisme penanganan back-pressure:
- **Rate Limiting / Throttling**: Membatasi laju pengiriman pesan dari produsen.
- **Dynamic Pull-based Consumer**: Konsumen meminta data hanya ketika memiliki kapasitas (misal: menggunakan prefetch limit).
- **Dead Letter Queue (DLQ)**: Memisahkan pesan yang gagal diproses agar tidak memblokir antrean utama.

```javascript
// Example: AMQP (RabbitMQ) Consumer with Prefetch Limit (Back-pressure control)
const amqp = require('amqplib');

async function startConsumer() {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    const queue = 'order_processing';

    await channel.assertQueue(queue, { durable: true });

    // Restrict consumer to pull only 10 messages at a time (Prefetch Limit)
    // This prevents consumer memory overload (back-pressure mitigation)
    channel.prefetch(10);

    console.log(`[*] Waiting for messages in ${queue}.`);

    channel.consume(queue, async (msg) => {
        if (msg !== null) {
            try {
                // Process the message payload
                await processOrder(JSON.parse(msg.content.toString()));
                channel.ack(msg);
            } catch (error) {
                console.error('Failed to process message, sending to DLQ', error);
                // Reject message and requeue=false (sends to configured Dead Letter Exchange)
                channel.nack(msg, false, false);
            }
        }
    });
}
```

## 6. Back-of-the-envelope Calculations
Kalkulasi cepat untuk memperkirakan kebutuhan kapasitas infrastruktur (storage, bandwidth, memory, QPS).

### Aturan Praktis (Rules of Thumb)
- 1 hari = 86,400 detik (~100,000 detik untuk estimasi kasar).
- QPS (Queries Per Second) = Total Request / 100,000.
- Bandwidth = QPS * Rata-rata Ukuran Request.

### Contoh Kasus
Estimasi penyimpanan data teks tweet untuk aplikasi Twitter Clone:
- **Asumsi**:
  - 100 juta Daily Active Users (DAU).
  - Setiap user memposting rata-rata 2 tweet per hari.
  - Setiap tweet berukuran 250 byte (metadata + text).
- **Kalkulasi**:
  - Total Tweet per hari = 100,000,000 * 2 = 200,000,000 tweet.
  - Storage per hari = 200,000,000 * 250 bytes = 50,000,000,000 bytes ≈ 50 GB.
  - Storage untuk 5 tahun = 50 GB/hari * 365 * 5 ≈ 91.25 TB.
  - Menulis QPS = 200,000,000 / 86,400 detik ≈ 2,300 QPS.
