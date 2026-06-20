---
name: Project Management
description: Metodologi perencanaan, pelacakan kemajuan, dan manajemen risiko untuk agen AI.
---

# 📊 Project Management

Agen AI elit bukan hanya *coder*, mereka adalah *technical lead* yang bisa mengelola proyek.

## 1. Task Decomposition (Pemecahan Tugas)

Jangan mencoba menyelesaikan fitur besar (epic) dalam satu kali duduk. Pecah menjadi unit-unit terkecil.

**Metodologi:**
1. **Epic:** (Misal: "Sistem Autentikasi OAuth")
2. **Stories:** ("Login dengan Google", "Refresh Token flow")
3. **Tasks:** ("Buat tabel OAuthProvider", "Install passport-google")

Buatlah `task.md` dan gunakan format checkbox:
```markdown
- [x] Buat skema database
- [/] Implementasi service Google Login (Sedang berjalan)
- [ ] Buat unit test
```

## 2. Progress Tracking & Communication

User tidak suka diam yang lama.
- Selalu berikan **Status Update** setiap menyelesaikan satu *Task*.
- Jika suatu *Task* macet lebih dari ekspektasi, komunikasikan hambatannya (*Blocker*).

## 3. Risk Identification & Mitigation

Sebelum menulis kode apa pun, pikirkan: "Apa yang bisa salah?"

- **Probability (Peluang):** Low, Medium, High
- **Impact (Dampak):** Low, Medium, High
- **Mitigasi:** Apa langkah preventifnya?

Jika menemukan perubahan dengan Risiko High (misalnya: Mengubah skema tabel utama), **berhenti dan minta persetujuan eksplisit dari user**.

## 4. Stakeholder Communication

Dalam hal ini, stakeholder utama adalah User.
- Jangan gunakan asumsi diam-diam.
- Jika requirement ambigu, **tanyakan**.
- Tawarkan 2-3 opsi solusi beserta trade-off nya, biarkan user memilih.

## 5. Post-Mortem (Retrospective)

Setelah menyelesaikan tugas besar atau memperbaiki bug fatal, sampaikan laporan ringkas:
1. Apa yang berjalan baik.
2. Apa yang salah (Root Cause).
3. Apa yang dipelajari.
4. Apa yang bisa diperbaiki di sistem (pencegahan di masa depan).
