"""Sanity checks for the dev-only Lua oracle. Skipped when the game is not installed."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "oracle"))
pytestmark = pytest.mark.skipif(not (ROOT / "game" / "values.lua").exists(), reason="game not installed")

SOLUTIONS = json.loads((ROOT / "tests/data/solutions.json").read_text())["levels"]


@pytest.fixture(scope="module")
def oracle():
    from oracle import Oracle

    return Oracle()


def test_level0_start(oracle):
    oracle.load("0level")
    rules = {" ".join(r[:3]) for r in oracle.rules()}
    assert {"baba is you", "flag is win", "wall is stop", "rock is push"} <= rules
    assert len(oracle.state()) == 67


def test_undo_restores_state(oracle):
    oracle.load("0level")
    start = oracle.state()
    for k in "rruld":
        oracle.move(k)
    assert oracle.state() != start
    for _ in range(5):
        oracle.undo()
    assert oracle.state() == start


@pytest.mark.parametrize("stem", sorted(SOLUTIONS))
def test_known_solution_wins(oracle, stem):
    oracle.load(stem)
    for k in SOLUTIONS[stem]["moves"]:
        assert not oracle.won
        oracle.move(k)
        if oracle.won:
            break
    assert oracle.won
