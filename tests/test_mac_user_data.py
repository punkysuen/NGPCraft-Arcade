"""macOS .app user-data directory (Application Support)."""

from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest.mock import patch

import ngpc_app_info as ai


class MacUserDataTests(unittest.TestCase):
    def test_app_support_when_embedded(self) -> None:
        old_mac = os.environ.get(ai.MAC_APP_ENV)
        old_repo = os.environ.get(ai.REPO_ROOT_ENV)
        old_user = os.environ.get(ai.USER_DATA_ENV)
        try:
            os.environ.pop(ai.REPO_ROOT_ENV, None)
            os.environ[ai.MAC_APP_ENV] = "1"
            with patch.object(ai.sys, "platform", "darwin"):
                self.assertTrue(ai.should_use_mac_app_support())
        finally:
            for key, val in ((ai.MAC_APP_ENV, old_mac), (ai.REPO_ROOT_ENV, old_repo),
                             (ai.USER_DATA_ENV, old_user)):
                if val is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = val

    def test_repo_root_env_keeps_legacy_layout(self) -> None:
        old = os.environ.get(ai.REPO_ROOT_ENV)
        try:
            os.environ[ai.REPO_ROOT_ENV] = "/tmp/legacy-ngpc"
            os.environ[ai.MAC_APP_ENV] = "1"
            with patch.object(ai.sys, "platform", "darwin"):
                self.assertFalse(ai.should_use_mac_app_support())
                self.assertEqual(ai.writable_data_root(), Path("/tmp/legacy-ngpc"))
        finally:
            if old is None:
                os.environ.pop(ai.REPO_ROOT_ENV, None)
            else:
                os.environ[ai.REPO_ROOT_ENV] = old
            os.environ.pop(ai.MAC_APP_ENV, None)


if __name__ == "__main__":
    unittest.main()
