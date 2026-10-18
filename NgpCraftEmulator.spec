# -*- mode: python ; coding: utf-8 -*-
#
# One spec, three platforms. PyInstaller never cross-compiles: this file runs ON
# each target OS (locally or in CI) and branches on sys.platform so the same
# command produces a Windows .exe, a Linux binary, or a macOS .app -- see
# .github/workflows/build.yml.

import sys

from PyInstaller.utils.hooks import collect_all

# The native core keeps the same stem on every OS (CMake strips the `lib` prefix);
# only the extension changes. This MUST match core.native._DLL_NAME.
if sys.platform == "win32":
    _CORE = "ngpc_core.dll"
    _ICON = "assets/icone_ngpcraft.ico"
    _EXE_NAME = "NgpCraftEmulator"
    _APP_BUNDLE = None
    _BUNDLE_ID = "com.ngpcraft.emulator"
elif sys.platform == "darwin":
    _CORE = "ngpc_core.dylib"
    import os
    _ICON = "assets/icone_ngpcraft.icns" if os.path.exists(
        "assets/icone_ngpcraft.icns") else "assets/icone_ngpcraft.ico"
    _EXE_NAME = "NGPCraftArcade"
    _APP_BUNDLE = "NGPCraft Arcade.app"
    _BUNDLE_ID = "com.ngpcraft.arcade"
    _DOC_TYPES = [
        {
            "CFBundleTypeName": "Neo Geo Pocket ROM",
            "CFBundleTypeRole": "Viewer",
            "LSHandlerRank": "Owner",
            "CFBundleTypeExtensions": ["ngc", "ngp", "zip", "7z"],
        },
    ]
else:
    _CORE = "ngpc_core.so"
    _ICON = None
    _EXE_NAME = "NgpCraftEmulator"
    _APP_BUNDLE = None
    _BUNDLE_ID = "com.ngpcraft.emulator"

_UPX = sys.platform == "win32"

_datas = [
    (f"cpp/build/{_CORE}", "cpp/build"),
    ("hle_bios/bios_hle.bin", "hle_bios"),
    ("assets/icone_ngpcraft.ico", "assets"),
    ("assets/ngpc_console.png", "assets"),
    ("lang", "lang"),
]
_binaries = []
_hidden = []
_runtime_hooks = []

# PyQt6 needs plugins + Qt frameworks in the bundle (macOS cocoa crash without this).
_pyqt_datas, _pyqt_binaries, _pyqt_hidden = collect_all("PyQt6")
_datas += _pyqt_datas
_binaries += _pyqt_binaries
_hidden += _pyqt_hidden

if sys.platform == "darwin":
    _runtime_hooks.append("pyi_rth_qt6_plugins.py")
else:
    _DOC_TYPES = None

# macOS .app: do not bundle pygame/SDL (libSDL2 aborts at load time inside the bundle).
_excludes = ["pygame"] if sys.platform == "darwin" else []

a = Analysis(
    ["ngpc_shell.py"],
    pathex=[],
    binaries=_binaries,
    datas=_datas,
    hiddenimports=_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=_runtime_hooks,
    excludes=_excludes,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

_common_exe_kw = dict(
    name=_EXE_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=_UPX,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[_ICON] if _ICON else None,
)

if sys.platform == "darwin" and _APP_BUNDLE:
    # Onedir .app: avoids ~10s onefile extract on every launch.
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        argv_emulation=True,
        **_common_exe_kw,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        name=_EXE_NAME,
    )
    _plist = {
        "CFBundleName": "NGPCraft Arcade",
        "CFBundleDisplayName": "NGPCraft Arcade",
        "CFBundleShortVersionString": "0.5.0",
        "NSHighResolutionCapable": True,
    }
    if _DOC_TYPES:
        _plist["CFBundleDocumentTypes"] = _DOC_TYPES
    app = BUNDLE(
        coll,
        name=_APP_BUNDLE,
        icon=_ICON,
        bundle_identifier=_BUNDLE_ID,
        info_plist=_plist,
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        argv_emulation=False,
        **_common_exe_kw,
    )
