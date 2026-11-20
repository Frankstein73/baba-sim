"""Tool-calling session and the agent loop, driven by a scripted stand-in for a model."""

import importlib.util
import json
from pathlib import Path

from babasim.session import Session

ROOT = Path(__file__).resolve().parent.parent


def test_tools_and_bad_calls():
    s = Session("0level", max_calls=10)
    assert [t["function"]["name"] for t in s.tools()] == ["move", "undo", "restart", "look"]
    assert "baba  (12,10)" in s.initial_observation()
    assert s.call("move", {"actions": ["jump"]}).startswith("Invalid call")
    assert s.call("fly").startswith("Invalid call")
    assert s.game.turn == 0 and s.stats["invalid_calls"] == 2
    out = s.call("move", '{"actions": ["right", "right"]}')  # arguments as a JSON string
    assert "baba (13,10)→(14,10)" in out and "Turn 2" in out and "calls left: 7" in out
    assert "Took back 2 turn(s)" in s.call("undo", {"steps": 5})
    s.call("move", {"actions": ["up"]})
    assert "Turn 0" in s.call("restart")
    zh = Session("0level", lang="zh")
    assert "已撤销" in zh.call("undo") or "没有可撤销" in zh.call("undo")
    assert "WIN" not in s.system_prompt() and "rule" not in s.system_prompt().lower()


def test_win_ends_session_and_counts():
    s = Session("0level")
    out = s.call("move", {"actions": ["right"] * 12})
    assert "level won" in out and "remaining 4 actions were not performed" in out
    assert s.won and s.done
    assert s.call("move", {"actions": ["left"]}).startswith("The game is over")
    assert s.summary()["steps"] == 8 and s.summary()["calls"] == 1


def test_step_budget():
    s = Session("0level", max_steps=3)
    out = s.call("move", {"actions": ["right"] * 5})
    assert "turn limit reached" in out and s.game.turn == 3 and s.done and not s.won


def test_agent_loop_with_scripted_model():
    spec = importlib.util.spec_from_file_location("play_llm", ROOT / "tools" / "play_llm.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    script = iter([
        {"role": "assistant", "content": "let me think"},  # no tool call: gets nudged
        {"role": "assistant", "tool_calls": [{"id": "1", "type": "function", "function": {
            "name": "move", "arguments": json.dumps({"actions": ["right"] * 4})}}]},
        {"role": "assistant", "tool_calls": [{"id": "2", "type": "function", "function": {
            "name": "move", "arguments": json.dumps({"actions": ["right"] * 4})}}]},
    ])
    s = Session("0level", max_calls=5)
    messages = mod.play(s, lambda messages, tools: next(script), log=lambda _: None)
    assert s.won and s.stats["calls"] == 2
    assert [m["role"] for m in messages] == ["system", "user", "assistant", "user", "assistant", "tool", "assistant", "tool"]


def test_image_observation():
    import pytest

    pytest.importorskip("PIL")
    s = Session("0level", obs="text+image", tile_px=8)
    parts = s.call("move", {"actions": ["right"]})
    assert parts[0]["type"] == "text" and parts[1]["image_url"]["url"].startswith("data:image/png;base64,")


def test_gif_observation_shows_the_whole_call():
    import base64
    import io

    import pytest

    PIL = pytest.importorskip("PIL.Image")
    s = Session("0level", obs="text+gif", tile_px=24)
    assert s.initial_observation()[1]["image_url"]["url"].startswith("data:image/png;base64,")  # nothing moved yet
    parts = s.call("move", {"actions": ["right", "right", "up"]})
    url = parts[1]["image_url"]["url"]
    assert parts[0]["type"] == "text" and url.startswith("data:image/gif;base64,")
    clip = PIL.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1])))
    assert clip.n_frames >= 1 + 3 * 2 and clip.size == (33 * 24, 18 * 24)  # start, then every step
    assert s.call("look")[1]["image_url"]["url"].startswith("data:image/png;base64,")
    assert s.call("undo")[1]["image_url"]["url"].startswith("data:image/gif;base64,")


def test_replay_leaves_out_what_was_taken_back():
    s = Session("0level", max_calls=20)
    assert "Limits" not in s.system_prompt() and "80" not in s.system_prompt()
    s.call("move", {"actions": ["up", "up"]})
    s.call("restart")  # everything before is gone
    s.call("move", {"actions": ["left", "left", "left", "right"]})  # baba walks into the wall: turns that change nothing
    s.call("move", {"actions": ["down", "down"]})
    s.call("undo", {"steps": 1})
    s.call("look")
    s.call("move", {"actions": ["right"] * 8})
    r = s.replay()
    assert r["verified"] and r["gif"] is None and r["status"] == s.game.status
    assert len(r["actions"]) == len(r["sources"]) < s.stats["steps"]
    again = Session("0level")
    again.call("move", {"actions": r["actions"]})
    assert again.game.observe()["objects"] == s.game.observe()["objects"]
    assert all(call > 2 for call, _ in r["sources"])  # nothing from before the restart


def test_replay_of_a_won_game_is_one_animation_from_the_start():
    import base64
    import io

    import pytest

    PIL = pytest.importorskip("PIL.Image")
    s = Session("0level", tile_px=24)
    s.call("move", {"actions": ["up", "down", "left"]})
    s.call("undo", {"steps": 3})
    s.call("move", {"actions": ["right"] * 8})
    r = s.replay(gif=True)
    assert r["won"] and r["verified"] and r["actions"] == ["right"] * 8
    clip = PIL.open(io.BytesIO(base64.b64decode(r["gif"].split(",", 1)[1])))
    assert clip.size == (33 * 24, 18 * 24) and clip.n_frames >= 1 + 8
    from babasim.render import Renderer

    start = Renderer(Session("0level", tile_px=24).game, tile_px=24).state_image().convert("RGB")
    clip.seek(0)
    assert clip.convert("RGB").tobytes() == start.tobytes()  # opens on the starting position
    clip.seek(clip.n_frames - 1)
    end = Renderer(s.game, tile_px=24).state_image().convert("RGB")
    assert clip.convert("RGB").tobytes() == end.tobytes()  # and ends on the state the game was left in


def test_dataset_rows_carry_a_picture_of_the_starting_position():
    import pytest

    pytest.importorskip("PIL")
    from babasim.dataset import rows

    (row,) = rows(["0level"], tile_px=8, max_calls=80)
    assert row["initial_image"].startswith("data:image/png;base64,") and "Limits" not in row["prompt"]
    assert "calls left: 80" in row["initial_state"]
    prompt, shown, state = row["problem_statement"].split("\n\n", 2)  # what a viewer shows as the task
    assert prompt == row["prompt"] and shown == f"![starting position]({row['initial_image']})"
    assert state == f"```\n{row['initial_state']}\n```"
    assert "initial_image" not in next(rows(["0level"], images=False))
