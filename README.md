# NGPCraft Arcade

A **Neo Geo Pocket / Color** emulator fork for **macOS and Windows**, with **MVS-style ABCD fight controls**, drag-and-drop ROM launch, and gamepad support. Based on [NgpCraft Emulator](https://github.com/Tixul/Ngpcraft_emulator) (MIT).

## Download

**[Releases](https://github.com/punkysuen/NGPCraft-Arcade/releases)** — pick the zip for your platform (e.g. `NGPCraft-Arcade-v0.5.0-Windows.zip`).  
You must supply your own legally obtained **ROM** and optional **BIOS** files.

| Platform | Notes |
|----------|--------|
| **Windows 10+** | Unzip and run `NgpCraftEmulator.exe`. Saves and data sit next to the exe. |
| **macOS 12+** | Use the embedded `.app` when provided, or build locally (below). User data: `~/Library/Application Support/NGPCraft Arcade/`. First launch of an unsigned app: **Right-click → Open**. |

## Quick start

1. Install or unzip the build for your OS.  
2. Open the app and **drag a `.ngc` / `.ngp`** (or `.zip` / `.7z`) onto the window, or choose a ROM folder in **Settings → Library**.  
3. For fighters: enable **fight mode** and **Use a controller** under **Settings → Controls**; bind **ABCD** (keyboard + pad buttons). See [Fight controls](docs/MAC_FIGHT_CONTROLS.md).

## Build from source

Details: **[docs/NGPCRAFT_ARCADE.md](docs/NGPCRAFT_ARCADE.md)**

```bash
git clone https://github.com/punkysuen/NGPCraft-Arcade.git
cd NGPCraft-Arcade
cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build cpp/build --config Release -j
pip install -r requirements.txt
python ngpc_shell.py
```

- **macOS `.app` (gamepads):** `./build_mac_embedded_app.sh`  
- **Windows `.exe`:** see [docs/WINDOWS_DEVELOPMENT.md](docs/WINDOWS_DEVELOPMENT.md)

## More documentation

| Doc | For |
|-----|-----|
| [NGPCRAFT_ARCADE.md](docs/NGPCRAFT_ARCADE.md) | Mac vs Windows paths, dev workflow |
| [MAC_FIGHT_CONTROLS.md](docs/MAC_FIGHT_CONTROLS.md) | ABCD fight input |
| [WINDOWS_DEVELOPMENT.md](docs/WINDOWS_DEVELOPMENT.md) | Windows build |
| [**UPSTREAM_README.md**](docs/UPSTREAM_README.md) | **Full original NgpCraft manual** — timing, debugging, netplay, plugins, Android/Libretro pointers, deep technical reference |

## Credits

- Emulator core: **Tixul** — [NgpCraft Emulator](https://github.com/Tixul/Ngpcraft_emulator)  
- **NGPCraft Arcade:** **Suen Kin**  
- Neo Geo Pocket is a trademark of SNK; this project is not affiliated with SNK.

License: [MIT](LICENSE)
