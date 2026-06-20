# 📝 Change Summary

> **Kapan digunakan:** Gunakan template ini sesudah melakukan refactoring besar, menyelesaikan fitur, atau sebelum melakukan commit/merge untuk merangkum perubahan.

## 🎯 Goal
`{{GOAL_OF_THESE_CHANGES}}`

## 📦 What Was Changed

### ➕ Added
- `{{NEW_FEATURE_OR_FILE}}`

### ➖ Removed
- `{{DELETED_CODE_OR_DEPENDENCY}}`

### 🔄 Modified
- `{{MODIFIED_BEHAVIOR_OR_LOGIC}}`

## ⚠️ Risk Assessment
| Component | Risk Level | Mitigation |
|-----------|------------|------------|
| `{{COMPONENT}}` | `{{LOW/MED/HIGH}}` | `{{MITIGATION_STRATEGY}}` |

## 🧪 Testing Performed
- [ ] `{{TEST_1}}`
- [ ] `{{TEST_2}}`

---

### 📝 Example Filled Version

## 🎯 Goal
Mengganti library request HTTP internal dari `axios` ke `fetch` bawaan Node.js untuk mengurangi ukuran bundle dan dependencies.

## 📦 What Was Changed

### ➕ Added
- Menambahkan utilitas error handling kustom untuk `fetch` di `src/utils/fetch-error.ts` karena `fetch` tidak otomatis throw error pada HTTP 4xx/5xx.

### ➖ Removed
- Menghapus dependency `axios` dari `package.json`.

### 🔄 Modified
- Memperbarui semua pemanggilan API di `src/services/*` untuk menggunakan syntax `fetch`.

## ⚠️ Risk Assessment
| Component | Risk Level | Mitigation |
|-----------|------------|------------|
| `External API Calls` | **Medium** | Timeout behavior berbeda antara axios dan fetch. Ditambahkan `AbortController` untuk memastikan timeout 5 detik tetap konsisten. |
| `Error Handling` | **Low** | Struktur error berubah, namun sudah di-handle oleh interceptor/wrapper baru. |

## 🧪 Testing Performed
- [x] Menjalankan seluruh test suite (`npm run test`) -> 100% Pass.
- [x] Verifikasi manual simulasi timeout (AbortController berfungsi).
