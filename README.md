# Mailopolis: Multi‑agent sustainable city simulation game

A strategy game about the real politics of sustainability. Instead of optimizing a city like a spreadsheet, Mailopolis simulates multi‑agent negotiation, lobbying, and adversarial influence across departments. You (the sustainability advisor) compete against AI bad actors who try to push the city toward unsustainable outcomes.

## What it is (short)
- Multi‑agent AI system: department heads with distinct personalities, corruption resistance, and decision patterns
- Adversarial gameplay: “bad actors” actively counter you with bribery and competing proposals
- In‑app email: agents communicate via realistic government‑style email threads (rendered safely in the UI)
- Dynamic city model: overall sustainability index responds to political wins/losses and cascading policy effects

## Technical architecture
```mermaid
flowchart TD
  subgraph Frontend[UI (React + Vite, TypeScript)]
    CM[CityMap]
    IP[InboxPanel]
    LP[LogsPanel]
  end

  subgraph Backend[Backend (FastAPI, Python)]
    API[API Layer]
    GE[Game Engine]
    AMS[AgentMail Service]
    Store[(State & Conversations)]
  end

  AM[(AgentMail API)]
  SOL[(Solana Ledger)]
  MCP[MCP Server\nsolana/src/mcpServer.ts]

  CM -->|click building| IP
  IP -->|load agent inbox| API
  LP <--> API
  API <--> GE
  GE --> Store
  API <--> AMS
  AMS <--> AM
  GE -. optional events .-> SOL
  SOL -. exposed to agents .-> MCP
```

Stack
- Frontend: React 18, TypeScript, Vite, CSS
- Backend: FastAPI, asyncio, WebSocket logs, pydantic
- Email: AgentMail service for inboxes and message threads
- Optional: Solana Agent Kit + MCP server to expose an on‑chain ledger

## Install & run
Prereqs: Python 3.10+, Node 18+

Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Optional: set AGENTMAIL_API_KEY in .env for live email
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend
```bash
cd ui
npm install
npm run dev   # http://localhost:5173
```

VS Code (one‑click)
- Use the provided `.vscode/launch.json`
- Select “Mailopolis: Full Stack Debug” to run backend + `npm run dev` + open the browser

## Solana integration (optional)
- Create/maintain the ledger under `solana/`
- Expose it to agents via the MCP server at `solana/src/mcpServer.ts`
- Follow `specs.md` for how agents use the ledger in game context

## Notes
- Inbox HTML is rendered via sandboxed iframes (no `dangerouslySetInnerHTML`)
- Game conversations and state are persisted locally under `data/`

## FAQ
- Do Mermaid diagrams render on README? Yes on GitHub (native support). VS Code preview may need a Mermaid extension.
