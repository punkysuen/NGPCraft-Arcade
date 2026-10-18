"""PyInstaller runtime hook: Qt6 platform plugins inside the frozen bundle."""
import os
import sys


def _configure_qt() -> None:
    if not getattr(sys, "frozen", False):
        return
    base = getattr(sys, "_MEIPASS", None)
    if not base:
        return
    plugins = os.path.join(base, "PyQt6", "Qt6", "plugins")
    platforms = os.path.join(plugins, "platforms")
    if os.path.isdir(platforms):
        os.environ["QT_PLUGIN_PATH"] = plugins
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms
    lib = os.path.join(base, "PyQt6", "Qt6", "lib")
    if os.path.isdir(lib):
        prev = os.environ.get("DYLD_FRAMEWORK_PATH", "")
        os.environ["DYLD_FRAMEWORK_PATH"] = (
            lib if not prev else f"{lib}{os.pathsep}{prev}"
        )


_configure_qt()
