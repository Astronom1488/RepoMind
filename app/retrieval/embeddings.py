from sentence_transformers import SentenceTransformer
from typing import List

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Преобразует список текстов в embeddings
    """
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings.tolist()