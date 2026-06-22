---
name: TypeScript Type Safety
description: Deep dive into TypeScript type system, generics, memory safety, async futures, and npm/pnpm compilation.
---

# 🛠️ TypeScript Type Safety

## 1. Memory Management & Lifecycles
Meskipun TypeScript menambahkan sistem pengetikan (type system) statis pada saat kompilasi, runtime-nya sepenuhnya berupa JavaScript biasa (JavaScript Engine seperti V8, JavaScriptCore, atau SpiderMonkey). Oleh karena itu, siklus hidup memori mengikuti aturan JavaScript Heap.

### Compilation vs Runtime Memory
- TypeScript bertindak sebagai lapisan penunjuk kesalahan statis sebelum eksekusi (*static analysis*).
- Seluruh anotasi tipe data, antarmuka (`interface`), dan tipe alias (`type`) dihapus sepenuhnya (*type erasure*) saat proses transpilasi menjadi JavaScript.
- Penggunaan struktur data seperti `WeakMap` dan `WeakSet` sangat disarankan untuk menjaga agar referensi objek tidak menghalangi proses pengumpulan sampah (Garbage Collection) ketika objek induknya dihancurkan.

---

## 2. Concurrency & Parallelism
TypeScript menggunakan API asinkronus bawaan JavaScript (`Promise`, `async/await`) serta runtime multithreaded jika dijalankan di Node.js (via `worker_threads`) atau di browser (via `Web Workers`).

### Type Safety in Async Workflows
TypeScript memperkuat operasi asinkronus dengan membungkus hasil akhir ke dalam tipe generik `Promise<T>`.
- **`async` function**: Selalu mengembalikan tipe `Promise<T>`.
- **`await` expression**: Mengekstrak tipe `T` dari `Promise<T>` secara otomatis pada tingkat kompilator.
- TypeScript mencegah kesalahan konkurensi dengan memaksa pengembang menangani kemungkinan penolakan janji (*Promise rejection*) menggunakan blok `try/catch` atau `.catch()`, meskipun ia tidak dapat mendeteksi kondisi balapan (*race condition*) tingkat runtime tanpa logika sinkronisasi tambahan.

---

## 3. Dependency & Build Systems
Ekosistem TypeScript memanfaatkan pengelola paket standar (seperti `npm`, `yarn`, atau `pnpm`) dan kompilator resmi `tsc`.

### Configuration (`tsconfig.json`)
Konfigurasi `tsconfig.json` yang ketat menjamin kualitas kode:
- `strict: true`: Mengaktifkan semua pemeriksaan tipe ketat, termasuk `noImplicitAny`, `strictNullChecks`, dan `strictFunctionTypes`.
- `target`: Menentukan versi ECMAScript keluaran (misal `ES2022`).
- `moduleResolution`: Menentukan bagaimana modul dicari di dalam folder proyek, biasanya disetel ke `node` atau `nodenext` untuk integrasi modul ESM (ES Modules) modern.

---

## 4. Real-world Code Implementation
Berikut adalah implementasi sistem pemrosesan pesan (Message Broker client) sederhana yang menjamin keamanan tipe (*type safety*) data pesan yang masuk menggunakan TypeScript Generics dan Type Guards.

```typescript
interface BaseMessage {
  id: string;
  timestamp: number;
}

interface UserRegisteredMessage extends BaseMessage {
  type: "USER_REGISTERED";
  payload: {
    userId: string;
    email: string;
  };
}

interface OrderCreatedMessage extends BaseMessage {
  type: "ORDER_CREATED";
  payload: {
    orderId: string;
    totalAmount: number;
  };
}

type Message = UserRegisteredMessage | OrderCreatedMessage;

// Type Guard Functions
function isUserRegisteredMessage(msg: Message): msg is UserRegisteredMessage {
  return msg.type === "USER_REGISTERED";
}

function isOrderCreatedMessage(msg: Message): msg is OrderCreatedMessage {
  return msg.type === "ORDER_CREATED";
}

class MessageDispatcher {
  private handlers: { [K in Message["type"]]?: (msg: any) => Promise<void> } = {};

  registerHandler<T extends Message>(
    type: T["type"],
    handler: (msg: T) => Promise<void>
  ): void {
    this.handlers[type] = handler;
  }

  async dispatch(rawMessage: unknown): Promise<void> {
    // Basic verification of incoming unknown payload
    if (typeof rawMessage !== "object" || rawMessage === null) {
      throw new Error("Invalid message format: must be an object");
    }

    const msg = rawMessage as Message;
    const handler = this.handlers[msg.type];

    if (!handler) {
      console.warn(`No handler registered for message type: ${msg.type}`);
      return;
    }

    if (isUserRegisteredMessage(msg)) {
      await (handler as (msg: UserRegisteredMessage) => Promise<void>)(msg);
    } else if (isOrderCreatedMessage(msg)) {
      await (handler as (msg: OrderCreatedMessage) => Promise<void>)(msg);
    } else {
      const _exhaustiveCheck: never = msg;
      throw new Error(`Unhandled message type: ${JSON.stringify(msg)}`);
    }
  }
}

// Example Execution
async function run() {
  const dispatcher = new MessageDispatcher();

  dispatcher.registerHandler<UserRegisteredMessage>("USER_REGISTERED", async (msg) => {
    console.log(`Processing User Registration: ${msg.payload.email} (${msg.payload.userId})`);
  });

  dispatcher.registerHandler<OrderCreatedMessage>("ORDER_CREATED", async (msg) => {
    console.log(`Processing Order Creation: $${msg.payload.totalAmount} (Order: ${msg.payload.orderId})`);
  });

  const incomingPayload = {
    id: "msg-101",
    timestamp: Date.now(),
    type: "USER_REGISTERED",
    payload: {
      userId: "user_abc123",
      email: "test@domain.com",
    },
  };

  await dispatcher.dispatch(incomingPayload);
}

run().catch(console.error);
```
