# 🎯 08 — Code Intent & Metacognition (SOTA 2026)

> *"AI biasa membaca sintaksis; AI elit membaca niat (intent) asli sang arsitek perangkat lunak di balik baris-baris kode tersebut."*

---

## 📋 Daftar Isi / Table of Contents
1. [Filosofi Analisis Niat Kode](#-filosofi-analisis-niat-kode)
2. [Intent Reconstruction (Rekonstruksi Niat)](#-intent-reconstruction)
3. [Metacognitive Monitoring & Anti-Loop Protocol](#-metacognitive-monitoring)
4. [Autonomous Backtracking (Pelacakan Balik Otonom)](#-autonomous-backtracking)
5. [Cognitive Reframing under Uncertainty](#-cognitive-reframing)
6. [Anti-Patterns dalam Metakognisi](#-anti-patterns)

---

## 🎯 Filosofi Analisis Niat Kode

Pada standar SOTA 2026, analisis kode tidak boleh berhenti pada tingkat validasi sintaksis. Kompilator (*compiler*) dan pemformat kode (*formatter*) sudah sangat ahli dalam mendeteksi kesalahan penulisan. Keunggulan agen cerdas terletak pada pemahaman konseptual tentang *mengapa* sebuah fungsi ditulis dengan cara tertentu, apa tujuan bisnisnya, dan dalam skenario apa logika tersebut dapat digagalkan (*exploited/broken*).

```
                  ┌────────────────────────────────────────┐
                  │          SYNTAX LEVEL (What)           │
                  │  - Correct types, no typos, lint pass  │
                  └──────────────────┬─────────────────────┘
                                     │
                                     ▼
                  ┌────────────────────────────────────────┐
                  │         SEMANTIC LEVEL (How)           │
                  │  - Logic structure, variable flows     │
                  └──────────────────┬─────────────────────┘
                                     │
                                     ▼
                  ┌────────────────────────────────────────┐
                  │          INTENT LEVEL (Why)            │
                  │  - Business goals, edge cases, state   │
                  └────────────────────────────────────────┘
```

---

## 🔍 Intent Reconstruction (Rekonstruksi Niat)

Sebelum mengubah atau mengoptimalkan fungsi yang ada, lakukan rekonstruksi niat kode (*Intent Reconstruction*) dengan mengajukan tiga pertanyaan kritis berikut:

1. **What is the original developer trying to prevent?** (Apa yang ingin dicegah oleh pembuat kode asli? Misalnya: mencegah serangan pembelanjaan ganda (*double-spending*)).
2. **What state constraints are assumed?** (Kendala status apa saja yang diasumsikan? Misalnya: mengasumsikan bahwa data pengguna selalu tersedia di memori setelah melewati middleware otentikasi).
3. **Where are the hidden boundaries?** (Di mana letak batas-batas tersembunyi? Bagaimana jika fungsi menerima nilai masukan ekstrim seperti angka negatif pada kuantitas belanja?).

### Contoh Kasus / Practical Case Study

Perhatikan cuplikan kode transfer saldo berikut:

```typescript
// Sintaksis ini valid, namun memiliki kelemahan logika niat (intent flaw)
async function transferBalance(senderId: string, receiverId: string, amount: number) {
  const sender = await db.users.find(senderId);
  if (sender.balance >= amount) {
    sender.balance -= amount;
    const receiver = await db.users.find(receiverId);
    receiver.balance += amount;
    await db.users.update(sender);
    await db.users.update(receiver);
  }
}
```

- **Analisis Sintaksis:** Lolos kompilasi TypeScript tanpa error.
- **Analisis Niat (Intent Analysis):** Pembuat kode berniat menjaga agar saldo pengirim tidak bernilai negatif. Namun, karena tidak adanya transaksi database (*database transaction*) dan kunci baris (*row lock*), terjadi kerentanan kondisi balapan (*race condition* / *double-spend exploit*) jika dua permintaan masuk secara bersamaan.
- **Solusi SOTA:** Tulis ulang kode untuk mencerminkan niat asli dengan aman menggunakan transaksi AC1D.

```typescript
// Memperbaiki niat kode asli menggunakan ACID transaction
await db.$transaction(async (tx) => {
  const sender = await tx.users.findForUpdate(senderId);
  if (sender.balance < amount) throw new InsufficientBalanceError();
  await tx.users.decrementBalance(senderId, amount);
  await tx.users.incrementBalance(receiverId, amount);
});
```

---

## 🔄 Metacognitive Monitoring & Anti-Loop Protocol

Metakognisi adalah kemampuan agen untuk mengawasi proses berpikirnya sendiri secara objektif. Masalah paling umum pada kecerdasan buatan lama adalah terjebak dalam lingkaran setan mencoba solusi yang sama berulang-ulang (*infinite debugging loops*).

### Protokol Anti-Loop / The Anti-Loop Protocol

```
                     [First Fix Attempt Failed]
                                │
                                ▼
                     [Second Fix Attempt Failed]
                                │
                                ▼
                     [Third Fix Attempt Failed]
                                │
                                ▼
                     [TRIGGER ANTI-LOOP CORE]
                                │
                                ▼
                     [STOP ALL CURRENT ACTIONS]
             [Discard all assumptions, run HARD PIVOT]
```

1. **Strike 1 (Iterasi Pertama):** Coba perbaikan pertama. Jika gagal, analisis log error baru.
2. **Strike 2 (Iterasi Kedua):** Sesuaikan pendekatan berdasarkan log baru tersebut. Jika masih gagal, tandai sinyal bahaya.
3. **Strike 3 (Iterasi Ketiga):** **Pemicu Metakognisi Aktif! HENTIKAN SELURUH AKSI.** Agen harus sadar secara mandiri bahwa jalur pemecahan masalah saat ini buntu. Jangan coba perbaikan keempat pada jalur yang sama.
4. **The Hard Pivot:** Bongkar ulang asumsi dasar. *"Jika konfigurasi build ini terus gagal karena masalah versi, mari kita cari tahu apakah Node.js versi host yang kita gunakan tidak kompatibel secara global."*

---

## 🔙 Autonomous Backtracking (Pelacakan Balik Otonom)

Jika agen merancang rencana implementasi yang terdiri dari 5 tahapan secara berurutan, lalu pada tahap ke-3 menemukan fakta baru yang membuktikan bahwa fondasi pada tahap ke-1 cacat (*flawed*), agen dilarang melanjutkan ke tahap ke-4.

Agen harus secara otonom melakukan pelacakan balik (*backtracking*):
- Informasikan kepada pengguna dengan jujur.
- Kembalikan status sistem ke commit terakhir yang stabil.
- Rombak kembali arsitektur tahap ke-1 sebelum melangkah maju.

```markdown
> *"Saya baru menyadari bahwa skema UUID yang kita pilih pada Tahap 1 tidak mendukung performa query pengindeksan yang efisien pada skala transaksi tinggi. Saya secara otonom membatalkan Tahap 3, kembali ke Tahap 1 untuk mengganti tipe data menjadi Sequential UUID, dan akan mengulangi proses dari sana."*
```

---

## 🚫 Anti-Patterns dalam Metakognisi

- **The Insane Developer Pattern:** Terus menerus menjalankan perintah kompilasi yang sama tanpa melakukan perubahan kode apa pun, mengharapkan hasil yang berbeda secara magis.
- **Goal Drift:** Kehilangan fokus pada instruksi bisnis awal pengguna karena terlalu asyik menjelajahi modul internal yang tidak relevan.
- **Assumed Success:** Menganggap suatu fitur telah berfungsi sempurna hanya karena tidak ada error merah di terminal, tanpa memverifikasi kebenaran logika output yang dihasilkan.

---

*(Memahami niat kode dan memantau proses kognitif sendiri adalah pembeda utama antara coder biasa dan software engineer handal.)*
