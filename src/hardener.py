"""Prompt-hardening operation."""
from __future__ import annotations

from pathlib import Path


def harden_prompt(project_root: Path) -> Path:
    source = project_root / "config" / "hardened_prompt.txt"
    target = project_root / "config" / "hardened_prompt.txt"
    text = source.read_text(encoding="utf-8")
    target.write_text(text, encoding="utf-8")
    return target