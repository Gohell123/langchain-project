# Multi-Tool Agentic RAG System


A **production-style Agentic AI system** built using **LangChain**, combining **RAG, Search, and Tool-based reasoning** with intelligent routing, memory, and latency optimizations.

---

## Key Features

- **Agentic AI with Tool Calling (ReAct-style reasoning)**
- **Intelligent Query Routing (Chat | RAG | Search | Agent)**
- **RAG Pipeline (Pinecone + HuggingFace Embeddings)**
- **Real-time Web Search (Tavily API)**
- **Conversation Memory (multi-turn context handling)**
- **Multi-layer Caching (Exact + Semantic)**
- **Latency Optimization (conditional LLM + tool-first execution)**
- **Input Guardrails (vague / irrelevant query handling)**

---

## Architecture

A[User Query] --> B[Agent (LLM)] B --> C{Decide Action} 
C -->|RAG| D[Vector DB (Pinecone)] 
C -->|Search| E[Web Search] 
C -->|Tool| F[Custom Tools] 

D --> G[Context] 
E --> G 
F --> G 

G --> H[LLM Response] 
H --> I[Final Answer]
```

## ⚙️ Core Components

### 🔹 Router
- Rule-based intent classification
- Context-aware follow-up handling
- Prevents unnecessary agent execution (latency optimization)

### 🔹 Agent
- ReAct-style reasoning with tool calling
- Handles multi-step queries and business logic
- Integrated with:
  - Price Tool
  - Discount Tool
  - RAG Tool

### RAG Pipeline
- Embeddings: HuggingFace (`all-MiniLM-L6-v2`)
- Vector DB: Pinecone
- Optimized retrieval using:
  - similarity threshold
  - top-k filtering

### Search
- Tavily API for real-time external knowledge
- Optional summarization for noisy results

### Caching Layer
- Exact match caching
- Semantic caching (embedding similarity)
- Reduces repeated LLM and tool calls significantly



## Performance Optimizations

- Reduced unnecessary LLM calls via routing
- Tool-first execution for deterministic queries
- Semantic caching for similar queries
- Trimmed context + controlled memory window
- Conditional summarization for large responses


## Tech Stack

* LangChain
* Pinecone
* HuggingFace Embeddings
* Tavily API
* Gemini / Ollama
* Python 3.12

---

## Setup

```bash
git clone https://github.com/Gohell123/langchain-project/tree/multi-tool-agentic-rag-system
cd multi-tool-agentic-rag

uv venv
.venv\Scripts\activate   # Windows

uv sync
python app.py
```

---

## Example

```text
User: What is the price of laptop?
AI: $1299.99

User: any discounts?
AI: Please specify discount tier

User: gold
AI: Final price = $1104.99
```

---

## Highlights

- Designed a hybrid AI system (Agent + RAG + Search)
- Implemented context-aware routing for multi-turn conversations
- Built multi-layer caching (exact + semantic) for latency reduction
- Solved tool selection ambiguity in agent systems
- Applied production-level optimizations (latency, fallback, guardrails)

---

## Agent 
Business Tools -Query Product Price and apply Discounts
RAG - Stores VectorDB Theoritical Concepts
WebSearch - General Query

## Author

**Mandeep Saini**
