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
    assert s.call("move", {"actions": ["jump"]}).startswith("调用无效")
    assert s.call("fly").startswith("调用无效")
    assert s.game.turn == 0 and s.stats["invalid_calls"] == 2
    out = s.call("move", '{"actions": ["right", "right"]}')  # arguments as a JSON string
    assert "baba (13,10)→(14,10)" in out and "第 2 回合" in out and "剩余调用 7" in out
    assert "已撤销 2 回合" in s.call("undo", {"steps": 5})
    s.call("move", {"actions": ["up"]})
    assert "第 0 回合" in s.call("restart")


def test_win_ends_session_and_counts():
    s = Session("0level")
    out = s.call("move", {"actions": ["right"] * 12})
    assert "胜利" in out and "后面 4 个操作没有执行" in out
    assert s.won and s.done
    assert s.call("move", {"actions": ["left"]}).startswith("游戏已结束")
    assert s.summary()["steps"] == 8 and s.summary()["calls"] == 1


def test_step_budget():
    s = Session("0level", max_steps=3)
    out = s.call("move", {"actions": ["right"] * 5})
    assert "回合数已用完" in out and s.game.turn == 3 and s.done and not s.won


def test_agent_loop_with_scripted_model():
    spec = importlib.util.spec_from_file_location("play_llm", ROOT / "tools" / "play_llm.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    script = iter([
        {"role": "assistant", "content": "先看看"},  # no tool call: gets nudged
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
