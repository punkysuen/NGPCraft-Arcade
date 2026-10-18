#!/usr/bin/env bash
# Build NGPCraft Arcade.app for macOS (double-clickable in Finder).
#
# Usage:
#   ./build_mac_app.sh              -> dist/NGPCraft Arcade.app
#   ./build_mac_app.sh --desktop    -> also copy to ~/Desktop/
#
# First launch: unsigned apps may need Right-click -> Open (Gatekeeper).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

COPY_DESKTOP=0
for arg in "$@"; do
  case "$arg" in
    --desktop) COPY_DESKTOP=1 ;;
  esac
done

if ! command -v cmake >/dev/null 2>&1; then
  echo "cmake not found. Install: brew install cmake"
  exit 1
fi

# PyInstaller + PyQt6: prefer 3.11/3.12 (matches CI; 3.14 has been fragile in bundles).
PY=""
for candidate in python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PY="$candidate"
    break
  fi
done
if [[ -z "$PY" ]]; then
  echo "No python3 found. Install: brew install python@3.12"
  exit 1
fi
echo "Using $PY ($("$PY" --version))"

if [[ ! -d .venv ]] || ! .venv/bin/python -c "import sys; exit(0 if sys.version_info[:2] in ((3,11),(3,12)) else 1)" 2>/dev/null; then
  rm -rf .venv
  "$PY" -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
pip install -q -U pip
pip install -q -r requirements.txt pyinstaller

echo "==> Building native core…"
cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build cpp/build --config Release -j

echo "==> App icon (.icns from NgpCraft .ico)…"
python tools/gen_mac_icns.py

echo "==> Packaging .app (PyInstaller + Qt plugins)…"
pyinstaller --noconfirm --clean NgpCraftEmulator.spec

APP="dist/NGPCraft Arcade.app"
if [[ ! -d "$APP" ]]; then
  echo "Expected \"$APP\" was not created."
  ls -la dist 2>/dev/null || true
  exit 1
fi

# Finder metadata breaks ad-hoc codesign and can confuse Icon Services.
xattr -cr "$APP" 2>/dev/null || true

echo ""
echo "Built: $ROOT/$APP"
echo "Place a roms/ folder next to the .app on Desktop, or pick a ROM when the app opens."
echo "Double-click: ROM picker on first launch; drag ROM onto the app icon or window."

if [[ "$COPY_DESKTOP" -eq 1 ]]; then
  rm -rf "$HOME/Desktop/NGPCraft Arcade.app" "$HOME/Desktop/NgpCraftEmulator.app" 2>/dev/null || true
  cp -R "$APP" "$HOME/Desktop/"
  echo "Copied to \"$HOME/Desktop/NGPCraft Arcade.app\""
fi
