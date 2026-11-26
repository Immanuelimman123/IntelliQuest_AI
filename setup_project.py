
from pathlib import Path

folders = [
    "frontend",
    "backend",
    "backend/models",
    "backend/document_processing",
    "backend/rag",
    "backend/agents",
    "backend/orchestration",
    "backend/mcp_server",
    "backend/database",
    "backend/evaluation",
    "storage/uploads",
    "storage/reports",
    "tests"
]

files = [
    "app.py",
    "config.py",
    "requirements.txt",
    ".env",
    ".gitignore",
    "README.md",
    "backend/__init__.py",
    "backend/models/__init__.py",
    "backend/document_processing/__init__.py",
    "backend/rag/__init__.py",
    "backend/agents/__init__.py",
    "backend/orchestration/__init__.py",
    "backend/mcp_server/__init__.py",
    "backend/database/__init__.py",
    "backend/evaluation/__init__.py"
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file in files:
    Path(file).touch(exist_ok=True)

print("IntelliQuest_AI structure created successfully!")
