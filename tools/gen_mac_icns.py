#!/usr/bin/env python3
"""Build assets/icone_ngpcraft.icns from assets/icone_ngpcraft.ico (macOS .app icon)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ICO = ROOT / "assets" / "icone_ngpcraft.ico"
ICONSET = ROOT / "assets" / "icone_ngpcraft.iconset"
OUT = ROOT / "assets" / "icone_ngpcraft.icns"

# Apple iconset naming (see `man iconutil`).
_SLOTS = (
    ("icon_16x16.png", 16),
    ("icon_16x16@2x.png", 32),
    ("icon_32x32.png", 32),
    ("icon_32x32@2x.png", 64),
    ("icon_128x128.png", 128),
    ("icon_128x128@2x.png", 256),
    ("icon_256x256.png", 256),
    ("icon_256x256@2x.png", 512),
    ("icon_512x512.png", 512),
    ("icon_512x512@2x.png", 1024),
)


def main() -> int:
    if not ICO.is_file():
        print(f"Missing {ICO}", file=sys.stderr)
        return 1
    img = Image.open(ICO)
    if ICONSET.exists():
        for p in ICONSET.iterdir():
            p.unlink()
    else:
        ICONSET.mkdir(parents=True)
    for name, size in _SLOTS:
        frame = img.copy()
        frame.thumbnail((size, size), Image.Resampling.LANCZOS)
        if frame.mode != "RGBA":
            frame = frame.convert("RGBA")
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ox = (size - frame.width) // 2
        oy = (size - frame.height) // 2
        canvas.paste(frame, (ox, oy))
        canvas.save(ICONSET / name, format="PNG")
    if subprocess.run(
        ["iconutil", "-c", "icns", str(ICONSET), "-o", str(OUT)],
        check=False,
    ).returncode != 0:
        print("iconutil failed (need macOS)", file=sys.stderr)
        return 1
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
