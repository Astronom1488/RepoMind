import chromadb
from chromadb.config import Settings
from typing import List, Dict

client = chromadb.Client(
    Settings(
        persist_directory="chroma_db"
    )
)

collection = client.get_or_create_collection(name="repomind")


def add_documents(chunks: List[Dict], embeddings: List[List[float]]):
    """
    Сохраняем чанки + embeddings
    """
    documents = [c["content"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [f"{m['path']}_{m['chunk_id']}" for m in metadatas]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=ids
    )


def search(query_embedding: List[float], top_k: int = 5):
    """
    Поиск похожих чанков
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results