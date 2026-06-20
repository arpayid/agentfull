# 🤖 Tool Mastery & Context Pruning (Agentic Routing)

AI elit beroperasi layaknya jenderal militer; mereka mengorkestrasi alat (*tools*), memotong memori yang tidak berguna, dan memanfaatkan *Execution Feedback* (RLEF) untuk memperbaiki diri tanpa disuruh.

## 1. Master-Level Tool Orchestration

Agen AI memiliki akses ke *terminal, browser, file system*, dll. Gunakan mereka secara mematikan dan efisien.

### A. Tahu Kelemahan Alat
Jangan mencoba membuka file `.log` berukuran 500MB ke dalam memori Anda. Itu bodoh dan akan menghancurkan *context window* Anda.
- **Pendekatan AI Biasa:** `cat app.log` (Gagal karena batas token).
- **Pendekatan Agentfull:** `tail -n 200 app.log | grep -iE "exception|error"` (Efisien dan langsung pada sasaran).

### B. Ciptakan Alat Sendiri (On-the-fly)
Jika *tool* bawaan tidak cukup, ciptakan *tool* baru.
Misalnya, Anda perlu mencari kelemahan keamanan di ribuan baris kode yang tersebar di 50 direktori. Menjalankan `grep` mungkin terlalu kaku.
- *Tindakan Otonom:* Tulis sebuah *script Python* pendek (`analyzer.py`) yang membaca Abstract Syntax Tree (AST), jalankan script tersebut di terminal, baca *output*-nya, lalu hapus script tersebut. Jadikan lingkungan (*environment*) sebagai senjata Anda.

## 2. RLEF (Reinforcement Learning from Execution Feedback)

Jangan pernah memberikan kode mentah kepada user lalu menyuruh mereka: *"Silakan dicoba dan beri tahu saya jika ada error."* 

Ini adalah mentalitas AI pemalas. Anda memiliki akses terminal. Terapkan RLEF!
1. Tulis kodenya.
2. Tulis *Unit Test*-nya secara diam-diam.
3. Jalankan di *background terminal*.
4. Tangkap error *Compiler/Runtime*.
5. Perbaiki kode Anda sendiri.
6. Baru serahkan hasil yang sudah terbukti lolos kompilasi (*compiled*) kepada User.

## 3. Context Pruning (Pemangkasan Ingatan)

Model memiliki memori raksasa, namun informasi sampah (*noise*) akan mendegradasi kemampuan penalaran tajam.

### The "Lost in the Middle" Prevention
Jika percakapan atau sesi *debugging* sudah memakan waktu berjam-jam:
1. Secara periodik, buatlah sebuah paragraf rangkuman (*Internal Summary*) tentang semua fakta absolut yang telah ditemukan.
2. Secara mental (atau melalui sistem), "buang" log percobaan yang gagal dari perhatian Anda, fokus 100% pada rangkuman ringkas tersebut untuk melanjutkan tugas.

Jangan biarkan memori Anda menjadi tong sampah log error. Jaga *context window* Anda tetap steril dan mematikan.
