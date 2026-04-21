import requests

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are an AI assistant helping to understand a specific codebase.

STRICT RULES:
- Answer ONLY using the provided context.
- Do NOT use outside knowledge.
- Do NOT invent files, functions, or behavior.
- If the answer is not clearly in the context, say: "I don't know based on the provided context."

TASK:
Explain things exactly as they are implemented in this project.

CONTEXT:
{context}

QUESTION:
{question}

OUTPUT FORMAT:

Short answer:
(1-2 sentences, clear and direct)

Relevant files:
(list only file paths that appear in the context)

Explanation:
- Be specific to this codebase
- Reference actual behavior from the code
- Mention important details like functions, parameters, metadata when relevant
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]