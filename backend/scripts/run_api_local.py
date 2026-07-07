"""Run the real FastAPI backend from a local checkout.

The script adds the optional local dependency folder used by Codex before
starting Uvicorn. In a regular developer environment, installed packages from a
virtualenv continue to work normally.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
LOCAL_DEPS_DIR = ROOT_DIR / ".python_deps"
BACKEND_DIR = ROOT_DIR / "backend"

for path in (LOCAL_DEPS_DIR, BACKEND_DIR):
    if path.exists():
        sys.path.insert(0, str(path))


def main() -> None:
    import uvicorn

    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = int(os.getenv("BACKEND_PORT", "8001"))
    uvicorn.run("app.api.app:app", host=host, port=port)


if __name__ == "__main__":
    main()
