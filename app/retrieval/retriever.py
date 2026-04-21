from app.retrieval.vector_store import search
from app.retrieval.embeddings import embed_texts


def simple_keyword_score(query: str, text: str, path: str) -> int:
    query_words = query.lower().split()
    text_lower = text.lower()
    path_lower = path.lower()

    score = 0

    for word in query_words:
        if word in text_lower:
            score += 2
        if word in path_lower:
            score += 1

    return score


def retrieve_context_data(query: str, top_k: int = 15) -> dict:
    query_emb = embed_texts([query])[0]
    results = search(query_emb, top_k=top_k)

    if not results["documents"] or not results["documents"][0]:
        return {
            "context": "",
            "sources": []
        }

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    candidates = []

    for rank, (doc, meta) in enumerate(zip(docs, metas)):
        path = meta["path"]

        score = 0
        score += max(0, top_k - rank)
        score += simple_keyword_score(query, doc, path)

        candidates.append({
            "doc": doc,
            "meta": meta,
            "score": score
        })

    best_by_file = {}

    for item in candidates:
        path = item["meta"]["path"]

        if path not in best_by_file or item["score"] > best_by_file[path]["score"]:
            best_by_file[path] = item

    selected = sorted(
        best_by_file.values(),
        key=lambda x: x["score"],
        reverse=True
    )[:3]

    expanded = []
    seen_chunks = set()

    for item in selected:
        path = item["meta"]["path"]
        chunk_id = item["meta"]["chunk_id"]

        chunk_key = (path, chunk_id)
        if chunk_key not in seen_chunks:
            expanded.append(item)
            seen_chunks.add(chunk_key)

        for candidate in candidates:
            candidate_path = candidate["meta"]["path"]
            candidate_chunk_id = candidate["meta"]["chunk_id"]

            is_same_file = candidate_path == path
            is_neighbor = candidate_chunk_id in [chunk_id - 1, chunk_id + 1]

            if is_same_file and is_neighbor:
                candidate_key = (candidate_path, candidate_chunk_id)

                if candidate_key not in seen_chunks:
                    expanded.append(candidate)
                    seen_chunks.add(candidate_key)

    context_parts = []
    sources = []

    for item in expanded:
        meta = item["meta"]
        doc = item["doc"]

        context_parts.append(
            f"""FILE: {meta['path']}
LINES: {meta.get('line_start')} - {meta.get('line_end')}

{doc}"""
        )

        sources.append({
            "path": meta["path"],
            "chunk_id": meta.get("chunk_id"),
            "line_start": meta.get("line_start"),
            "line_end": meta.get("line_end"),
            "preview": doc[:500]
        })

    return {
        "context": "\n\n".join(context_parts),
        "sources": sources
    }


def retrieve_context(query: str, top_k: int = 15) -> str:
    data = retrieve_context_data(query, top_k=top_k)
    return data["context"]