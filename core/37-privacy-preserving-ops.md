# 🔒 37 — Privacy-Preserving Operations

> *"Melindungi data sensitif melalui masking PII otonom, eksekusi template zero-knowledge, dan menghasilkan mock data dinamis yang aman."*

---

## 📋 Daftar Isi
1. [Filosofi Keamanan & Privasi Operasi](#-filosofi-keamanan--privasi-operasi)
2. [Penyaringan PII & Data Sensitif (PII & Sensitive Data Masking)](#-penyaringan-pii--data-sensitif-pii--sensitive-data-masking)
3. [Template Eksekusi Zero-Knowledge (Zero-Knowledge Execution Templates)](#-template-eksekusi-zero-knowledge-zero-knowledge-execution-templates)
4. [Pembuatan Data Tiruan Dinamis (Secure Dynamic Mock Data Generation)](#-pembuatan-data-tiruan-dinamis-secure-dynamic-mock-data-generation)
5. [Arsitektur Sensor Privasi Agen (Agent Privacy Shield Architecture)](#-arsitektur-sensor-privasi-agen-agent-privacy-shield-architecture)
6. [Skema Kebijakan Sanitasi Data (Data Sanitization Policy Schema)](#-skema-kebijakan-sanitasi-data-data-sanitization-policy-schema)

---

## 🎯 Filosofi Keamanan & Privasi Operasi

Ketika agen AI mengeksekusi perintah di server produksi atau membaca basis data korporat (SOTA 2026), risiko kebocoran data pribadi (PII - Personally Identifiable Information) sangat tinggi. Agen wajib bertindak dengan arsitektur privasi berlapis. Sebelum mengirimkan teks atau data apa pun ke penyedia LLM eksternal, agen harus mendeteksi, menyamarkan (*masking*), atau menyintesis data sensitif tersebut agar tidak melanggar kepatuhan hukum seperti GDPR, CCPA, atau UU PDP.

---

## 🛡️ Penyaringan PII & Data Sensitif (PII & Sensitive Data Masking)

Penyaringan PII otonom dilakukan sebelum payload API dikirimkan ke model LLM. Entitas seperti email, nomor kartu kredit, alamat IP, kata sandi, dan nomor telepon diganti dengan token representasional (placeholder).

### Jenis Penyamaran (Masking Types):
*   **Tokenization**: Mengganti `John Doe` menjadi `[USER_NAME_1]`.
*   **Redaction**: Menghapus total data sensitif seperti `admin_pass_123` menjadi `[REDACTED_PASSWORD]`.
*   **Hashing**: Mengubah data menjadi representasi hash satu arah SHA-256 untuk memfasilitasi integritas pengujian tanpa mengekspos data mentah.

### Implementasi Masking Engine di Python:

```python
import re
from typing import Dict, Tuple

class PrivacyMasker:
    def __init__(self):
        # High confidence regex patterns for SOTA 2026 PII entities
        self.patterns = {
            "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "IP_ADDRESS": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "API_KEY": r"(?i)(?:key|secret|token|password|auth)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{16,})['\"]"
        }

    def mask_text(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Masks PII inside the text and returns the masked text 
        along with a mapping table for de-masking later.
        """
        demask_map = {}
        masked_text = text
        
        for pii_type, regex in self.patterns.items():
            matches = re.findall(regex, masked_text)
            for idx, match in enumerate(set(matches)):
                # If API_KEY pattern catches the whole assignation, we extract and mask only the value
                target = match[0] if isinstance(match, tuple) else match
                placeholder = f"[{pii_type}_{idx}]"
                demask_map[placeholder] = target
                masked_text = masked_text.replace(target, placeholder)
                
        return masked_text, demask_map

    def restore_text(self, masked_text: str, demask_map: Dict[str, str]) -> str:
        """Restores the original values back into the response."""
        restored = masked_text
        for placeholder, original in demask_map.items():
            restored = restored.replace(placeholder, original)
        return restored
```

---

## 🧩 Template Eksekusi Zero-Knowledge (Zero-Knowledge Execution Templates)

Zero-Knowledge Execution memastikan bahwa data rahasia diproses secara lokal di sandbox aman milik pengguna, sedangkan LLM di awan hanya menerima template logika abstrak tanpa mengetahui isi data tersebut.

*   **Langkah 1**: LLM membuat logika query generik: `SELECT * FROM users WHERE email = [PARAM_1]`.
*   **Langkah 2**: Klien lokal menggabungkan query dengan data riil `[PARAM_1] = "user@domain.com"` di memori RAM tertutup.
*   **Langkah 3**: Hasil dieksekusi secara lokal dan hanya agregasi statistik tanpa PII yang dikirimkan kembali ke LLM.

---

## 🧪 Pembuatan Data Tiruan Dinamis (Secure Dynamic Mock Data Generation)

Untuk kebutuhan unit testing dan simulasi kegagalan, agen harus mampu membangkitkan data tiruan (mock data) yang secara statistik mirip dengan data asli, namun tidak mengandung informasi privat yang sesungguhnya.

```typescript
import { faker } from '@faker-js/faker';

interface MockUser {
  id: string;
  name: string;
  email: string;
  balance: number;
}

export function generateSecureMockUsers(count: number): MockUser[] {
  const mockUsers: MockUser[] = [];
  for (let i = 0; i < count; i++) {
    mockUsers.push({
      id: faker.string.uuid(),
      name: faker.person.fullName(), // Synthesized realistic names
      email: faker.internet.email(),
      balance: parseFloat(faker.finance.amount({ min: 10, max: 10000, dec: 2 }))
    });
  }
  return mockUsers;
}
```

---

## 🗺️ Arsitektur Sensor Privasi Agen (Agent Privacy Shield Architecture)

```
[Local Raw Workspace Data / Log]
               │
               ▼
   [Privacy Shield Masker] ──► (Generates Local De-mask Map)
               │
               ▼
[Masked Payload (Safe for Web)]
               │
               ▼
      [External Cloud LLM]
               │
               ▼
    [Masked Model Response]
               │
               ▼
    [De-masking Restorer] ◄── (Reads Local De-mask Map)
               │
               ▼
[Final Safe Execution / Action]
```

---

## 📄 Skema Kebijakan Sanitasi Data (Data Sanitization Policy Schema)

Skema validasi JSON untuk mendefinisikan aturan pembersihan data di lingkungan runtime:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DataSanitizationPolicy",
  "type": "object",
  "properties": {
    "policyName": { "type": "string" },
    "enabledMasks": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["EMAIL", "IP_ADDRESS", "CREDIT_CARD", "API_KEY", "PHONE_NUMBER"]
      }
    },
    "customRules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ruleId": { "type": "string" },
          "patternRegex": { "type": "string" },
          "replacement": { "type": "string" }
        },
        "required": ["ruleId", "patternRegex", "replacement"]
      }
    },
    "allowFallbackOnFailure": { "type": "boolean" }
  },
  "required": ["policyName", "enabledMasks"]
}
```
