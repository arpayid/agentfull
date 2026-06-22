# 👁️ 33 — Multimodal Visual Debugging

> *"Menangkap screenshot secara otonom, mengaudit regresi UI, dan melakukan validasi keselarasan desain CSS/Figma secara multimodal."*

---

## 📋 Daftar Isi
1. [Filosofi Debugging Visual Multimodal](#-filosofi-debugging-visual-multimodal)
2. [Otomatisasi Screenshot (Screenshot Capture Automation)](#-otomatisasi-screenshot-screenshot-capture-automation)
3. [Audit Regresi UI (UI Regression Auditing)](#-audit-regresi-ui-ui-regression-auditing)
4. [Validasi Keselarasan CSS & Figma (CSS & Figma Alignment Validation)](#-validasi-keselarasan-css--figma-css--figma-alignment-validation)
5. [Arsitektur Pemrosesan Citra Multimodal (Multimodal Image Processing Architecture)](#-arsitektur-pemrosesan-citra-multimodal-multimodal-image-processing-architecture)
6. [Skema Hasil Validasi Visual (Visual Validation Output Schema)](#-skema-hasil-validasi-visual-visual-validation-output-schema)

---

## 🎯 Filosofi Debugging Visual Multimodal

Pada era kecerdasan buatan multimodal (SOTA 2026), agen tidak hanya membaca HTML dan DOM tree secara tekstual. Agen juga harus "melihat" antarmuka pengguna (UI) sebagaimana manusia melihatnya. Dengan memadukan model penglihatan komputer (VLM - Vision-Language Models) dan browser otomasi, agen dapat mendeteksi rendering error, ketidaksesuaian tata letak (layout shifts), elemen yang tumpang tindih, serta deviasi gaya dari spesifikasi Figma.

---

## 📸 Otomatisasi Screenshot (Screenshot Capture Automation)

Untuk melakukan analisis visual, agen harus mengontrol browser headless seperti Playwright atau Puppeteer untuk menangkap visualisasi halaman pada berbagai resolusi viewport (desktop, tablet, mobile).

### Contoh Implementasi Playwright untuk Screenshot Capture:

```typescript
import { chromium, Browser, Page } from 'playwright';

interface ScreenshotOptions {
  url: string;
  outputPath: string;
  viewport: { width: number; height: number };
}

export async function capturePageSnapshot(options: ScreenshotOptions): Promise<void> {
  const browser: Browser = await chromium.launch({ headless: true });
  try {
    const page: Page = await browser.newPage();
    await page.setViewportSize(options.viewport);
    
    // Navigate and wait for network idle to ensure resources are loaded
    await page.goto(options.url, { waitUntil: 'networkidle' });
    
    // Hide dynamic elements like cursors or ad banners to ensure clean diffs
    await page.evaluate(() => {
      const styles = document.createElement('style');
      styles.innerHTML = '* { transition: none !important; animation: none !important; }';
      document.head.appendChild(styles);
    });

    await page.screenshot({ path: options.outputPath, fullPage: true });
    console.log(`Snapshot saved successfully at: ${options.outputPath}`);
  } catch (error) {
    console.error('Failed to capture visual snapshot:', error);
    throw error;
  } finally {
    await browser.close();
  }
}
```

---

## 🔍 Audit Regresi UI (UI Regression Auditing)

Audit regresi visual membandingkan tangkapan layar saat ini (*candidate*) dengan tangkapan layar referensi yang telah disetujui sebelumnya (*baseline*). Deteksi dilakukan menggunakan pixel-matching algorithm dengan toleransi warna yang dinamis.

### Perbandingan Pixel Menggunakan Pixelmatch di Node.js:

```javascript
const fs = require('fs');
const PNG = require('pngjs').PNG;
const pixelmatch = require('pixelmatch');

function computeVisualDiff(baselinePath, candidatePath, diffOutputPath) {
  const img1 = PNG.sync.read(fs.readFileSync(baselinePath));
  const img2 = PNG.sync.read(fs.readFileSync(candidatePath));
  const { width, height } = img1;
  const diff = new PNG({ width, height });

  const numDiffPixels = pixelmatch(
    img1.data,
    img2.data,
    diff.data,
    width,
    height,
    { threshold: 0.1, includeAA: true }
  );

  const mismatchPercentage = (numDiffPixels / (width * height)) * 100;
  fs.writeFileSync(diffOutputPath, PNG.sync.write(diff));

  return {
    mismatchPixels: numDiffPixels,
    mismatchPercentage: mismatchPercentage.toFixed(2),
    passed: mismatchPercentage < 0.05 // 0.05% tolerance threshold
  };
}
```

---

## 🎨 Validasi Keselarasan CSS & Figma (CSS & Figma Alignment Validation)

Agen menggunakan Vision LLM untuk membandingkan rendering web secara langsung dengan aset desain Figma. Agen menganalisis properti visual seperti:
*   **Typography**: Keselarasan font-family, font-size, line-height, dan font-weight.
*   **Color Palette**: Konsistensi HEX/RGBA code pada background, text, dan border.
*   **Spacing**: Jarak margin, padding, alignment grid, dan flexbox alignment.

### Alur Prompting Multimodal (System Instructions):
```
Your task is to compare the reference Figma Design (Image A) and the Candidate Web Rendering (Image B).
Analyze the layout constraints, element spacing, and typographic properties.
List any deviation in JSON format, specifying:
1. Element selector (CSS)
2. Expected value (Figma)
3. Actual rendering value (Candidate)
4. Recommended CSS fix
```

---

## 🗺️ Arsitektur Pemrosesan Citra Multimodal (Multimodal Image Processing Architecture)

```
 [Figma Mockup (JSON/Image)]           [Web App Running]
              │                                │
              ▼                                ▼
     [Figma Specs Extractor]           [Playwright Headless Browser]
              │                                │
              │                                ▼
              │                        [Candidate PNG Snapshot]
              │                                │
              └───────────────┬────────────────┘
                              ▼
                     [Vision-Language Model]
                              │
                              ▼
                     [Visual Audit Report]
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
       [Passed (0% Diff)]             [Failed (>0.05% Diff)]
             │                                 │
             ▼                                 ▼
      [Proceed Pipeline]               [Auto-CSS Refactor Loop]
```

---

## 📄 Skema Hasil Validasi Visual (Visual Validation Output Schema)

Skema validasi untuk menstandarisasi output laporan audit regresi visual:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VisualAuditReport",
  "type": "object",
  "properties": {
    "auditTimestamp": {
      "type": "string",
      "format": "date-time"
    },
    "viewports": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "device": { "type": "string" },
          "width": { "type": "integer" },
          "height": { "type": "integer" },
          "mismatchPercentage": { "type": "number" },
          "diffImageUri": { "type": "string", "format": "uri" },
          "deviations": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "cssSelector": { "type": "string" },
                "property": { "type": "string" },
                "expected": { "type": "string" },
                "actual": { "type": "string" },
                "severity": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH"] }
              },
              "required": ["cssSelector", "property", "expected", "actual", "severity"]
            }
          }
        },
        "required": ["device", "width", "height", "mismatchPercentage", "deviations"]
      }
    },
    "overallPassed": { "type": "boolean" }
  },
  "required": ["auditTimestamp", "viewports", "overallPassed"]
}
```
