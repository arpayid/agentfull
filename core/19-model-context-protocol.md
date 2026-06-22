# 🔌 19 — Model Context Protocol (MCP) Integration

> *"Standardisasi interaksi tool dynamic adalah kunci skalabilitas ekosistem agen AI."*

---

## 📋 Daftar Isi

1. [Filosofi MCP](#-filosofi-mcp)
2. [Arsitektur Server-Client MCP (Server-Client Architecture)](#-arsitektur-server-client-mcp-server-client-architecture)
3. [Skema Pertukaran JSON-RPC 2.0 (Communication Schema)](#-skema-pertukaran-json-rpc-20-communication-schema)
4. [Implementasi MCP Client (Client Code Fragment)](#-implementasi-mcp-client-client-code-fragment)
5. [Konfigurasi Server MCP (Server Configuration YAML)](#-konfigurasi-server-mcp-server-configuration-yaml)
6. [Mitigasi Kegagalan Sambungan (Failover Protocols)](#-mitigasi-kegagalan-sambungan-failover-protocols)
7. [Anti-Patterns Integrasi MCP](#-anti-patterns-integrasi-mcp)

---

## 🎯 Filosofi MCP

Model Context Protocol (MCP) adalah **standar terbuka** untuk menghubungkan LLM ke data sources dan eksekutor tool secara modular. Dibanding mengkodekan tool manual satu per satu, agen cukup menjadi MCP Client yang berbicara ke berbagai MCP Servers (Database, GitHub API, Slack). Hal ini mengurangi overhead pemeliharaan kode integration.

---

## 🏗️ Arsitektur Server-Client MCP

Arsitektur MCP memisahkan klien (kognisi agen) dari server (akses data dan kemampuan sistem):

```
                     ┌──────────────────┐
                     │   AI Agent       │ (MCP Client)
                     └────────┬─────────┘
                              │ JSON-RPC 2.0 (stdio or SSE)
                     ┌────────┴─────────┐
                     │   MCP Router     │
                     └─┬──────────────┬─┘
                       │              │
       ┌───────────────┴┐            ┌┴────────────────┐
       │ DB MCP Server  │            │ GitHub Server   │ (MCP Servers)
       └────────────────┘            └─────────────────┘
```

---

## ⚙️ Skema Pertukaran JSON-RPC 2.0

Komunikasi dinamis menggunakan format JSON-RPC melalui input/output standar (stdio) atau Server-Sent Events (SSE).

### 1. Request List Tools (`tools/list`):
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 1
}
```

### 2. Response List Tools:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "read_file",
        "description": "Read file contents from the workspace",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": { "type": "string" }
          },
          "required": ["path"]
        }
      }
    ]
  },
  "id": 1
}
```

---

## 💻 Implementasi MCP Client

Berikut adalah kode Node.js sederhana untuk menghubungkan Client ke Server MCP melalui proses `stdio`:

```javascript
const { spawn } = require('child_process');

class MCPClient {
  constructor(serverPath) {
    this.serverProcess = spawn('node', [serverPath]);
    this.requestId = 1;
    this.callbacks = {};

    this.serverProcess.stdout.on('data', (data) => {
      const response = JSON.parse(data.toString());
      if (this.callbacks[response.id]) {
        this.callbacks[response.id](response.result || response.error);
        delete this.callbacks[response.id];
      }
    });
  }

  callTool(toolName, args) {
    return new Promise((resolve, reject) => {
      const id = this.requestId++;
      const payload = {
        jsonrpc: '2.0',
        method: 'tools/call',
        params: { name: toolName, arguments: args },
        id
      };
      
      this.callbacks[id] = (result) => {
        if (result.code) reject(result); // Contains error structure
        else resolve(result);
      };

      this.serverProcess.stdin.write(JSON.stringify(payload) + '\n');
    });
  }
}

// Usage
// const client = new MCPClient('./sqlite-mcp-server.js');
// client.callTool('query_db', { sql: 'SELECT * FROM users' }).then(console.log);
```

---

## 🛠️ Konfigurasi Server MCP

Berikut konfigurasi JSON-RPC router untuk menghubungkan client ke beberapa server backend:

```json
{
  "mcpServers": {
    "sqlite-server": {
      "command": "node",
      "args": ["/usr/local/bin/sqlite-mcp-server.js"],
      "env": {
        "DB_PATH": "/workspace/prod.db"
      }
    },
    "github-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

---

## 🛡️ Mitigasi Kegagalan Sambungan

* **Fallback ke Shell Lokal**: Jika koneksi MCP server terputus atau timeout, agen harus mengalihkan runtime kembali ke command line lokal (Local Shell) daripada menghentikan eksekusi tugas.
* **Mekanisme Reconnection**: Hubungkan kembali server proses secara otomatis setelah jeda waktu tertentu (exponential backoff).

---

## ⚠️ Anti-Patterns Integrasi MCP

* ❌ **Hardcoded Server Paths**: Menggunakan path absolut statis untuk executable server di mesin host yang berbeda.
* ❌ **No Error Handling**: Mengabaikan kemacetan proses stdout/stdin pada server, yang menyebabkan thread agen membeku (hang).
* ❌ **Sensitive Env Leak**: Mewariskan seluruh environment variable sistem host ke proses server MCP tanpa disaring terlebih dahulu.
