"""Translated engine vs the original Lua, step by step. Skipped when the game is not installed."""

import random
import sys
from pathlib import Path

import pytest

from babasim.runtime import Engine

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "oracle"))
pytestmark = pytest.mark.skipif(not (ROOT / "game" / "values.lua").exists(), reason="game not installed")

LEVELS = ["0level", "1level", "189level", "3level", "90level", "177level", "207level", "206level",
          "16level", "169level", "87level", "245level", "130level", "327level"]


def noid(state):
    return sorted((u[:4] + u[5:] for u in state), key=str)


@pytest.mark.parametrize("stem", LEVELS)
def test_random_walk_matches_oracle(stem):
    from oracle import Oracle

    o, e = Oracle(), Engine()
    o.load(stem)
    e.load(stem)
    rng = random.Random(stem)
    for _ in range(60):
        k = rng.choice("rrrruuuullllddddwz")
        o.undo() if k == "z" else o.move(k)
        e.undo() if k == "z" else e.move(k)
        if o.state() != e.state() and noid(o.state()) == noid(e.state()):
            return  # creation order from a string-keyed pairs(): random per run in the game too
        assert o.state() == e.state()
        assert sorted(o.rules()) == sorted(e.rules())
        assert o.won == e.won
