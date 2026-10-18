# Windows edition — development branch

This document is for the **`windows-edition`** branch: packaging and testing **NGPCraft Arcade** on Windows while macOS work continues on `main`.

## Clone on your Windows PC

```powershell
git clone https://github.com/punkysuen/NGPCraft-Arcade.git
cd NGPCraft-Arcade
git fetch origin
git checkout windows-edition
```

Open this folder in **Cursor** (separate workspace from your Mac — chat history stays on each machine; use Git and this file for shared context).

## Prerequisites (Windows)

- [Git for Windows](https://gitforwindows.org/)
- **Python 3.11 or 3.12** (64-bit) — matches GitHub Actions
- **Visual Studio Build Tools** or VS with “Desktop development with C++” (for `ngpc_core.dll`)
- **CMake** on `PATH`

## Quick run from source

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build cpp/build --config Release
python ngpc_shell.py
```

Gamepads: **SDL (pygame)** and **XInput** — see `ngpc_input.py`. Fight ABCD behaviour matches Mac (see `docs/MAC_FIGHT_CONTROLS.md` / `ngpc_fight_input.py`).

## Packaged `.exe` (PyInstaller)

Upstream uses `NgpCraftEmulator.spec` and CI (`.github/workflows/build.yml`). Windows-specific branding, paths, and Release assets for NGPCraft Arcade will be tracked on this branch.

```powershell
pip install pyinstaller
pyinstaller --noconfirm --clean NgpCraftEmulator.spec
```

Or trigger **Actions → build → Run workflow** on GitHub and download the Windows artifact from the run (no tag required).

## Sync with Mac

```powershell
git pull origin windows-edition
```

When Windows work is ready to ship, merge `windows-edition` → `main` via pull request on GitHub.

## Goals (initial checklist)

- [ ] Confirm fight mode + C/D hold + pad bindings on Windows
- [ ] PyInstaller build runs; data lives beside `.exe` (not Mac Application Support)
- [ ] CI / Release asset name: **NGPCraft Arcade** Windows zip
- [ ] English release notes for first Windows tag
