"""ROM drag-and-drop path detection."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import MagicMock

from ngpc_rom_drop import is_rom_path, rom_path_from_launch_args, rom_paths_from_local_urls
import ngpc_input


class RomDropTests(unittest.TestCase):
    def test_is_rom_path(self) -> None:
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as td:
            root = Path(td)
            rom = root / "game.ngc"
            rom.write_bytes(b"\x00")
            self.assertTrue(is_rom_path(rom))
            self.assertFalse(is_rom_path(root / "readme.txt"))

    def test_urls_filter(self) -> None:
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as td:
            rom = Path(td) / "kof.ngp"
            rom.write_bytes(b"\x00")
            good = MagicMock()
            good.isLocalFile.return_value = True
            good.toLocalFile.return_value = str(rom)
            bad = MagicMock()
            bad.isLocalFile.return_value = True
            bad.toLocalFile.return_value = str(Path(td) / "note.txt")
            paths = rom_paths_from_local_urls([good, bad])
            self.assertEqual(len(paths), 1)
            self.assertEqual(paths[0].name, "kof.ngp")

    def test_launch_args(self) -> None:
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as td:
            rom = Path(td) / "fight.ngc"
            rom.write_bytes(b"\x00")
            got = rom_path_from_launch_args(["-psn_0_123", str(rom), "junk.txt"])
            self.assertIsNotNone(got)
            assert got is not None
            self.assertEqual(got.name, "fight.ngc")
            self.assertIsNone(rom_path_from_launch_args(["--timing", "legacy"]))

    def test_mac_bundle_skips_sdl(self) -> None:
        import sys
        old = getattr(sys, "frozen", False)
        try:
            sys.frozen = True  # type: ignore[attr-defined]
            if sys.platform == "darwin":
                self.assertFalse(ngpc_input.sdl_backend_allowed())
        finally:
            if old:
                sys.frozen = True  # type: ignore[attr-defined]
            elif hasattr(sys, "frozen"):
                del sys.frozen  # type: ignore[attr-defined]


if __name__ == "__main__":
    unittest.main()
