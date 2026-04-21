# RepoMind

RepoMind is a local Retrieval-Augmented Generation (RAG) assistant designed to help understand and navigate a codebase. It indexes a repository, breaks files into manageable chunks, generates embeddings, and enables semantic search combined with LLM-based explanations.

---

## Overview

RepoMind provides a simple pipeline for exploring and reasoning about code:

Repository → Loader → Chunker → Embeddings → Vector Store → Retrieval → LLM

It allows you to ask questions about a project and receive answers grounded in the actual source code, along with references to relevant files and line ranges.

---

## Features

* Index a local repository
* Line-based chunking of files
* Embeddings using Sentence Transformers
* Vector search with ChromaDB
* Question answering over code
* Source-aware responses (file paths and line ranges)
* Repository file listing via API
* Minimal web interface for interaction

---

## Architecture

### Ingestion

* Traverses repository files
* Filters by extension and size
* Ignores system and dependency directories

### Chunking

* Splits files into line-based chunks
* Maintains metadata:

  * file path
  * chunk id
  * line_start / line_end

### Embeddings

* Uses `sentence-transformers/all-MiniLM-L6-v2`
* Converts chunks into vector representations

### Storage

* Stores embeddings and metadata in ChromaDB

### Retrieval

* Performs semantic search (top-k)
* Applies additional keyword-based scoring
* Deduplicates results per file
* Expands context with neighboring chunks

### Generation

* Sends retrieved context to a local LLM (via Ollama)
* Produces structured answers:

  * short answer
  * relevant files
  * explanation

---

## API

### POST /index

Indexes a repository.

Request:

```json
{
  "repo_path": "path/to/repository"
}
```

Response:

```json
{
  "status": "success",
  "documents_indexed": 120,
  "chunks_indexed": 850
}
```

---

### POST /ask

Asks a question about the indexed repository.

Request:

```json
{
  "question": "How does chunk_text work?"
}
```

Response:

```json
{
  "question": "...",
  "answer": "...",
  "context": "...",
  "sources": [
    {
      "path": "...",
      "line_start": 1,
      "line_end": 20,
      "preview": "..."
    }
  ]
}
```

---

### POST /files

Returns a list of repository files.

Request:

```json
{
  "repo_path": "path/to/repository"
}
```

Response:

```json
{
  "repo_path": "...",
  "count": 42,
  "files": [
    "app/main.py",
    "app/ingestion/chunker.py"
  ]
}
```

---

## How to Run

### Backend

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
python -m http.server 3000
```

Open in browser:

http://127.0.0.1:3000

---

## Example Questions

* How does chunk_text work?
* What is the difference between chunk_text and chunk_documents?
* Which file handles embeddings?
* How does the retrieval logic rank results?
* What does this project do?

---

## Limitations

* Local LLM performance depends on hardware
* Retrieval is relatively simple and may include noise
* No incremental indexing or change tracking
* File tree is not hierarchical (flat list)
* No authentication or multi-user support

---

## Roadmap

* Improved retrieval ranking and filtering
* Multiple answer modes (Explain, Debug, Architecture)
* File tree visualization
* Streaming responses
* Incremental indexing
* Better chunking for code structure (functions/classes)

---

## Notes

This project is built as a learning-focused implementation of a RAG pipeline. The goal is to understand the full flow from raw repository data to LLM-powered answers, rather than rely on high-level frameworks.
