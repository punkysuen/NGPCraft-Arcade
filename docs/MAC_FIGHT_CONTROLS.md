# Mac NGPC 格鬥四鍵版

本專案以 [NgpCraft](https://github.com/Tixul/Ngpcraft_emulator) 的 MIT C++ 核心為基礎，並加入 **MVS 風格 ABCD 四鍵** 輸入層。

## 原理

NGPC 格鬥遊戲只有 **A / B** 兩顆面鍵，遊戲以 **按住 A 或 B 的時間** 區分輕拳、重拳、輕腳、重腳。本模擬器提供四個獨立按鍵，自動代為送出固定時長的 A/B 脈衝：

| 虛擬鍵 | 實際送到 NGPC | 時長 | 對應街機 |
|--------|----------------|------|----------|
| A | A 鍵 | 0.1 秒 | 輕拳 |
| B | B 鍵 | 0.1 秒 | 輕腳 |
| C | A 鍵 | 至少 ~0.17 秒（10 幀）；**可按住更久** | 重拳／蓄力 |
| D | B 鍵 | 至少 ~0.17 秒（10 幀）；**可按住更久** | 重腳／蓄力 |

（NGPC 沒有第三顆面鍵；D 對應 **長按 B**，非「原 D 鍵」。）

時長以 **模擬幀數** 計算（約 60 Hz）：輕攻擊 A/B 固定 3 幀。**C/D** 快按仍保證至少 **10 幀**（約 0.17 秒）才放開 A/B 線，方便連續重攻；需要蓄力超必殺時可 **一直按住 C/D**，放開才結束。常數 `HEAVY_FRAMES`（`ngpc_fight_input.py`）可依實機手感再調。

## 預設鍵位（玩家 1）

| 功能 | 鍵盤 | 手把（設定裡開啟「使用手把」） |
|------|------|--------------------------------|
| 輕拳 | J | A |
| 輕腳 | K | B |
| 重拳 | U | X |
| 重腳 | I | Y |

方向：鍵盤方向鍵／手把十字鍵或左搖桿。Option 仍用鍵盤綁定；手把 Start/Back 仍對應 Option。

格鬥四鍵開啟時，手把 **不會** 再直接把 A/B 當 NGPC 面鍵（改由上述四鍵觸發固定時長宏）。

### 自訂手把格鬥鍵（config.ini）

SDL 遊戲手把按鈕編號（Xbox 布局）：`0=A, 1=B, 2=X, 3=Y`。

```ini
[input/fight_pad/A]=0
[input/fight_pad/B]=1
[input/fight_pad/C]=2
[input/fight_pad/D]=3
```

可改成其他編號（例如肩鍵 9/10）；需重啟或重新載入設定後生效。

## Qt 無法啟動（`Could not find the Qt platform plugin "cocoa"`）

在專案 venv 內重裝 PyQt6 套件（常見於首次安裝不完整或 Python 3.14 環境）：

```bash
cd /Users/suenkin/Desktop/Cursor/ngpc
source .venv/bin/activate
pip install --force-reinstall PyQt6 PyQt6-Qt6 PyQt6-sip
python3 -c "from PyQt6.QtWidgets import QApplication; import sys; QApplication(sys.argv); print('Qt OK')"
```

最後一行應印出 `Qt OK`。也可直接執行 `./run_mac.sh`。

## 封裝成桌面 .app（雙擊啟動）

在專案目錄執行：

```bash
./build_mac_app.sh --desktop
```

會產生 `dist/NgpCraftEmulator.app`，並複製到 **桌面**。第一次開啟若 macOS 阻擋未簽名 app：**右鍵 → 打開**。

**雙擊 `.app`**（未帶 ROM）時才會跳出 **Finder 選檔視窗**；**把 ROM 拖到 `.app` 圖示**或「用此 App 開啟」會直接進遊戲，不會再彈選檔。取消選檔則進入遊戲庫。開發模式 `python3 ngpc_shell.py` 預設直接進遊戲庫；測試選檔：`NGPCRAFT_PICK_ROM=1 python3 ngpc_shell.py`。

## 使用者資料位置（macOS .app）

內嵌版 `.app` 的存檔、備份設定、縮圖快取等寫入：

`~/Library/Application Support/NGPCraft Arcade/`

（不再在桌面／`.app` 旁產生 `settings_backup.ini` 等檔案。若你曾用舊版在 `.app` 旁留下資料，首次啟動新版本會**複製**到上述資料夾。若要恢復舊行為，可在啟動前設定環境變數 `NGPCRAFT_REPO_ROOT` 指向要使用的資料夾。）

一般設定（未開可攜模式）仍由 macOS 的 `QSettings` 儲存；可攜模式的 `config.ini` 則在 Application Support 內。

## 放入 ROM 的方式

1. **Application Support 內的 `roms/`**（或開發時在專案 `roms/`）
2. **設定 → 遊戲庫** 指定資料夾
3. **拖放**：把 **`.ngc` / `.ngp`**（或 `.zip` / `.7z` 壓縮包）拖到模擬器視窗（遊戲庫或遊戲中皆可），會直接開始該 ROM  
   （副檔名須為 `.ngc` / `.ngp`，不是 `.npc`）

## 建置（macOS 開發）

```bash
cd cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
# 產出：cpp/build/ngpc_core.dylib

pip install -r requirements.txt
python ngpc_shell.py
```

可在 **設定 → 控制** 中開關「格鬥四鍵（ABCD 時序）」。

## 實作位置

- `ngpc_fight_input.py` — 脈衝排程
- `ngpc_settings.py` — `input/fight_mode`、預設鍵位
- `ngpc_shell.py` — 每幀合併至 0x00B0 手把位元組
