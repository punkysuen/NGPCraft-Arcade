"""NGPC fighting-game input: four arcade buttons from timed A/B pulses.

Fighters on NGPC read how many *emulated frames* A or B stay low. Pulses are
therefore counted in console frames (~60 Hz), not wall-clock time — otherwise
a catch-up burst (many frames in one host tick) makes a "0.1 s" tap look like
a long hold and every attack becomes heavy.
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
HEAVY_FRAMES = 36   # ~600 ms — heavy punch / heavy kick

_FIGHT_SPECS: dict[FightSlot, tuple[int, int]] = {
    "a": (A, LIGHT_FRAMES),
    "b": (B, LIGHT_FRAMES),
    "c": (A, HEAVY_FRAMES),
    "d": (B, HEAVY_FRAMES),
}


@dataclass(frozen=True)
class _Pulse:
    mask: int
    until_frame: int  # exclusive: active while frame < until_frame


class FightInputMixer:
    """Schedules NGPC A/B pulses by emulated frame index."""

    def __init__(self) -> None:
        self._pulses: list[_Pulse] = []

    def reset(self) -> None:
        self._pulses.clear()

    def trigger(self, slot: FightSlot, frame: int) -> None:
        """Start one press for a fixed number of emulated frames."""
        mask, length = _FIGHT_SPECS[slot]
        self._pulses.append(_Pulse(mask=mask, until_frame=frame + length))

    def active_mask(self, frame: int) -> int:
        self._pulses = [p for p in self._pulses if frame < p.until_frame]
        out = 0
        for p in self._pulses:
            out |= p.mask
        return out & NGPC_AB

    def merge_joypad(self, held: int, frame: int) -> int:
        return (held | self.active_mask(frame)) & 0x7F


def strip_face_buttons(mask: int) -> int:
    """Remove NGPC A/B so only fight macros (or turbo) drive face buttons."""
    return mask & ~NGPC_AB & 0x7F
