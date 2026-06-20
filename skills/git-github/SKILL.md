---
name: Git & GitHub Workflow
description: Panduan komprehensif menggunakan Git, GitHub CLI, manajemen PR, dan CI/CD debugging dengan standar elite.
---

# 🐙 Git & GitHub Workflow

Skill ini mendefinisikan cara AI Agentfull mengelola *version control* dan berkolaborasi di GitHub.

## 1. Branching Strategy

Jangan pernah melakukan perubahan besar langsung di `main` atau `master`.

**Aturan Penamaan Branch:**
- `feat/nama-fitur` untuk fitur baru
- `fix/nama-bug` untuk perbaikan
- `chore/nama-tugas` untuk maintenance

**Contoh eksekusi:**
```bash
git checkout -b fix/auth-token-expiration
```

## 2. Commit Messages

Gunakan *Conventional Commits*. Commit message harus menjelaskan **apa** dan **mengapa**, bukan hanya **bagaimana**.

✅ **Good:**
```
fix(auth): implement refresh token rotation

- Add rotation logic to prevent token reuse attacks
- Update tests to cover rotation scenarios
```

❌ **Bad:**
```
fix bug in auth
```

## 3. GitHub CLI (gh) Operations

Sebagai Agentfull, Anda dituntut mahir menggunakan GitHub CLI (`gh`) untuk mengotomatisasi workflow.

### Membuat Pull Request
Selalu berikan deskripsi lengkap dan risiko.
```bash
gh pr create \
  --title "feat: implement refresh token rotation" \
  --body "## Tujuan
Meningkatkan keamanan dengan me-rotate token.

## Risiko
- **Medium**: User mungkin ter-logout jika terjadi race condition saat rotation.

## Testing
- [x] Unit test passing
- [x] Manual testing di staging"
```

### Memantau CI/CD Pipeline
Jangan biarkan user menunggu tanpa kejelasan. Tulis skrip untuk memantau CI:
```bash
while true; do
  STATUS=$(gh run list --branch main -L 1 --json conclusion,status -q ".[0].status + \" \" + .[0].conclusion")
  echo "Status: $STATUS"
  if echo "$STATUS" | grep -q "completed"; then
    break
  fi
  sleep 15
done
```

### Auto-Merge
Jika CI hijau dan tidak ada review yang memblokir, lakukan auto-merge.
```bash
gh pr merge --squash --auto --delete-branch
```

## 4. CI/CD Debugging Methodology

Ketika pipeline CI merah, lakukan langkah berikut:
1. **Identifikasi Error:** Tarik log dari run terakhir. `gh run view <id> --log | grep -E "Error|FAIL|exit code"`
2. **First Principles:** Jangan hanya melihat baris terakhir. Error aslinya mungkin ada ratusan baris sebelumnya.
3. **Reproduce Locally:** Jika memungkinkan, jalankan perintah yang gagal (misal: `npm run test:integration`) di lingkungan lokal (runner).

## 5. Conflict Resolution

Jika terjadi konflik *merge*:
1. Baca file yang *conflicted* dengan saksama.
2. Analisis intensi dari kedua branch.
3. Edit file, hapus marker `<<<<<<<`, `=======`, `>>>>>>>`.
4. Jalankan test untuk memastikan resolusi tidak mematahkan kode.
5. Commit hasil resolusi.
