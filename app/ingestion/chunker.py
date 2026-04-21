from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 3):
    lines = text.split("\n")
    chunks = []

    current_chunk_lines = []
    current_length = 0
    current_start_line = 1

    for i, line in enumerate(lines):
        line_length = len(line) + 1

        if current_chunk_lines and current_length + line_length > chunk_size:
            chunk_content = "\n".join(current_chunk_lines)
            line_end = current_start_line + len(current_chunk_lines) - 1

            chunks.append({
                "content": chunk_content,
                "meta": {
                    "line_start": current_start_line,
                    "line_end": line_end
                }
            })

            if overlap > 0:
                current_chunk_lines = current_chunk_lines[-overlap:]
            else:
                current_chunk_lines = []

            current_length = sum(len(l) + 1 for l in current_chunk_lines)

            if current_chunk_lines:
                current_start_line = line_end - len(current_chunk_lines) + 1
            else:
                current_start_line = i + 1

        current_chunk_lines.append(line)
        current_length += line_length

    if current_chunk_lines:
        chunk_content = "\n".join(current_chunk_lines)
        line_end = current_start_line + len(current_chunk_lines) - 1

        chunks.append({
            "content": chunk_content,
            "meta": {
                "line_start": current_start_line,
                "line_end": line_end
            }
        })

    return chunks


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "content": chunk["content"],
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": i,
                    "line_start": chunk["meta"]["line_start"],
                    "line_end": chunk["meta"]["line_end"]
                }
            })

    return all_chunks