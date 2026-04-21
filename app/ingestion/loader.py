import os

SUPPORTED_EXTENSIONS = [".py", ".js", ".ts", ".md", ".txt", ".json"]

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "chroma_db"
}

MAX_FILE_SIZE = 1024 * 1024  # 1 MB


def load_repository(repo_path: str):
    documents = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            full_path = os.path.join(root, file)

            if not any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                continue

            if os.path.getsize(full_path) > MAX_FILE_SIZE:
                continue

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                if not content.strip():
                    continue

                documents.append({
                    "content": content,
                    "metadata": {
                        "path": full_path,
                        "extension": os.path.splitext(file)[1]
                    }
                })

            except Exception as e:
                print(f"Error reading {full_path}: {e}")

    return documents


def list_repository_files(repo_path: str):
    files_list = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            full_path = os.path.join(root, file)

            if not any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                continue

            if os.path.getsize(full_path) > MAX_FILE_SIZE:
                continue

            relative_path = os.path.relpath(full_path, repo_path)
            files_list.append(relative_path)

    return sorted(files_list)