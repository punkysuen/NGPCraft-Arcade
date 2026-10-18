"""NGPC fighting-game input: four arcade buttons from timed A/B pulses.

Fighters on NGPC read how many *emulated frames* A or B stay low. Pulses are
therefore counted in console frames (~60 Hz), not wall-clock time — otherwise
a catch-up burst (many frames in one host tick) makes a "0.1 s" tap look like
a long hold and every attack becomes heavy.

Light A/B (slots a/b) are fixed-length taps. Heavy C/D (c/d) use real hold:
pressed for as long as the player holds the key, with a minimum of HEAVY_FRAMES
so a quick tap still registers as a heavy/charged input; longer holds support
charge supers (e.g. hold C to store power).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ngpc_input import A, B

FightSlot = Literal["a", "b", "c", "d"]

NGPC_AB = A | B

# ~60 Hz NGPC; 0.1 s / 0.6 s as frame counts. Light uses fewer frames than 6
# because many fighters treat ~4+ frames on A/B as a heavy/charged input.
_CONSOLE_HZ = 60
LIGHT_FRAMES = 3    # ~50 ms — light punch / light kick
HEAVY_FRAMES = 10   # ~167 ms at 60 Hz — minimum heavy; tune if a game mis-reads taps

_FIGHT_SPECS: dict[FightSlot, tuple[int, int]] = {
    "a": (A, LIGHT_FRAMES),
    "b": (B, LIGHT_FRAMES),
    "c": (A, HEAVY_FRAMES),
    "d": (B, HEAVY_FRAMES),
}

HEAVY_HOLD_SLOTS: frozenset[FightSlot] = frozenset({"c", "d"})


def is_heavy_hold_slot(slot: FightSlot) -> bool:
    return slot in HEAVY_HOLD_SLOTS


@dataclass(frozen=True)
class _Pulse:
    mask: int
    until_frame: int  # exclusive: active while frame < until_frame


@dataclass
class _HeavyHold:
    mask: int
    since_frame: int


class FightInputMixer:
    """Schedules NGPC A/B pulses by emulated frame index."""

    def __init__(self) -> None:
        self._pulses: list[_Pulse] = []
        self._heavy_holds: dict[FightSlot, _HeavyHold] = {}

    def reset(self) -> None:
        self._pulses.clear()
        self._heavy_holds.clear()

    def trigger(self, slot: FightSlot, frame: int) -> None:
        """Fixed-length tap (light A/B only)."""
        if is_heavy_hold_slot(slot):
            self.press_heavy(slot, frame)
            self.release_heavy(slot, frame)
            return
        mask, length = _FIGHT_SPECS[slot]
        self._pulses.append(_Pulse(mask=mask, until_frame=frame + length))

    def press_heavy(self, slot: FightSlot, frame: int) -> None:
        """Begin holding heavy punch (c) or heavy kick (d) on the A or B line."""
        if not is_heavy_hold_slot(slot):
            return
        mask, _ = _FIGHT_SPECS[slot]
        self._heavy_holds[slot] = _HeavyHold(mask=mask, since_frame=frame)

    def release_heavy(self, slot: FightSlot, frame: int) -> None:
        """End hold; if shorter than HEAVY_FRAMES, pad out to the minimum heavy length."""
        hold = self._heavy_holds.pop(slot, None)
        if hold is None:
            return
        if frame - hold.since_frame < HEAVY_FRAMES:
            self._pulses.append(
                _Pulse(mask=hold.mask, until_frame=hold.since_frame + HEAVY_FRAMES))

    def active_mask(self, frame: int) -> int:
        self._pulses = [p for p in self._pulses if frame < p.until_frame]
        out = 0
        for p in self._pulses:
            out |= p.mask
        for hold in self._heavy_holds.values():
            out |= hold.mask
        return out & NGPC_AB

    def merge_joypad(self, held: int, frame: int) -> int:
        return (held | self.active_mask(frame)) & 0x7F


def strip_face_buttons(mask: int) -> int:
    """Remove NGPC A/B so only fight macros (or turbo) drive face buttons."""
    return mask & ~NGPC_AB & 0x7F
