# 🔀 29 — Graph-based Associative Memory

> *"Menghubungkan potongan memori ke dalam relasi modular demi penalaran kontekstual yang lebih kaya."*

---

## 📋 Daftar Isi

1. [Filosofi Memori Asosiatif](#-filosofi-memori-asosiatif)
2. [Arsitektur Database Graf Memori](#-arsitektur-database-graf-memori)
3. [Aliran Navigasi Asosiatif](#-aliran-navigasi-asosiatif)
4. [Pola Pengambilan Data](#-pola-pengambilan-data)

---

## 🎯 Filosofi Memori Asosiatif

Graph-based Associative Memory adalah **metode penyimpanan memori agen menggunakan skema graf**. Berbeda dengan basis data vektor yang murni mencari kemiripan teks (cosine similarity), graf memetakan hubungan ketergantungan antar modul logika (misal: "Mengubah `auth.service.ts` $\rightarrow$ berdampak pada `auth.controller.ts` dan tabel `sessions`").

---

## 🏗️ Arsitektur Database Graf Memori

```
          ┌────────────────┐
          │ auth.service   │
          └───────┬────────┘
             rel: modify_impacts
                  ▼
          ┌────────────────┐         rel: schema_depends       ┌──────────────┐
          │ auth.controller│ ────────────────────────────────► │ sessions tab │
          └────────────────┘                                   └──────────────┘
```

---

## ⚙️ Pola Pengambilan Data

Saat agen diperintahkan memodifikasi berkas target, agen pertama-tama menanyakan graf asosiatif untuk menarik seluruh berkas yang memiliki relasi dependensi tinggi ke dalam working memory (Modul 06).
