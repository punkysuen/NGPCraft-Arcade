#!/usr/bin/env bash
# Build NGPCraft Arcade.app with embedded Python (route 1: pygame/SDL works in the bundle).
#
# Usage:
#   ./build_mac_embedded_app.sh              -> dist/NGPCraft Arcade.app
#   ./build_mac_embedded_app.sh --desktop    -> also copy to ~/Desktop/
#
# Requires: cmake, Python 3.12 (python.org or Homebrew) with Python.framework.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

COPY_DESKTOP=0
for arg in "$@"; do
  case "$arg" in
    --desktop) COPY_DESKTOP=1 ;;
  esac
done

APP_NAME="NGPCraft Arcade"
EXE_NAME="NGPCraftArcade"
DIST_APP="$ROOT/dist/$APP_NAME.app"
CONTENTS="$DIST_APP/Contents"
MACOS="$CONTENTS/MacOS"
FRAMEWORKS="$CONTENTS/Frameworks"
RES="$CONTENTS/Resources"
APP="$RES/app"
SITE="$APP/site-packages"
BUNDLE_ID="com.ngpcraft.arcade"

PY=""
for candidate in python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 11) else 1)' 2>/dev/null; then
      PY="$candidate"
      break
    fi
  fi
done
if [[ -z "$PY" ]]; then
  echo "Need Python 3.11+ (brew install python@3.12 recommended)."
  exit 1
fi
echo "Using $PY ($("$PY" --version))"

# Locate Python.framework for embedding (Homebrew or python.org layout).
BASE="$("$PY" -c 'import sys; print(sys.base_prefix)')"
FW_SRC=""
if [[ -d "$BASE/Python.framework" ]]; then
  FW_SRC="$BASE/Python.framework"
elif [[ -d "$(dirname "$(dirname "$BASE")")" ]] && [[ "$(basename "$(dirname "$BASE")")" == "Versions" ]]; then
  FW_SRC="$(cd "$(dirname "$(dirname "$BASE")")" && pwd)"
elif [[ -d "/Library/Frameworks/Python.framework" ]]; then
  FW_SRC="/Library/Frameworks/Python.framework"
else
  echo "Could not find Python.framework for embedding (install python.org or Homebrew python)."
  exit 1
fi
PY_VER="$("$PY" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
FW_PY="$FRAMEWORKS/Python.framework/Versions/$PY_VER/bin/python$PY_VER"

echo "==> Building native core…"
cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build cpp/build --config Release -j

echo "==> App icon…"
_gen_icns() {
  local icopy
  if [[ -x "$ROOT/.venv/bin/python" ]] && "$ROOT/.venv/bin/python" -c "import PIL" 2>/dev/null; then
    icopy="$ROOT/.venv/bin/python"
  elif "$PY" -c "import PIL" 2>/dev/null; then
    icopy="$PY"
  elif [[ -f "$ROOT/assets/icone_ngpcraft.icns" ]]; then
    echo "Pillow not installed on $PY; reusing assets/icone_ngpcraft.icns"
    return 0
  else
    PIP_BREAK_SYSTEM_PACKAGES=1 "$PY" -m pip install -q Pillow
    icopy="$PY"
  fi
  "$icopy" "$ROOT/tools/gen_mac_icns.py"
}
_gen_icns

echo "==> Assembling .app bundle…"
rm -rf "$DIST_APP"
mkdir -p "$MACOS" "$FRAMEWORKS" "$APP/cpp/build" "$SITE"

echo "==> Embedding Python.framework…"
ditto "$FW_SRC" "$FRAMEWORKS/Python.framework"
chmod -R u+w "$FRAMEWORKS/Python.framework" 2>/dev/null || true

echo "==> Installing Python dependencies into bundle…"
"$FW_PY" -m ensurepip --upgrade 2>/dev/null || true
export PIP_BREAK_SYSTEM_PACKAGES=1
export PIP_DISABLE_PIP_VERSION_CHECK=1
"$FW_PY" -m pip install -q -U pip
"$FW_PY" -m pip install -q -r requirements.txt --target "$SITE" --only-binary=:all: 2>/dev/null \
  || "$FW_PY" -m pip install -q -r requirements.txt --target "$SITE"
unset PIP_BREAK_SYSTEM_PACKAGES

echo "==> Copying application code…"
rsync -a \
  --exclude '.git' --exclude '.venv' --exclude 'dist' --exclude 'build' \
  --exclude 'tests' --exclude 'cpp/build' --exclude '__pycache__' \
  --exclude '*.pyc' --exclude '.DS_Store' \
  core hle_bios lang assets \
  ngpc_*.py \
  "$APP/"
install -m 644 cpp/build/ngpc_core.dylib "$APP/cpp/build/"
install -m 644 "$ROOT/assets/icone_ngpcraft.icns" "$RES/icone_ngpcraft.icns"

cat > "$MACOS/$EXE_NAME" <<'LAUNCHER'
#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../Resources/app" && pwd)"
FW_VER="$(ls "$HERE/../Frameworks/Python.framework/Versions" | grep -E '^[0-9]+\.[0-9]+$' | head -1)"
FW="$HERE/../Frameworks/Python.framework/Versions/$FW_VER"
PY="$FW/bin/python${FW_VER}"
[[ -x "$PY" ]] || PY="$FW/bin/python3"
# Writable data (saves, backups, …) goes to ~/Library/Application Support/NGPCraft Arcade/
export NGPCRAFT_MAC_APP=1
export NGPCRAFT_APP_ROOT="$ROOT"
export PYTHONHOME="$FW"
export PYTHONPATH="$ROOT:$ROOT/site-packages${PYTHONPATH:+:$PYTHONPATH}"
export PYGAME_HIDE_SUPPORT_PROMPT=1
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-dummy}"
export SDL_AUDIODRIVER="${SDL_AUDIODRIVER:-dummy}"
cd "$ROOT"
if [[ $# -eq 0 ]] && [[ -n "${LAUNCHER_OPEN_FILE:-}" ]]; then
  set -- "$LAUNCHER_OPEN_FILE"
fi
exec "$PY" "$ROOT/ngpc_shell.py" "$@"
LAUNCHER
chmod +x "$MACOS/$EXE_NAME"

/usr/libexec/PlistBuddy -c "Clear dict" "$CONTENTS/Info.plist" 2>/dev/null || true
cat > "$CONTENTS/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleDevelopmentRegion</key><string>en</string>
  <key>CFBundleExecutable</key><string>$EXE_NAME</string>
  <key>CFBundleIconFile</key><string>icone_ngpcraft</string>
  <key>CFBundleIdentifier</key><string>$BUNDLE_ID</string>
  <key>CFBundleName</key><string>$APP_NAME</string>
  <key>CFBundleDisplayName</key><string>$APP_NAME</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleShortVersionString</key><string>0.5.0</string>
  <key>CFBundleVersion</key><string>0.5.0</string>
  <key>LSMinimumSystemVersion</key><string>12.0</string>
  <key>NSHighResolutionCapable</key><true/>
  <key>CFBundleDocumentTypes</key>
  <array>
    <dict>
      <key>CFBundleTypeName</key><string>Neo Geo Pocket ROM</string>
      <key>CFBundleTypeRole</key><string>Viewer</string>
      <key>LSHandlerRank</key><string>Owner</string>
      <key>CFBundleTypeExtensions</key>
      <array><string>ngc</string><string>ngp</string><string>zip</string><string>7z</string></array>
    </dict>
  </array>
</dict>
</plist>
PLIST

xattr -cr "$DIST_APP" 2>/dev/null || true

echo ""
echo "Built (embedded Python): $DIST_APP"
echo "Drag ROM onto the app or window; pygame gamepads enabled in this build."

if [[ "$COPY_DESKTOP" -eq 1 ]]; then
  rm -rf "$HOME/Desktop/$APP_NAME.app" 2>/dev/null || true
  cp -R "$DIST_APP" "$HOME/Desktop/"
  xattr -cr "$HOME/Desktop/$APP_NAME.app" 2>/dev/null || true
  echo "Copied to \"$HOME/Desktop/$APP_NAME.app\""
fi
