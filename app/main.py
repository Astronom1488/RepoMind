from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.ingestion.loader import load_repository, list_repository_files
from app.ingestion.chunker import chunk_documents
from app.retrieval.embeddings import embed_texts
from app.retrieval.vector_store import add_documents
from app.retrieval.retriever import retrieve_context_data
from app.llm.generator import generate_answer


app = FastAPI(title="RepoMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IndexRequest(BaseModel):
    repo_path: str


class AskRequest(BaseModel):
    question: str


class FilesRequest(BaseModel):
    repo_path: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/index")
def index_repository(request: IndexRequest):
    try:
        print("[INDEX] start")
        print(f"[INDEX] repo_path = {request.repo_path}")

        documents = load_repository(request.repo_path)
        print(f"[INDEX] documents loaded = {len(documents)}")

        if not documents:
            raise HTTPException(status_code=400, detail="No supported files found in repository")

        chunks = chunk_documents(documents)
        print(f"[INDEX] chunks created = {len(chunks)}")

        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks were created")

        texts = [chunk["content"] for chunk in chunks]
        print(f"[INDEX] texts prepared = {len(texts)}")

        embeddings = embed_texts(texts)
        print(f"[INDEX] embeddings created = {len(embeddings)}")

        add_documents(chunks, embeddings)
        print("[INDEX] documents added to vector store")

        return {
            "status": "success",
            "documents_indexed": len(documents),
            "chunks_indexed": len(chunks)
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[INDEX ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/files")
def get_repository_files(request: FilesRequest):
    try:
        files = list_repository_files(request.repo_path)

        if not files:
            raise HTTPException(status_code=400, detail="No supported files found in repository")

        return {
            "repo_path": request.repo_path,
            "count": len(files),
            "files": files
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
def ask_question(request: AskRequest):
    try:
        retrieval_result = retrieve_context_data(request.question)

        context = retrieval_result["context"]
        sources = retrieval_result["sources"]

        if not context:
            raise HTTPException(status_code=404, detail="No relevant context found")

        answer = generate_answer(context, request.question)

        return {
            "question": request.question,
            "context": context,
            "sources": sources,
            "answer": answer
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))