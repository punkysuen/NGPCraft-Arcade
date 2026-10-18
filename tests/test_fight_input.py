"""Timed fight-button pulses for NGPC fighters."""

from __future__ import annotations

import unittest

from ngpc_fight_input import (
    HEAVY_FRAMES,
    LIGHT_FRAMES,
    FightInputMixer,
    strip_face_buttons,
)
from ngpc_input import A, B


class FightInputTests(unittest.TestCase):
    def test_light_pulses(self) -> None:
        mix = FightInputMixer()
        mix.trigger("a", frame=10)
        for f in range(10, 10 + LIGHT_FRAMES):
            self.assertEqual(mix.active_mask(f), A, f"frame {f}")
        self.assertEqual(mix.active_mask(10 + LIGHT_FRAMES), 0)

    def test_heavy_short_tap_minimum_frames(self) -> None:
        mix = FightInputMixer()
        mix.press_heavy("c", frame=100)
        mix.release_heavy("c", frame=102)
        for f in range(100, 100 + HEAVY_FRAMES):
            self.assertEqual(mix.active_mask(f), A, f"frame {f}")
        self.assertEqual(mix.active_mask(100 + HEAVY_FRAMES), 0)

    def test_heavy_hold_until_release(self) -> None:
        mix = FightInputMixer()
        mix.press_heavy("c", frame=10)
        for f in range(10, 50):
            self.assertEqual(mix.active_mask(f), A, f"frame {f}")
        mix.release_heavy("c", frame=50)
        self.assertEqual(mix.active_mask(50), 0)

    def test_heavy_long_hold_no_extra_tail(self) -> None:
        mix = FightInputMixer()
        mix.press_heavy("d", frame=0)
        for f in range(0, HEAVY_FRAMES + 10):
            self.assertEqual(mix.active_mask(f), B)
        mix.release_heavy("d", frame=HEAVY_FRAMES + 10)
        self.assertEqual(mix.active_mask(HEAVY_FRAMES + 10), 0)
        self.assertEqual(mix.active_mask(HEAVY_FRAMES + 11), 0)

    def test_trigger_compat_heavy_minimum(self) -> None:
        """Legacy trigger(c) at one frame still yields HEAVY_FRAMES of A."""
        mix = FightInputMixer()
        mix.trigger("c", frame=100)
        for f in range(100, 100 + HEAVY_FRAMES):
            self.assertEqual(mix.active_mask(f), A)
        self.assertEqual(mix.active_mask(100 + HEAVY_FRAMES), 0)

    def test_b_and_d_use_b_line(self) -> None:
        mix = FightInputMixer()
        mix.trigger("b", frame=0)
        self.assertEqual(mix.active_mask(0), B)
        mix.press_heavy("d", frame=50)
        mix.release_heavy("d", frame=51)
        self.assertEqual(mix.active_mask(50 + HEAVY_FRAMES - 1), B)
        self.assertEqual(mix.active_mask(50 + HEAVY_FRAMES), 0)

    def test_overlapping_same_line(self) -> None:
        mix = FightInputMixer()
        mix.trigger("a", frame=0)
        mix.trigger("a", frame=1)
        self.assertEqual(mix.active_mask(LIGHT_FRAMES), A)

    def test_strip_face_buttons(self) -> None:
        self.assertEqual(strip_face_buttons(A | B | 0x01), 0x01)

    def test_merge_keeps_directions(self) -> None:
        mix = FightInputMixer()
        mix.trigger("a", frame=0)
        self.assertEqual(mix.merge_joypad(0x02, 1), 0x02 | A)

    def test_pad_edge_triggers_once(self) -> None:
        from ngpc_input import poll_fight_pad_edges

        class _FakePad:
            def __init__(self, buttons):
                self._b = frozenset(buttons)

            def fight_button_mask(self):
                return self._b

        pad = _FakePad({0})
        fired, prev = poll_fight_pad_edges(pad, frozenset(), {0: "a", 1: "b"})
        self.assertEqual(fired, ["a"])
        fired, prev = poll_fight_pad_edges(pad, prev, {0: "a"})
        self.assertEqual(fired, [])
        pad2 = _FakePad({0, 1})
        fired, _ = poll_fight_pad_edges(pad2, prev, {0: "a", 1: "b"})
        self.assertEqual(fired, ["b"])


if __name__ == "__main__":
    unittest.main()
