# NGPCraft Arcade v0.5.0 — macOS & Windows

**NGPCraft Arcade** is a fork of [NgpCraft Emulator](https://github.com/Tixul/Ngpcraft_emulator) (MIT) for **macOS and Windows**, focused on Neo Geo Pocket / Color fighting games with MVS-style four-button timing, drag-and-drop ROM launch, and gamepad support.

**Downloads (Assets below):**

- **Windows 10+:** [`NGPCraft-Arcade-v0.5.0-Windows.zip`](https://github.com/punkysuen/NGPCraft-Arcade/releases/download/v0.5.0/NGPCraft-Arcade-v0.5.0-Windows.zip)
- **macOS 12+:** [`NGPCraft-Arcade-v0.5.0-macOS.zip`](https://github.com/punkysuen/NGPCraft-Arcade/releases/download/v0.5.0/NGPCraft-Arcade-v0.5.0-macOS.zip)

Or build macOS from source with `./build_mac_embedded_app.sh` (see [Build from source](#build-from-source)).

## Requirements

- **Windows 10 or later (64-bit)**
- **macOS 12.0 (Monterey) or later**
- Your own legally obtained **ROM** and optional **BIOS** files (none are included)
- First launch of an unsigned build: **Right-click the app → Open**, or allow in **System Settings → Privacy & Security**

## Download & install

1. Download **`NGPCraft-Arcade-v0.5.0-macOS.zip`** from Assets (link above), or build from source (see [Build from source](#build-from-source)).
2. Unzip and move **`NGPCraft Arcade.app`** to Applications or Desktop.
3. Open a game:
   - **Drag** a `.ngc` / `.ngp` (or `.zip` / `.7z` archive) onto the app icon or window, or
   - **Double-click** the app and use the file picker, or
   - Set a ROM folder under **Settings → Library**.

### Windows

1. Download **`NGPCraft-Arcade-v0.5.0-Windows.zip`** and unzip.
2. Run **`NgpCraftEmulator.exe`** (no Python install required).
3. Place your ROMs (and optional BIOS) beside the `.exe`; saves and data stay in that folder.

## What’s new in v0.5.0

### Mac app & data

- **Embedded Python `.app`** (`build_mac_embedded_app.sh`) with **pygame / SDL gamepads** (avoid the PyInstaller Mac build for controllers).
- User data (saves, backups, thumbnails, portable `config.ini`) under  
  **`~/Library/Application Support/NGPCraft Arcade/`** — not beside the `.app` on Desktop.
- One-time **migration** of older files from the folder next to the `.app` when upgrading.

### Fight controls (ABCD)

- **A / B** — short light punch / kick pulses (3 frames).
- **C / D** — **real hold**: hold for charge moves (e.g. charged supers); **quick tap** still guarantees at least **10 frames** (~167 ms at 60 Hz) so heavies register without blocking fast heavy chains.
- **Settings → Controls**: bind keyboard and **gamepad button indices** for fight ABCD; console picture map is **keyboard only**.
- Enable **Use a controller** and pick controller index 1–4 if needed.

### UI & launch

- Left rail **About** (credits, version, macOS minimum, SNK disclaimer).
- Removed redundant product title from the top of the sidebar.
- **Drag ROM onto the app** no longer shows the file picker when a ROM is already being opened.

## Default keys (Setting 1)

| Fight | Keyboard | Gamepad (typical Xbox layout) |
|-------|----------|-------------------------------|
| Light punch | J | Button 0 (A) |
| Light kick | K | Button 1 (B) |
| Heavy punch | U | Button 2 (X) — hold allowed |
| Heavy kick | I | Button 3 (Y) — hold allowed |

Directions: keyboard arrows or D-pad / left stick.

## Build from source

```bash
git clone https://github.com/punkysuen/NGPCraft-Arcade.git
cd NGPCraft-Arcade
git checkout v0.5.0

# Native core
cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build cpp/build --config Release -j

# Embedded Mac .app (gamepads enabled)
./build_mac_embedded_app.sh
# Output: dist/NGPCraft Arcade.app
```

See also [docs/MAC_FIGHT_CONTROLS.md](MAC_FIGHT_CONTROLS.md) for fight input details.

## Credits & license

- Emulator core: **Tixul** — [NgpCraft Emulator](https://github.com/Tixul/Ngpcraft_emulator) (MIT)
- **NGPCraft Arcade:** **Suen Kin**
- Neo Geo Pocket is a trademark of SNK; this project is not affiliated with SNK.

Full license: [LICENSE](https://github.com/punkysuen/NGPCraft-Arcade/blob/main/LICENSE)
