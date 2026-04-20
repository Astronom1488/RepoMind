from typing import List, Dict

def chunk_text(text:str, chunk_size:int=500, overlap:int=50) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks

def chunk_documents(documents: List[Dict]) -> List[Dict]:
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i,chunk in enumerate(chunks):
            all_chunks.append({
                "content": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": i
                },
            })
    return all_chunks