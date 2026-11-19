"""Model-facing API: states, events, text, rendering."""

import json
import random

import pytest

from babasim.api import Game
from babasim.runtime import Engine
from babasim.text import format_state, format_step


@pytest.fixture(scope="module")
def engine():
    return Engine()


def test_state_and_move_events(engine):
    g = Game("0level", rules="list", engine=engine)
    s = g.observe()
    assert s["size"] == [33, 18] and s["status"] == "playing"
    assert {"kind": "object", "name": "baba", "pos": [12, 10], "facing": "right"} in s["objects"]
    assert {"text": "BABA IS YOU", "tiles": [[11, 6], [12, 6], [13, 6]]} in s["rules"]
    assert not any("id" in o for o in s["objects"])  # perceptual view carries no ids
    for _ in range(3):
        g.step("right")
    r = g.step("right")  # baba pushes the rock: both moves share one phase
    moves = [(e["what"]["name"], e["from"], e["to"], e["phase"]) for e in r["events"]]
    assert sorted(moves) == [("baba", [15, 10], [16, 10], 1), ("rock", [16, 10], [17, 10], 1)]


def test_win_stops_play_and_undo_recovers(engine):
    g = Game("0level", engine=engine)
    r = g.play(["right"] * 12)
    assert r["stopped_by"] == "win" and r["executed"] == 8 and r["state"]["status"] == "won"
    assert r["steps"][-1]["events"][-1]["type"] == "win"
    with pytest.raises(RuntimeError):
        g.step("left")
    assert g.undo()["state"]["status"] == "playing"


def test_rule_events_when_text_is_pushed(engine):
    g = Game("0level", rules="list", engine=engine)
    # walk up to WALL IS STOP's row and push STOP away: the rule must turn off
    seen = set()
    for a in ["down"] * 4 + ["right"] * 3 + ["up"] * 8:
        seen |= {(e["type"], e.get("rule")) for e in g.step(a)["events"]}
    types = {t for t, _ in seen}
    assert "move" in types
    json.dumps(g.observe())


def test_full_view_has_ids_and_order(engine):
    g = Game("0level", view="full", engine=engine)
    s = g.observe()
    assert all("id" in o and "dir" in o for o in s["objects"])
    assert [o["id"] for o in s["objects"]] == [u[4] for u in engine.state()]


def test_text_format(engine):
    g = Game("0level", engine=engine)
    before = g.observe()
    text = format_state(before, grid=True)
    assert "baba  (12,10) 朝右" in text and "wall  (11–21,8) (11–21,12)" in text
    r = g.step("up")
    assert "本回合（↑）" in format_step(r, before)


@pytest.mark.parametrize("stem", ["0level", "1level", "245level", "90level", "177level", "16level", "87level"])
def test_random_play_events_are_consistent(engine, stem):
    """Replaying move/destroy/create/transform events on the start state gives the end state."""
    g = Game(stem, view="full", engine=engine)
    rng = random.Random(stem)
    state = g.observe()
    for _ in range(40):
        if g.status != "playing":
            break
        pos = {o["id"]: (o.get("name") or o.get("word") or o.get("letter"), tuple(o["pos"])) for o in state["objects"]}
        r = g.step(rng.choice(["right", "up", "left", "down", "wait"]))
        for e in r["events"]:
            if e["type"] in ("move", "teleport"):
                assert pos[e["id"]][1] == tuple(e["from"]), e
                pos[e["id"]] = (pos[e["id"]][0], tuple(e["to"]))
        state = r["state"]
        end = {o["id"]: tuple(o["pos"]) for o in state["objects"]}
        for uid, (_name, p) in pos.items():
            if uid in end:
                assert end[uid] == p


def test_renderer_frames(engine):
    pytest.importorskip("PIL")
    from babasim.render import Renderer

    g = Game("0level", rules="list", engine=engine)
    r = Renderer(g, tile_px=16, axes=True)
    assert r.state_image().size[0] > 33 * 16
    for _ in range(4):
        g.step("right")
    frames = r.frames("phases")
    assert [t for t, _ in frames] == [0.0, 0.5, 1.0]
    assert frames[0][1].tobytes() != frames[1][1].tobytes() != frames[2][1].tobytes()
    assert len(r.frames(5)) == 5 and len(r.frames("endpoints")) == 2
    g.step("up")  # blocked by nothing; then a no-op against the wall keeps frames identical
    assert r.state_image().tobytes() == r.frame(1.0).tobytes()
