# 🌐 38 — Inter-Agent Protocols

> *"Menetapkan Standar Protokol Agen (RFC-level), serta antarmuka RESTful dan WebSocket untuk koordinasi antar-platform agen."*

---

## 📋 Daftar Isi
1. [Filosofi Protokol Antar-Agen](#-filosofi-protokol-antar-agen)
2. [Spesifikasi RFC Inter-Agent Coordination (IAC-1)](#-spesifikasi-rfc-inter-agent-coordination-iac-1)
3. [Antarmuka RESTful API (RESTful Endpoints)](#-antarmuka-restful-api-restful-endpoints)
4. [Komunikasi Real-time Melalui WebSocket (WebSocket Interface)](#-komunikasi-real-time-melalui-websocket-websocket-interface)
5. [Arsitektur Jaringan Agen (Agent Network Topology)](#-arsitektur-jaringan-agen-agent-network-topology)
6. [Skema Payload Pertukaran Protokol (Protocol Payload Schema)](#-skema-payload-pertukaran-protokol-protocol-payload-schema)

---

## 🎯 Filosofi Protokol Antar-Agen

Di masa depan (SOTA 2026), tidak ada satu agen pun yang menyelesaikan seluruh tugas kompleks sendirian. Agen dari platform berbeda (misalnya, Google Antigravity, Cursor, Autogen) harus dapat berkolaborasi. **Inter-Agent Protocol** menetapkan tata krama komunikasi, negosiasi tugas, penyerahan status (state handoff), serta pertukaran data terstruktur secara aman tanpa batas hambatan bahasa internal model.

---

## 📄 Spesifikasi RFC Inter-Agent Coordination (IAC-1)

Dokumen ini mendefinisikan standar **IAC-1** untuk koordinasi agen terdistribusi.

### Status Komunikasi:
*   `DISCOVERY`: Tahap pencarian kemampuan agen lain di jaringan lokal/global.
*   `NEGOTIATION`: Agen saling menawarkan harga token, estimasi waktu penyelesaian, dan kompetensi.
*   `EXECUTION`: Agen utama menugaskan sub-task ke agen spesialis.
*   `HANDOVER`: Pengiriman hasil eksekusi lengkap dengan bukti audit.

### Jenis Sinyal Pesan:
1.  **Request for Proposal (RFP)**: Meminta agen lain untuk mengajukan penawaran eksekusi.
2.  **Proposal**: Pernyataan kesediaan agen untuk menjalankan tugas dengan estimasi biaya/waktu.
3.  **Handoff**: Pengalihan token sesi dan state payload ke agen tujuan.

---

## ⚙️ Antarmuka RESTful API (RESTful Endpoints)

RESTful API digunakan untuk interaksi request-response synchronous jarak jauh antar-platform.

### Endpoints Standard:
*   `POST /v1/agent/handshake`: Memulai negosiasi sesi.
*   `POST /v1/agent/propose`: Mengirimkan penawaran pengerjaan sub-tugas.
*   `POST /v1/agent/handoff`: Melakukan serah terima konteks dan kontrol tugas.

### Implementasi Node.js (Express & TypeScript):

```typescript
import express, { Request, Response, Router } from 'express';

export const agentRouter: Router = Router();

interface HandoffPayload {
  sessionId: string;
  sourceAgentId: string;
  targetAgentId: string;
  contextState: Record<string, any>;
}

agentRouter.post('/handoff', async (req: Request, res: Response) => {
  const payload: HandoffPayload = req.body;
  
  if (!payload.sessionId || !payload.contextState) {
    return res.status(400).json({ error: 'Invalid handoff configuration payloads.' });
  }

  try {
    console.log(`[IAC-1 Handoff] Received state from ${payload.sourceAgentId} for session ${payload.sessionId}`);
    
    // Process context validation internally before accepting state control
    const isStateAccepted = validateIncomingContext(payload.contextState);
    if (!isStateAccepted) {
      return res.status(422).json({ error: 'Context state validation failed. Rejected handoff.' });
    }

    // Acknowledge acceptance
    return res.status(200).json({
      status: 'ACCEPTED',
      targetAgentId: payload.targetAgentId,
      acceptedAt: new Date().toISOString()
    });
  } catch (error) {
    return res.status(500).json({ error: 'Internal system error during state transfer.' });
  }
});

function validateIncomingContext(state: Record<string, any>): boolean {
  // Simple check for required workspace paths
  return !!state.workingDirectory;
}
```

---

## 🔌 Komunikasi Real-time Melalui WebSocket (WebSocket Interface)

Untuk interaksi asinkronus dengan latensi rendah (seperti perdebatan multi-agen real-time), WebSocket adalah pilihan utama.

```typescript
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WebSocket) => {
  console.log('[IAC-1 WS] New agent connection established.');

  ws.on('message', (message: string) => {
    try {
      const data = JSON.parse(message);
      
      switch (data.type) {
        case 'HEARTBEAT':
          ws.send(JSON.stringify({ type: 'ACK', timestamp: new Date().toISOString() }));
          break;
        case 'BROADCAST_RFP':
          // Distribute task request to all other connected agent instances
          broadcastToAgents(data);
          break;
        default:
          console.warn(`[IAC-1 WS] Unknown event pattern: ${data.type}`);
      }
    } catch (e) {
      ws.send(JSON.stringify({ error: 'Bad JSON format' }));
    }
  });
});

function broadcastToAgents(payload: any): void {
  // Mock broadcasting logic
  console.log(`Broadcasting RFP for task: ${payload.taskName}`);
}
```

---

## 🗺️ Arsitektur Jaringan Agen (Agent Network Topology)

```
[Agent Initiator (Antigravity)]
        │
        ├─► (WebSocket Conn) ──► [Central Agent Hub Router]
        │                                  │
        │                                  ├──► [Agent Coder (Cursor)]
        │                                  │
        │                                  └──► [Agent Tester (Local CLI)]
        │
        └─► (REST POST Handshake) ──► [Remote Enterprise Cloud Agent]
```

---

## 📄 Skema Payload Pertukaran Protokol (Protocol Payload Schema)

Skema validasi JSON untuk format data pengiriman status (*handoff*) antar-agen:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InterAgentHandoffPayload",
  "type": "object",
  "properties": {
    "protocolVersion": { "type": "string", "const": "IAC-1" },
    "sessionId": { "type": "string", "format": "uuid" },
    "handoverTimestamp": { "type": "string", "format": "date-time" },
    "sourceAgent": {
      "type": "object",
      "properties": {
        "agentId": { "type": "string" },
        "platform": { "type": "string" }
      },
      "required": ["agentId", "platform"]
    },
    "contextMetadata": {
      "type": "object",
      "properties": {
        "currentTaskDescription": { "type": "string" },
        "executionPath": { "type": "string" },
        "variablesRegistry": { "type": "object" }
      },
      "required": ["currentTaskDescription"]
    }
  },
  "required": ["protocolVersion", "sessionId", "handoverTimestamp", "sourceAgent", "contextMetadata"]
}
```
