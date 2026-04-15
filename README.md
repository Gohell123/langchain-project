# Multi-Tool Agentic RAG System

A **production-style Agentic AI system** built with **LangChain**, combining **RAG, Search, and Tool-based reasoning** with chat memory and smart routing.

---

## Features

* **Agentic AI** with multi-tool reasoning
* **RAG (Pinecone + HuggingFace Embeddings)**
* **Real-time Search (Tavily API)**
* **Context-aware Query Routing**
* **Chat Memory (multi-turn conversations)**
* **Optimized performance (conditional LLM calls)**

---

## Architecture


User Query
   ↓
Router
   ↓
 ├── Search → Summarization
 ├── RAG → Knowledge Retrieval
 └── Agent → Tool Execution
```


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
git clone https://github.com/Gohell123/multi-tool-agentic-rag.git
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

* Built **hybrid AI system (Agent + RAG + Search)**
* Implemented **memory-aware routing for follow-up queries**
* Reduced latency using **conditional summarization**
* Designed **robust tool calling with input normalization**

---

## Author

**Mandeep Saini**
