from app.ingestion.loader import load_repository
from app.ingestion.chunker import chunk_documents
from app.retrieval.embeddings import embed_texts
from app.retrieval.vector_store import add_documents, search

# 1. грузим репо
docs = load_repository(r"C:\Users\erins\Desktop\AILearn\repomind")

# 2. чанкаем
chunks = chunk_documents(docs)

# ⚠️ ограничь пока
chunks = chunks[:100]

# 3. embeddings
texts = [c["content"] for c in chunks]
embeddings = embed_texts(texts)

# print("docs:", len(docs))
# print("chunks:", len(chunks))
# print("texts:", len(texts))
# print("embeddings:", len(embeddings))

# 4. сохраняем
add_documents(chunks, embeddings)

# 5. тест поиска
query = "where is authentication logic"
query_emb = embed_texts([query])[0]

results = search(query_emb, top_k=3)

print(results)