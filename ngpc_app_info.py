"""Branding and credits for this macOS / NGPCraft Arcade edition.

Edit FORK_DEVELOPER with your name or GitHub handle before publishing.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Public product name (window title, About).
APP_NAME = "NGPCraft Arcade"
APP_VERSION = "0.5.0"

# Must match LSMinimumSystemVersion in build_mac_embedded_app.sh Info.plist.
MACOS_MIN_VERSION = "12.0"
MACOS_MIN_NAME = "Monterey"

# Upstream emulator this fork is based on (MIT — see LICENSE).
UPSTREAM_NAME = "NgpCraft Emulator"
UPSTREAM_AUTHOR = "Tixul"
UPSTREAM_URL = "https://github.com/Tixul/Ngpcraft_emulator"
UPSTREAM_LICENSE = "MIT License"

# Shown in About; should match the copyright holder in LICENSE (legal/GitHub name).
FORK_DEVELOPER = "Suen Kin"
FORK_COPYRIGHT_HOLDER = "Suen Kin"
FORK_TAGLINE = (
    "macOS & Windows edition with MVS-style ABCD fight controls, "
    "drag-and-drop ROM, and gamepad support."
)

# Play counts / favourites stay in RAM only — no library.json beside the .app.
PERSIST_LIBRARY_JSON = False

# Set by Contents/MacOS launcher (embedded-Python .app, route 1 — not PyInstaller).
MAC_APP_ENV = "NGPCRAFT_MAC_APP"
APP_ROOT_ENV = "NGPCRAFT_APP_ROOT"
REPO_ROOT_ENV = "NGPCRAFT_REPO_ROOT"
# Override Application Support (tests); normally derived automatically on macOS .app.
USER_DATA_ENV = "NGPCRAFT_USER_DATA"


def is_mac_embedded_app() -> bool:
    """True when running inside the embedded-Python .app (pygame/SDL allowed)."""
    return os.environ.get(MAC_APP_ENV, "").strip().lower() in ("1", "true", "yes")


def mac_app_root() -> Path | None:
    raw = os.environ.get(APP_ROOT_ENV, "").strip()
    return Path(raw) if raw else None


def mac_repo_root() -> Path | None:
    raw = os.environ.get(REPO_ROOT_ENV, "").strip()
    return Path(raw) if raw else None


def is_packaged_app() -> bool:
    """PyInstaller frozen build or embedded macOS .app."""
    return bool(getattr(sys, "frozen", False)) or is_mac_embedded_app()


def mac_install_dir() -> Path | None:
    """Folder that contains the .app bundle (e.g. Desktop), when embedded."""
    root = mac_app_root()
    if root is None:
        return None
    # …/NGPCraft Arcade.app/Contents/Resources/app
    return root.resolve().parent.parent.parent.parent


def should_use_mac_app_support() -> bool:
    """Store saves/backups under ~/Library/Application Support/… on macOS builds."""
    if sys.platform != "darwin" or not is_packaged_app():
        return False
    # Legacy: keep data beside the .app when explicitly requested.
    if os.environ.get(REPO_ROOT_ENV, "").strip():
        return False
    return True


def user_data_dir(*, create: bool = True) -> Path:
    """Per-user writable root on macOS (.app builds)."""
    override = os.environ.get(USER_DATA_ENV, "").strip()
    if override:
        path = Path(override)
    else:
        path = Path.home() / "Library" / "Application Support" / APP_NAME
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def writable_data_root() -> Path:
    """Saves, thumbnails, settings backups, portable config.ini (when enabled)."""
    if should_use_mac_app_support():
        return user_data_dir()
    repo = os.environ.get(REPO_ROOT_ENV, "").strip()
    if repo:
        return Path(repo)
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable).resolve()
        if sys.platform == "darwin" and exe.parent.name == "MacOS":
            return exe.parent.parent.parent.parent
        return exe.parent
    return Path(__file__).resolve().parent


_LEGACY_MIGRATE_NAMES = (
    "settings_backup.ini",
    "settings_backup.prev.ini",
    "config.ini",
    "library.json",
)
_LEGACY_MIGRATE_DIRS = (
    "saves",
    "thumbnails",
    "savestates",
    "screenshots",
    "crashes",
    "watches",
    "covers",
    "roms",
)


def migrate_legacy_bundle_data() -> None:
    """One-time move from data left next to the .app (old builds) into App Support."""
    if not should_use_mac_app_support():
        return
    legacy = mac_install_dir()
    if legacy is None or not legacy.is_dir():
        return
    dest = user_data_dir()
    flag = dest / ".migrated_from_install_dir"
    if flag.is_file():
        return

    def _copy_file(name: str) -> None:
        src = legacy / name
        if not src.is_file():
            return
        target = dest / name
        if target.exists():
            return
        shutil.copy2(src, target)

    def _copy_dir(name: str) -> None:
        src = legacy / name
        if not src.is_dir():
            return
        target = dest / name
        if target.exists():
            return
        shutil.copytree(src, target)

    for name in _LEGACY_MIGRATE_NAMES:
        _copy_file(name)
    for name in _LEGACY_MIGRATE_DIRS:
        _copy_dir(name)
    try:
        flag.write_text(str(legacy.resolve()), encoding="utf-8")
    except OSError:
        pass


def about_placeholders() -> dict[str, str]:
    """Keyword args for lang/about_html."""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "upstream": UPSTREAM_NAME,
        "author": UPSTREAM_AUTHOR,
        "license": UPSTREAM_LICENSE,
        "url": UPSTREAM_URL,
        "developer": FORK_DEVELOPER,
        "copyright_holder": FORK_COPYRIGHT_HOLDER,
        "tagline": FORK_TAGLINE,
        "macos_min": MACOS_MIN_VERSION,
        "macos_name": MACOS_MIN_NAME,
    }


def about_html(lang: str) -> str:
    import ngpc_settings as cfg
    code = lang.lower().replace("-", "_")
    return cfg.tr(code, "about_html").format(**about_placeholders())
