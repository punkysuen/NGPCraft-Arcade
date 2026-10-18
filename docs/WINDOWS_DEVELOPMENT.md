# Windows — build & test

NGPCraft Arcade shares **`main`** with the macOS edition. This file covers Windows-only packaging.

## Clone

```powershell
git clone https://github.com/punkysuen/NGPCraft-Arcade.git
cd NGPCraft-Arcade
git checkout main
git pull origin main
```

## Prerequisites

- Git, **Python 3.11 or 3.12** (64-bit)
- **Visual Studio Build Tools** (Desktop C++ workload) or full Visual Studio
- **CMake** on `PATH`

## Run from source

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build cpp/build --config Release
# If MSVC placed the DLL under Release\:
copy cpp\build\Release\ngpc_core.dll cpp\build\ngpc_core.dll
python ngpc_shell.py
```

The repo may ship a prebuilt **`cpp/build/ngpc_core.dll`** (MSVC) for Windows PyInstaller; on Mac/Linux, CMake produces `ngpc_core.dylib` / `.so` locally instead.

## PyInstaller `.exe`

```powershell
pip install pyinstaller
pyinstaller --noconfirm --clean NgpCraftEmulator.spec
# Output: dist\NgpCraftEmulator.exe (+ bundled files)
```

Zip `dist\` contents for Release (e.g. `NGPCraft-Arcade-v0.5.0-Windows.zip`) and upload to [GitHub Releases](https://github.com/punkysuen/NGPCraft-Arcade/releases).

## CI

Push a tag matching `v*` to run `.github/workflows/build.yml` (Windows/Linux/macOS PyInstaller). Fork releases may still attach hand-tested zips manually.

## Gamepads & fight mode

Same as macOS: enable **Use a controller** in Settings; bind fight ABCD in Controls. XInput and SDL (pygame) are supported on Windows.

See [NGPCRAFT_ARCADE.md](NGPCRAFT_ARCADE.md) and [MAC_FIGHT_CONTROLS.md](MAC_FIGHT_CONTROLS.md).
