---
name: Infrastructure & DevOps
description: Praktik terbaik pengelolaan Docker, database, dan CI/CD pipeline.
---

# 🏗️ Infrastructure & DevOps

Agen AI harus mampu mengelola infrastruktur layaknya seorang DevOps Engineer elit.

## 1. Docker Best Practices

Saat menulis atau me-review `Dockerfile`:
- **Gunakan Multi-stage builds:** Pisahkan *build environment* dan *production environment* untuk meminimalisir ukuran image.
- **Jalankan sebagai Non-Root:** Selalu gunakan `USER node` atau user non-root lainnya untuk keamanan.
- **Layer Caching:** Urutkan instruksi dari yang paling jarang berubah (misal: install OS packages) ke yang sering berubah (misal: copy source code). Copy `package.json` sebelum meng-copy semua source code.
- **Gunakan `.dockerignore`:** Jangan biarkan file `node_modules` atau log masuk ke build context.

## 2. Container Orchestration (Docker Compose)

Prinsip `docker-compose.yml`:
- Hindari konflik port di mesin host (misal: gunakan `${PORT:-5432}:5432`).
- Gunakan `healthcheck` untuk memastikan dependensi (database) siap sebelum backend menyala (`depends_on: condition: service_healthy`).
- Pasang volume untuk data persisten (database, redis).

## 3. Database Management

- **Migrations:** Jangan pernah memanipulasi skema database produksi tanpa file migrasi.
- **Seeding:** Pastikan file seed bersifat *idempotent* (aman dijalankan berkali-kali).
- **CI/CD:** Di lingkungan CI, seringkali database harus di-reset sepenuhnya (`docker compose down -v`) untuk menghindari status basi (*stale state*).

## 4. CI/CD Pipeline Design

Pipeline CI yang baik memiliki ciri:
1. **Cepat:** Gunakan caching untuk dependencies (npm/pnpm).
2. **Ketat:** Gagal jika *linter* atau *typechecker* merah.
3. **Realistis:** Integration test harus menggunakan database sungguhan (via Docker), bukan sekadar in-memory mock.
4. **Resilien:** Lakukan *teardown* service secara otomatis di blok `always()` atau `finally` agar tidak meninggalkan sampah di runner.

## 5. Environment Management

Jangan menaruh secret di *plain text*.
Gunakan:
- `.env.example` untuk dokumentasi.
- Variabel lingkungan dinamis di script shell.

Contoh override env yang aman di bash:
```bash
POSTGRES_PORT=5433 REDIS_PORT=6380 ./scripts/start.sh
```
