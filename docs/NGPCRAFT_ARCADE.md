# NGPCraft Arcade — macOS & Windows

Single codebase, two desktop builds. Based on [NgpCraft Emulator](https://github.com/Tixul/Ngpcraft_emulator) (MIT).

| Platform | Download | Build | User data |
|----------|----------|-------|-----------|
| **macOS 12+** | [Releases](https://github.com/punkysuen/NGPCraft-Arcade/releases) (embedded `.app` when attached) | `./build_mac_embedded_app.sh` | `~/Library/Application Support/NGPCraft Arcade/` |
| **Windows** | [Releases](https://github.com/punkysuen/NGPCraft-Arcade/releases) — `NGPCraft-Arcade-v*-Windows.zip` | PyInstaller — see [WINDOWS_DEVELOPMENT.md](WINDOWS_DEVELOPMENT.md) | Beside `NgpCraftEmulator.exe` (portable layout) |

## Shared features (both platforms)

- MVS-style **fight ABCD** input (`ngpc_fight_input.py`): light A/B taps; **C/D** hold with **10-frame** minimum heavy length and longer charge support.
- **Settings → Controls**: keyboard + gamepad fight bindings; SDL / XInput gamepads (`ngpc_input.py`).
- Drag-and-drop ROM, library UI, native C++ core (`cpp/`).
- Version string: `ngpc_app_info.APP_VERSION` (About dialog).

## Development

- **Primary branch:** `main` — all Mac and Windows work lands here.
- **Do not use** a separate product branch; `windows-edition` was merged into `main`.
- Mac: edit in Cursor on macOS, push `main`.
- Windows `.exe` for releases: build on Windows (or CI — see `.github/workflows/build.yml`) and attach zip to GitHub Releases; commit source/spec changes to `main`.

## Docs

- [MAC_FIGHT_CONTROLS.md](MAC_FIGHT_CONTROLS.md) — fight input and Mac `.app` notes  
- [WINDOWS_DEVELOPMENT.md](WINDOWS_DEVELOPMENT.md) — Windows venv, CMake, PyInstaller  
- [RELEASE_v0.5.0.md](RELEASE_v0.5.0.md) — v0.5.0 release notes (English)

## Legal

Neo Geo Pocket is a trademark of SNK; this project is not affiliated with SNK. No ROMs or BIOS are distributed.
