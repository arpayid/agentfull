# OpenCode CLI Integration

OpenCode CLI adalah agen kolaboratif yang sangat efisien untuk menangani operasi lintas file, *refactoring* massal, dan manajemen repositori.

File aturan ini dirancang untuk memastikan OpenCode CLI tidak hanya mengeksekusi perintah secara buta, tetapi mengevaluasi risiko dari setiap modifikasi lintas-file (*Cross-File Modification Risk*).

## Cara Instalasi

Sebagian besar implementasi OpenCode membaca konfigurasi instruksi dari file `.opencode.yml` atau menggunakan *system flag* khusus saat *runtime*.

1. Salin file `OPENCODE_RULES.md` ke dalam folder proyek Anda (misalnya `.opencode/rules.md`).
2. Muat file tersebut saat inisialisasi:
   ```bash
   opencode start --rules .opencode/rules.md
   ```
   *Catatan: Flag perintah spesifik mungkin berbeda tergantung versi OpenCode CLI yang Anda gunakan.*
