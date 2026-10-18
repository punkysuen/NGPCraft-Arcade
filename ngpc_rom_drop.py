"""Drag-and-drop helpers for NGPC ROM files."""

from __future__ import annotations

from pathlib import Path

# Same extensions as the library scanner (see ngpc_shell.ROM_EXTS).
ROM_DROP_EXTS = frozenset({".ngc", ".ngp", ".zip", ".7z"})


def is_rom_path(path: Path) -> bool:
    return path.is_file() and path.suffix.casefold() in ROM_DROP_EXTS


def rom_path_from_launch_args(args: list[str]) -> Path | None:
    """First loadable ROM path from argv (double-click .ngc or drop ROM onto .app icon)."""
    for raw in args:
        if not raw or raw.startswith("-"):
            continue
        path = Path(raw)
        if is_rom_path(path):
            return path
    return None


def rom_paths_from_local_urls(urls) -> list[Path]:
    """Extract loadable ROM paths from QUrl list (e.g. mimeData().urls())."""
    out: list[Path] = []
    for url in urls:
        if not url.isLocalFile():
            continue
        path = Path(url.toLocalFile())
        if is_rom_path(path):
            out.append(path)
    return out
