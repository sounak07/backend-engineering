[Source](https://newsletter.pragmaticengineer.com/p/cursor)

# 📒 Comprehensive Notes on Cursor’s Architecture

## 1. **Product Positioning**

- Cursor is not just “Copilot with chat” → it’s an **AI-first IDE**.
    
- Based on a **fork of VS Code** (Electron + TypeScript), so inherits VS Code’s ecosystem but with deeper AI integration.
    
- Focus: **speed, privacy, developer trust**, and scaling enterprise adoption.
    

---

## 2. **Frontend (Editor Layer)**

- **Fork of VS Code** → allows control of UX without reinventing an editor.
    
- **Electron** framework.
    
- **TypeScript** for most business logic.
    
- **Cursor-specific UX**:
    
    - “Tab model” autocomplete (inline gray suggestions, Tab to accept).
        
    - Chat mode integrated with context of codebase.
        
    - Memory, background agents, and AI code review (BugBot).
        

---

## 3. **Backend Architecture**

- **Monolithic backend** (not microservices) → helps move fast.
    
- **TypeScript**: most business logic.
    
- **Rust**: performance-critical components (indexing, orchestrator, sync engine).
    
- **Node.js ↔ Rust bridge** → heavy compute tasks (like indexing) run in Rust but triggered from TypeScript logic.
    

---

## 4. **Autocomplete / Tab Model**

Workflow when you type in Cursor:

1. Client captures small local context window.
    
2. Context is **encrypted** and sent to backend.
    
3. Backend decrypts → runs inference on in-house LLM.
    
4. Suggestion generated and sent back.
    
5. Client displays gray inline suggestion → “Tab” accepts.
    

- **Design tradeoff**: Larger context = better suggestions, but slower latency. Cursor optimizes for <1s roundtrip.
    

---

## 5. **Chat Mode (AI with your codebase)**

- Cursor does **not store source code** server-side. Instead:
    
    1. Client builds **embeddings** (encrypted chunks of code).
        
    2. Embeddings stored in server-side vector DB.
        
    3. When you ask a question (e.g. “what does createTodo() do?”):
        
        - Server runs **vector search** → finds best-matching embeddings.
            
        - Server requests relevant files/snippets from client.
            
        - Analysis is run server-side with full context.
            
        - Response sent back to user.
            

---

## 6. **Indexing & Merkle Trees**

- **Why indexing?**  
    Enables fast code search + chat without storing full code.
    
- **Process:**
    
    1. Files split into **chunks**.
        
    2. Encrypted chunks → embeddings created server-side (GPU heavy).
        
    3. Embeddings stored in Turbopuffer / Pinecone.
        
- **Keeping index fresh:**
    
    - Cursor uses **Merkle trees** (hash tree structure).
        
    - Client = source of truth, server = last indexed state.
        
    - Every 3 mins, Merkle trees compared → only changed files re-indexed.
        
    - Saves bandwidth + GPU compute.
        
- **Security:**
    
    - Respects `.gitignore` and `.cursorignore`.
        
    - Pre-scan avoids sending secrets (API keys, passwords, env files).
        

---

## 7. **Data & Storage**

- **Databases:**
    
    - Turbopuffer → multi-tenant DB for encrypted files + Merkle trees.
        
    - Pinecone → vector DB for embeddings (docs, code search).
        
    - Previously tried Yugabyte → too complex → moved to Postgres → scaled to Turbopuffer.
        
- **Streaming:** Warpstream (Kafka-compatible).
    

---

## 8. **Infra / Orchestration**

- **Anyrun**: custom orchestrator (Rust service).
    
    - Launches agents in cloud securely.
        
    - Runs on AWS EC2 + AWS Firecracker for isolation.
        
- **Cloud strategy:**
    
    - CPU infra → AWS.
        
    - GPU infra → Azure (NVIDIA H100 GPUs).
        
    - Other GPU clouds for training/fine-tuning.
        
- **Terraform** → manages infra.
    

---

## 9. **Observability & Tooling**

- **Datadog** → heavy usage (logs, metrics, tracing).
    
- **PagerDuty** → on-call.
    
- **Sentry** → error monitoring.
    
- **Amplitude** → analytics.
    
- **Linear** → task management.
    
- **Slack** → internal comms.
    

---

## 10. **Business + Engineering Culture**

- **Releases every 2–4 weeks**.
    
- **Strong feature-flag discipline** → conservative rollouts.
    
- **Dedicated infra team** → scaling, outages, migrations.
    
- **Experimentation culture** → test, learn, ship fast.
    
- **Dogfooding**: Engineers use Cursor to build Cursor → constant feedback loop.
    

---

## 11. **Key Engineering Challenges**

- Balancing **latency vs. context size** in autocomplete.
    
- **Cold starts** on large codebases.
    
- **Sharding + scaling** vector DBs.
    
- **Hard-to-detect outages** in sync/indexing pipelines.
    
- **Large migrations** (Yugabyte → Postgres → Turbopuffer in hours during outage).
    

---

## 12. **Numbers to Remember**

- **50 engineers**.
    
- **7M lines of code, 25k files** in codebase.
    
- **1M+ TPS** backend load.
    
- **100M+ lines of code/day** written with Cursor by enterprise clients.
    
- **$500M+ ARR** (within 2 yrs).
    
- **Thousands of H100 GPUs**.
    

---

✅ **Mental Model for Cursor’s Architecture**

- **Editor UX layer** (VS Code fork + AI features)
    
- **Sync + Indexing layer** (low-latency + Merkle tree-based)
    
- **Inference layer** (LLMs on GPUs for autocomplete & chat)
    
- **Storage layer** (encrypted embeddings in Turbopuffer/Pinecone)
    
- **Infra + Orchestration layer** (Anyrun, AWS/Azure, Firecracker)
    
- **Monitoring + Ops layer** (Datadog, PagerDuty, etc.)