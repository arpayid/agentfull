# 🧠 28 — Dynamic KV-Cache Compaction & Memory Compression

> *"Kurangi redundansi token tanpa kehilangan esensi sejarah eksekusi."*

---

## 📋 Daftar Isi

1. [Filosofi Pemadatan KV-Cache](#-filosofi-pemadatan-kv-cache)
2. [Arsitektur Kompresi KV-Cache (KV-Cache Compression Architecture)](#-arsitektur-kompresi-kv-cache-kv-cache-compression-architecture)
3. [Algoritma Kompresi Semantik (Semantic Compression Algorithm)](#-algoritma-kompresi-semantik-semantic-compression-algorithm)
4. [Tabel Klasifikasi Jenis Log (Log Category Matrix)](#-tabel-klasifikasi-jenis-log-log-category-matrix)
5. [Format Pruning Log Konteks (Context Log Pruning Format)](#-format-pruning-log-konteks-context-log-pruning-format)
6. [Implementasi Kode Pemadatan (Compaction Python Script)](#-implementasi-kode-pemadatan-compaction-python-script)
7. [Mitigasi Kehilangan Konteks Penting (Loss Minimization Protocols)](#-mitigasi-kehilangan-konteks-penting-loss-minimization-protocols)
8. [Anti-Patterns Pemadatan KV-Cache](#-anti-patterns-pemadatan-kv-cache)

---

## 🎯 Filosofi Pemadatan KV-Cache

Dynamic KV-Cache Compaction adalah **sekumpulan mekanisme pemangkasan token history secara cerdas**. Saat interaksi dengan developer berlangsung terlalu lama, log stderr terminal dan output pengujian yang panjang akan memenuhi memori. Sistem memadatkan history tersebut menjadi metadata ringkas sehingga konsumsi token input tetap konstan dan efisien. Hal ini meminimalkan biaya token dan latensi inferensi.

---

## 🏗️ Arsitektur Kompresi KV-Cache

Cache dipotong secara dinamis dengan mengidentifikasi status keberhasilan eksekusi:

```
┌─────────────────────────────────┐
│ System Logs / Command History   │ (Raw Context Stack)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ Semantic Compactor filter       ├──────► [Remove resolved errors]
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ Compacted System Prompt State   │ (Reduced Context Size)
└─────────────────────────────────┘
```

---

## ⚙️ Algoritma Kompresi Semantik

Sistem membagi history menjadi unit-unit logis:
* `Compressible`: Log output compiler yang sudah berhasil diperbaiki (buang atau ganti dengan tanda `[compiler check passed]`).
* `Incompressible`: Konvensi yang disepakati pengguna dan keputusan rancangan arsitektur utama.

---

## 📊 Tabel Klasifikasi Jenis Log

| Jenis Log | Kompresibilitas | Metode Penanganan | Contoh Penanganan |
| :--- | :--- | :--- | :--- |
| **Compiler Error Stacks** | Sangat Tinggi | Hapus / Ringkas ke Kode Error | Pangkas trace error 50 baris menjadi `TS2322 at line 14`. |
| **User Requirements** | Nol (Incompressible) | Pertahankan Kata demi Kata | Simpan utuh di memori utama. |
| **Local File Index** | Sedang | Ubah ke Struktur Tree Ringkas | Ubah path list panjang menjadi ASCII tree. |

---

## 📝 Format Pruning Log Konteks

### Sebelum Pemadatan (Raw context log):
```yaml
log_history: |
  TypeError at line 14: getUser is undefined
    at getUserDetails (src/user.ts:14:12)
    at handleRequest (src/server.ts:45:2)
    at runTest (tests/server.test.ts:12:1)
  [1000 lines of trace...]
```

### Setelah Pemadatan (Compacted context log):
```yaml
log_history_compact: "TypeError at line 14 (Resolved: added null validation check to user.ts)"
```

---

## 💻 Implementasi Kode Pemadatan

Skrip Python berikut memindai daftar pesan percakapan dan memadatkan data output CLI yang panjang:

```python
import re

class KVCacheCompactor:
    def __init__(self, max_length: int = 150):
        self.max_length = max_length

    def compact_log_text(self, log_text: str) -> str:
        # If log is short, keep it
        if len(log_text) < self.max_length:
            return log_text
            
        # Pattern to scan for standard stack traces
        if "at " in log_text or "Error:" in log_text:
            lines = log_text.splitlines()
            first_line = lines[0] if lines else "Error"
            # Extract error code if present
            error_code_match = re.search(r"(TS\d+|TypeError|ReferenceError|ValueError)", log_text)
            err_code = error_code_match.group(1) if error_code_match else "RuntimeError"
            return f"[Compacted Log: {err_code} - {first_line[:50]}... (lines truncated: {len(lines)})]"
        
        return log_text[:self.max_length] + "... [truncated]"

# Usage Example:
# compactor = KVCacheCompactor()
# small_log = compactor.compact_log_text("TypeError: Cannot read property 'id' of undefined\n  at getUser...")
# print(small_log)
```

---

## 🛡️ Mitigasi Kehilangan Konteks Penting

* **Memory Summarization Loop**: Jalankan sub-model berkala untuk merangkum hasil penting sebelum memangkas riwayat chat secara masif.
* **Anchor Points**: Tandai berkas konfigurasi penting (seperti `package.json` atau `tsconfig.json`) sebagai file indeks statis yang tidak boleh dipangkas dari cache memori utama.

---

## ⚠️ Anti-Patterns Pemadatan KV-Cache

* ❌ **Radical Truncation**: Memotong log mentah secara acak tanpa menganalisis apakah terdapat instruksi user penting di dalamnya.
* ❌ **No History Compaction**: Menyimpan seluruh log run test build yang panjang selama 20 iterasi berturut-turut, menyebabkan token overflow.
* ❌ **Losing Original Instructions**: Menghapus gol awal pengguna (User Goal) saat merapikan context window.
