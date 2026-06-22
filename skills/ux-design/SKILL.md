---
name: UX Design for Developers
description: Prinsip hierarki visual, wireframing, usability testing, dan aksesibilitas web.
---

# 🛠️ UX Design for Developers

## 1. Design System Integration
Integrasi design system menjamin konsistensi visual dan efisiensi pengembangan. Pengembang harus memahami:
- **Design Tokens**: Nilai-nilai atomik (warna, font-size, spacing, shadow) yang didefinisikan secara agnostik dari platform dan direferensikan ke dalam kode.
- **Component Componentization**: Membuat komponen pembungkus dasar (Button, Input, Card) sebelum membangun layout kompleks.

```json
// Example: Figma-exported Design Tokens file (tokens.json)
{
  "color": {
    "brand": {
      "primary": { "value": "#4f46e5", "type": "color" },
      "secondary": { "value": "#06b6d4", "type": "color" }
    },
    "neutral": {
      "background": { "value": "#f9fafb", "type": "color" },
      "text": { "value": "#111827", "type": "color" }
    }
  },
  "spacing": {
    "xs": { "value": "4px", "type": "dimension" },
    "sm": { "value": "8px", "type": "dimension" },
    "md": { "value": "16px", "type": "dimension" },
    "lg": { "value": "24px", "type": "dimension" }
  }
}
```

## 2. Component Hierarchy
Hierarki komponen menentukan cara komponen berkomunikasi dan tersusun. Ikuti pola pengelompokan berdasarkan fungsionalitas:
1. **Atoms**: Elemen UI dasar yang tidak bisa dipecah lagi (misalnya `<Button />`, `<Label />`).
2. **Molecules**: Gabungan atom membentuk fungsi sederhana (misalnya `<SearchField />` = `<Input />` + `<Button />`).
3. **Organisms**: Gabungan molekul membentuk bagian interface kompleks (misalnya `<HeaderNavbar />`).
4. **Templates/Pages**: Tata letak halaman penuh.

```tsx
// Example: React + TypeScript Component Hierarchy implementation
import React from 'react';

// Atom
export const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = ({ children, ...props }) => (
  <button className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700" {...props}>
    {children}
  </button>
);

// Atom
export const Input: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = (props) => (
  <input className="border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500" {...props} />
);

// Molecule (Input + Button)
export const SearchBar: React.FC<{ onSearch: (val: string) => void }> = ({ onSearch }) => {
  const [val, setVal] = React.useState('');
  return (
    <div className="flex gap-2">
      <Input placeholder="Cari data..." value={val} onChange={(e) => setVal(e.target.value)} />
      <Button onClick={() => onSearch(val)}>Search</Button>
    </div>
  );
};
```

## 3. Accessibility Rules (WCAG 2.1 Compliance)
Memastikan produk digital dapat diakses oleh semua orang, termasuk penyandang disabilitas.
- **Warna Kontras**: Minimum rasio kontras 4.5:1 untuk teks normal, dan 3:1 untuk teks besar (WCAG AA).
- **Keyboard Navigation**: Semua elemen interaktif harus dapat dijangkau dan dioperasikan menggunakan keyboard (`Tab`, `Enter`, `Spacebar`).
- **Semantic HTML**: Menggunakan elemen yang tepat (`<header>`, `<nav>`, `<main>`, `<button>`) alih-alih `<div>` sembarangan.
- **ARIA Attributes**: Menyediakan label deskriptif tambahan untuk screen reader.

```html
<!-- Example: WCAG 2.1 Compliant Accessible Form -->
<form action="/submit" method="POST">
  <!-- Semantic label associated explicitly with input via 'for' -> 'id' -->
  <div class="form-group">
    <label for="user-email" class="block text-sm font-medium text-gray-700">Email Address</label>
    <input 
      type="email" 
      id="user-email" 
      name="email" 
      required
      aria-required="true"
      aria-describedby="email-hint"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
    />
    <p id="email-hint" class="mt-2 text-sm text-gray-500">We will never share your email address.</p>
  </div>

  <!-- Interactive element with accessible name and visible focus state -->
  <button 
    type="submit" 
    class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
  >
    Submit Form
  </button>
</form>
```

## 4. Tailwind Configuration
Kustomisasi konfigurasi Tailwind CSS untuk mengamankan standardisasi visual tokens yang telah ditentukan.

```javascript
// Example: tailwind.config.js customized for corporate design token limits
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          light: '#e0e7ff',
          DEFAULT: '#4f46e5',
          dark: '#3730a3',
        },
        neutral: {
          surface: '#f9fafb',
          foreground: '#111827',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '72': '18rem',
        '84': '21rem',
      },
      boxShadow: {
        'brand-focus': '0 0 0 3px rgba(79, 70, 229, 0.4)',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

## 5. Visual Layout Optimizations
Menerapkan optimasi tata letak agar mata pengguna diarahkan dengan alur membaca yang nyaman (F-pattern dan Z-pattern).
- **Whitespace / Negative Space**: Memberi ruang bernapas pada elemen UI untuk mengurangi beban kognitif.
- **Cumulative Layout Shift (CLS) Reduction**: Selalu tentukan rasio aspek gambar atau berikan skeleton loader sebelum aset dimuat agar layout tidak bergeser secara tiba-tiba.

```tsx
// Example: Reducing CLS using Image Aspect Ratio and Skeleton Fallbacks
import React from 'react';

export const ImageCard: React.FC<{ imageUrl: string; title: string }> = ({ imageUrl, title }) => {
  const [loaded, setLoaded] = React.useState(false);

  return (
    <div className="max-w-sm rounded overflow-hidden shadow-lg bg-white">
      {/* Aspect Ratio Box to reserve space and prevent layout shifts (CLS) */}
      <div className="relative w-full aspect-video bg-gray-200">
        {!loaded && (
          <div className="absolute inset-0 animate-pulse bg-gray-300 flex items-center justify-center">
            <span className="sr-only">Loading image...</span>
          </div>
        )}
        <img
          src={imageUrl}
          alt={title}
          onLoad={() => setLoaded(true)}
          className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-300 ${
            loaded ? 'opacity-100' : 'opacity-0'
          }`}
        />
      </div>
      <div className="px-6 py-4">
        <h3 className="font-bold text-xl mb-2 text-gray-900">{title}</h3>
      </div>
    </div>
  );
};
```
