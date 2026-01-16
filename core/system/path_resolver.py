import os
from typing import Optional, Dict, Any

from core.system.config import HOME_DIR


# -------------------------------------------------
# Allowed base directories (sandbox)
# -------------------------------------------------

ALLOWED_DIRS = {
    "home": HOME_DIR,
    "desktop": os.path.join(HOME_DIR, "Desktop"),
    "downloads": os.path.join(HOME_DIR, "Downloads"),
    "documents": os.path.join(HOME_DIR, "Documents"),
}


# -------------------------------------------------
# Base directory resolution
# -------------------------------------------------

def resolve_base_path(text: str) -> Optional[str]:
    """
    Resolve spoken directory names to absolute paths.
    Only allows HOME and known subfolders.
    """
    if not text:
        return HOME_DIR

    text = text.lower()

    for key, path in ALLOWED_DIRS.items():
        if key in text:
            if os.path.isdir(path):
                return path
            return None

    # Default to HOME if nothing explicit
    return HOME_DIR


# -------------------------------------------------
# File path resolution (SAFE)
# -------------------------------------------------

def resolve_file_path(filename: str, base_dir: str) -> Optional[str]:
    """
    Resolve a file path safely inside base_dir.
    Prevents path traversal.
    Does NOT read or modify files.
    """
    if not filename or not base_dir:
        return None

    # Normalize filename only (no directory guessing)
    filename = filename.strip().replace("..", "")
    candidate = os.path.abspath(os.path.join(base_dir, filename))

    # Sandbox enforcement
    if not candidate.startswith(HOME_DIR):
        return None

    if os.path.isfile(candidate):
        return candidate

    return None


# -------------------------------------------------
# Day 54: Path preview (READ-ONLY)
# -------------------------------------------------

def build_path_preview(path: str) -> Optional[Dict[str, Any]]:
    """
    Build a safe, read-only preview of a file or directory.

    Returns metadata ONLY.
    No file reads.
    No mutations.
    """

    if not path:
        return None

    path = os.path.abspath(path)

    # Sandbox enforcement
    if not path.startswith(HOME_DIR):
        return None

    if not os.path.exists(path):
        return None

    preview: Dict[str, Any] = {
        "path": path,
        "type": "directory" if os.path.isdir(path) else "file",
    }

    try:
        stat = os.stat(path)
    except OSError:
        return None

    if os.path.isfile(path):
        preview["size"] = _format_size(stat.st_size)

    return preview


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _format_size(size_bytes: int) -> str:
    """
    Human-readable file size.
    """
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes} {unit}"
        size_bytes //= 1024
    return f"{size_bytes} TB"
