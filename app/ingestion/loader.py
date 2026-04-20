import os
from typing import List, Dict

SUPPORTED_EXTENSIONS = [".py", ".js", ".ts", ".md", ".txt", ".json"]

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    "dist",
    "build"
}

def load_repository(repo_path: str) -> List[Dict]:
    documents = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1]

            if ext not in SUPPORTED_EXTENSIONS:
                continue

            full_path = os.path.join(root, file)

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    documents.append({
                        "content": content,
                        "metadata": {
                            "path": full_path,
                            "extension": ext,
                        },
                    })
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
        
    return documents


