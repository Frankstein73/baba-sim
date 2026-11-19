"""The translated engine on its own: no game files, no Lua."""

import json
from pathlib import Path

import pytest

from babasim.runtime import Engine

ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS = json.loads((ROOT / "tests/data/solutions.json").read_text())["levels"]


@pytest.fixture(scope="module")
def engine():
    return Engine()


def test_level0_start(engine):
    engine.load("0level")
    rules = {" ".join(r[:3]) for r in engine.rules()}
    assert {"baba is you", "flag is win", "wall is stop", "rock is push"} <= rules
    assert len(engine.state()) == 67


def test_undo_restores_state(engine):
    engine.load("0level")
    start = engine.state()
    for k in "rruld":
        engine.move(k)
    assert engine.state() != start
    for _ in range(5):
        engine.undo()
    assert engine.state() == start


@pytest.mark.parametrize("stem", sorted(SOLUTIONS))
def test_known_solution_wins(engine, stem):
    engine.load(stem)
    for k in SOLUTIONS[stem]["moves"]:
        assert not engine.won
        engine.move(k)
        if engine.won:
            break
    assert engine.won
