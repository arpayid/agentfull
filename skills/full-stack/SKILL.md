---
name: Full Stack Integration
description: Penyelarasan client-server, sinkronisasi state data, dan deployment monorepo.
---

# 🛠️ Full Stack Integration

## 1. Client/Server State Synchronization
Menyelaraskan data antara client dan server secara efisien tanpa membebani jaringan. Strategi utama meliputi:
- **Optimistic Updates**: Mengupdate UI di sisi client secara instan sebelum server mengembalikan respons sukses. Jika server gagal, UI di-rollback.
- **Polling (Short & Long)**: Request berkala untuk mendeteksi perubahan data.
- **WebSockets / Server-Sent Events (SSE)**: Koneksi persisten dua arah (WebSockets) atau satu arah dari server (SSE) untuk update real-time.
- **Revalidation Strategies**: Menggunakan pustaka seperti React Query / SWR dengan strategi stale-while-revalidate.

```typescript
// Example: Optimistic Update using TanStack Query (React Query)
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface Todo {
  id: string;
  title: string;
  completed: boolean;
}

export function useUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (updatedTodo: Todo) => {
      const response = await fetch(`/api/todos/${updatedTodo.id}`, {
        method: 'PUT',
        body: JSON.stringify(updatedTodo),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    },
    // Perform optimistic update
    onMutate: async (newTodo) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);

      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old ? old.map((t) => (t.id === newTodo.id ? { ...t, ...newTodo } : t)) : []
      );

      return { previousTodos };
    },
    // Rollback if mutation fails
    onError: (err, newTodo, context) => {
      if (context?.previousTodos) {
        queryClient.setQueryData(['todos'], context.previousTodos);
      }
    },
    // Always refetch after success or error
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
}
```

## 2. Monorepo Management (Turborepo & Lerna)
Monorepo mempermudah pengelolaan banyak project dan shared libraries dalam satu repositori tunggal.

- **Turborepo**: Build system berkinerja tinggi untuk JavaScript/TypeScript monorepo. Menggunakan remote caching untuk menghemat waktu kompilasi.
- **Lerna**: Framework optimasi workflow monorepo untuk mengelola versi package dan dependency publish.

```json
// Example: turborepo configuration (turbo.json)
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "test/**/*.ts"]
    },
    "lint": {},
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

```json
// Example: Monorepo package.json root configuration
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}
```

## 3. Webpack & Vite Optimization
Memaksimalkan kecepatan build dan performa runtime frontend aplikasi melalui optimasi bundler.

- **Vite Optimization**:
  - `rollupOptions` split chunks.
  - Pre-bundling dependencies menggunakan Esbuild.
- **Webpack Optimization**:
  - Tree shaking (menghapus dead code).
  - Code splitting menggunakan `optimization.splitChunks`.
  - Minifikasi dengan TerserPlugin dan CssMinimizerPlugin.

```javascript
// Example: Vite Configuration optimization (vite.config.ts)
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'esnext',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react') || id.includes('react-dom')) {
              return 'react-vendor';
            }
            if (id.includes('@tanstack')) {
              return 'query-vendor';
            }
            return 'vendor';
          }
        },
      },
    },
  },
});
```

## 4. Modern Hybrid Rendering (SSR, SSG, ISR)
Strategi rendering modern untuk mengoptimalkan Core Web Vitals (LCP, FID, CLS) dan SEO:

- **SSR (Server-Side Rendering)**: Render halaman HTML di setiap request server. Baik untuk konten dinamis yang cepat berubah.
- **SSG (Static Site Generation)**: Build halaman HTML sekali saja saat build-time. Latensi sangat rendah.
- **ISR (Incremental Static Regeneration)**: Mengupdate halaman statis secara bertahap di latar belakang tanpa membangun kembali seluruh situs.

```typescript
// Example: Next.js Pages Router implementing ISR and SSR
import { GetStaticProps, GetServerSideProps } from 'next';

interface Product {
  id: string;
  name: string;
  price: number;
}

// 1. Incremental Static Regeneration (ISR)
export const getStaticProps: GetStaticProps = async () => {
  const res = await fetch('https://api.example.com/products');
  const products: Product[] = await res.json();

  return {
    props: {
      products,
    },
    // Re-generate the page at most once every 60 seconds
    revalidate: 60,
  };
};

// 2. Server-Side Rendering (SSR) - Dynamic implementation fallback example
export const getServerSideProps: GetServerSideProps = async (context) => {
  const { id } = context.query;
  const res = await fetch(`https://api.example.com/products/${id}`);
  const product: Product = await res.json();

  return {
    props: {
      product,
    },
  };
};
```
