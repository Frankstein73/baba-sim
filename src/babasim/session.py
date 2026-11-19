"""Tool-calling session: what a model needs to play one level.

Transport-agnostic. `tools()` gives function schemas (OpenAI-compatible function calling),
`call(name, arguments)` executes one tool call and returns the observation to send back.

    s = Session("0level")
    messages = [{"role": "system", "content": s.system_prompt()},
                {"role": "user", "content": s.initial_observation()}]
    ... model replies with tool calls ...
    result = s.call("move", {"actions": ["right", "right"]})
"""

from __future__ import annotations

import base64
import io
import json

from babasim.api import ACTION_NAMES, ACTIONS, Game
from babasim.text import format_events, format_state

MOVES = ["up", "down", "left", "right", "wait"]

# The prompts say how to interact, not how the game works: finding that out is the task.
M = {
    "en": {
        "move": "Perform one or more actions in order (at most {n}). \"wait\" passes a turn without moving. "
                "Stops early if the level ends; the remaining actions are then not performed.",
        "undo": "Take back the most recent turns.",
        "restart": "Reset the level to its initial state.",
        "look": "Show the current state again. Does not use a turn.",
        "system": [
            "You are playing a puzzle game on a grid. Work out how the game behaves and win the level.",
            "Interact only through the tools: move, undo, restart, look.",
            "Positions are (x,y): x grows to the right, y grows downwards, both start at 0. "
            "\"up\" decreases y, \"down\" increases y.",
            "Each tool call returns what changed and the state afterwards.",
        ],
        "limits": "Limits: {b}.", "lim_calls": "at most {n} tool calls", "lim_steps": "at most {n} turns",
        "over_won": "The game is over: level won.", "over_budget": "The game is over: limits used up.",
        "invalid": "Invalid call: {e}", "not_object": "arguments must be a JSON object",
        "no_tool": "no tool named {name}; available: move, undo, restart, look",
        "bad_actions": "actions must be a non-empty array of up/down/left/right/wait",
        "too_many": "at most {n} actions per call", "bad_action": "unknown action {a!r}; available: up, down, left, right, wait",
        "destroyed": "the level has been destroyed; only undo or restart are possible",
        "steps_out": "(turn limit reached; the remaining actions were not performed)",
        "stopped": "(stopped early; the remaining {n} actions were not performed)",
        "bad_steps": "steps must be a positive integer",
        "undone": "Took back {n} turn(s).", "undo_none": "Already at the initial state; nothing to take back.",
        "restarted": "Level reset.", "left_calls": "calls left: {n}", "left_steps": "turns left: {n}",
        "budget": "({b})", "join": ", ",
    },
    "zh": {
        "move": "按顺序执行一个或多个操作（最多 {n} 个）。wait 表示原地等待一回合。关卡结束时提前停止，后面的操作不执行。",
        "undo": "撤销最近的若干回合。",
        "restart": "把关卡重置到初始状态。",
        "look": "重新查看当前状态，不消耗回合。",
        "system": [
            "你在玩一个网格上的解谜游戏。弄清楚游戏的运作方式，并通过这一关。",
            "只能通过工具交互：move、undo、restart、look。",
            "坐标 (x,y)：x 向右增大，y 向下增大，都从 0 开始。up 使 y 减小，down 使 y 增大。",
            "每次工具调用会返回发生的变化和之后的状态。",
        ],
        "limits": "限制：{b}。", "lim_calls": "最多 {n} 次工具调用", "lim_steps": "最多 {n} 个回合",
        "over_won": "游戏已结束：已胜利。", "over_budget": "游戏已结束：已用完限制。",
        "invalid": "调用无效：{e}", "not_object": "参数必须是对象",
        "no_tool": "没有名为 {name} 的工具；可用：move、undo、restart、look",
        "bad_actions": "actions 必须是非空数组，元素为 up/down/left/right/wait",
        "too_many": "一次最多 {n} 个操作", "bad_action": "未知操作 {a!r}；可用：up、down、left、right、wait",
        "destroyed": "关卡已被摧毁，只能 undo 或 restart",
        "steps_out": "（回合数已用完，后面的操作没有执行）",
        "stopped": "（提前停止，后面 {n} 个操作没有执行）",
        "bad_steps": "steps 必须是正整数",
        "undone": "已撤销 {n} 回合。", "undo_none": "已经在初始状态，没有可撤销的回合。",
        "restarted": "关卡已重置。", "left_calls": "剩余调用 {n}", "left_steps": "剩余回合 {n}",
        "budget": "（{b}）", "join": "，",
    },
}


class Session:
    def __init__(self, level: str, world: str = "baba", seed: int = 0, rules: str = "lit",
                 obs: str = "text", grid: bool = False, max_actions_per_call: int = 32,
                 max_calls: int | None = None, max_steps: int | None = None, tile_px: int = 48,
                 lang: str = "en"):
        if obs not in ("text", "json", "image", "text+image", "gif", "text+gif"):
            raise ValueError("obs must be text, json, image, text+image, gif or text+gif")
        self.game = Game(level, world, seed, rules)
        self.obs, self.grid, self.tile_px = obs, grid, tile_px
        self.lang, self.m = lang, M[lang]
        self.max_actions_per_call = max_actions_per_call
        self.max_calls, self.max_steps = max_calls, max_steps
        # calls and executed steps are counted separately (docs/state-schema.md §9)
        self.stats = {"calls": 0, "steps": 0, "undos": 0, "restarts": 0, "invalid_calls": 0}
        self.history: list[dict] = []  # every executed call, for replay / scoring
        self._renderer = None
        self._clip = []  # pictures of the call being executed (gif modes)

    # ---- what the model is told ------------------------------------------------------------
    def tools(self) -> list[dict]:
        def fn(name, description, properties=None, required=()):
            return {"type": "function", "function": {
                "name": name, "description": description,
                "parameters": {"type": "object", "properties": properties or {},
                               "required": list(required), "additionalProperties": False}}}

        m = self.m
        return [
            fn("move", m["move"].format(n=self.max_actions_per_call),
               {"actions": {"type": "array", "items": {"type": "string", "enum": MOVES},
                            "minItems": 1, "maxItems": self.max_actions_per_call}}, ["actions"]),
            fn("undo", m["undo"], {"steps": {"type": "integer", "minimum": 1, "default": 1}}),
            fn("restart", m["restart"]),
            fn("look", m["look"]),
        ]

    def system_prompt(self) -> str:
        m = self.m
        budget = []
        if self.max_calls is not None:
            budget.append(m["lim_calls"].format(n=self.max_calls))
        if self.max_steps is not None:
            budget.append(m["lim_steps"].format(n=self.max_steps))
        lines = list(m["system"])
        if budget:
            lines.append(m["limits"].format(b=m["join"].join(budget)))
        return "\n".join(lines)

    def initial_observation(self):
        return self._content("", final=True)

    # ---- executing tool calls --------------------------------------------------------------
    @property
    def won(self) -> bool:
        return self.game.status == "won"

    @property
    def exhausted(self) -> bool:
        return ((self.max_calls is not None and self.stats["calls"] >= self.max_calls)
                or (self.max_steps is not None and self.stats["steps"] >= self.max_steps))

    @property
    def done(self) -> bool:
        return self.won or self.exhausted

    def call(self, name: str, arguments: dict | str | None = None):
        """Run one tool call. Returns the observation (str, or content parts in image modes).

        Bad calls never raise: the model gets an error message and the state is unchanged.
        """
        if self.done:
            return self.m["over_won"] if self.won else self.m["over_budget"]
        try:
            args = json.loads(arguments) if isinstance(arguments, str) and arguments.strip() else (arguments or {})
            if not isinstance(args, dict):
                raise ValueError(self.m["not_object"])
            self.stats["calls"] += 1
            body = getattr(self, f"_tool_{name}", None)
            if body is None:
                raise ValueError(self.m["no_tool"].format(name=name))
            text = body(args)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            self.stats["invalid_calls"] += 1
            return self.m["invalid"].format(e=e)
        self.history.append({"tool": name, "arguments": args})
        return self._content(text, final=True)

    def _tool_move(self, args):
        actions = args.get("actions")
        if isinstance(actions, str):  # tolerate "rrul" or "right,right"
            actions = [a for a in actions.replace(",", " ").split()] if (" " in actions or "," in actions) else list(actions)
        if not isinstance(actions, list) or not actions:
            raise ValueError(self.m["bad_actions"])
        if len(actions) > self.max_actions_per_call:
            raise ValueError(self.m["too_many"].format(n=self.max_actions_per_call))
        keys = []
        for a in actions:
            k = ACTIONS.get(str(a).lower())
            if k is None:
                raise ValueError(self.m["bad_action"].format(a=a))
            keys.append(k)
        if self.game.status != "playing":
            raise ValueError(self.m["destroyed"])
        out, executed = [], 0
        for k in keys:
            if self.max_steps is not None and self.stats["steps"] >= self.max_steps:
                out.append(self.m["steps_out"])
                break
            r = self.game.step(ACTION_NAMES[k])
            self._film()
            executed += 1
            self.stats["steps"] += 1
            out.append(self._events_text(r, executed))
            if r["state"]["status"] != "playing":
                if executed < len(keys):
                    out.append(self.m["stopped"].format(n=len(keys) - executed))
                break
        return "\n".join(out)

    def _tool_undo(self, args):
        n = args.get("steps", 1)
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ValueError(self.m["bad_steps"])
        done = min(n, self.game.turn)
        for _ in range(done):
            self.game.step("undo")
            self._film()
        self.stats["undos"] += done
        return self.m["undone"].format(n=done) if done else self.m["undo_none"]

    def _tool_restart(self, args):
        self.game.step("restart")
        self._film()
        self.stats["restarts"] += 1
        return self.m["restarted"]

    def _tool_look(self, args):
        return ""

    # ---- formatting ------------------------------------------------------------------------
    def _events_text(self, result, i):
        if self.obs == "json":
            return json.dumps({"action": result["action"], "events": result["events"]}, ensure_ascii=False)
        if "text" not in self.obs and self.obs != "json":
            return ""
        return f"[{i}] " + format_events(result["action"], result["events"], self.lang)

    def _state_text(self):
        state = self.game._state(self.game.last)
        if self.obs == "json":
            return json.dumps(state, ensure_ascii=False)
        if "text" not in self.obs:
            return ""
        return format_state(state, self.grid, self.lang)

    def _budget_text(self):
        parts = []
        if self.max_calls is not None:
            parts.append(self.m["left_calls"].format(n=self.max_calls - self.stats["calls"]))
        if self.max_steps is not None:
            parts.append(self.m["left_steps"].format(n=self.max_steps - self.stats["steps"]))
        return self.m["budget"].format(b=self.m["join"].join(parts)) if parts else ""

    def _content(self, text, final):
        """`text` (what the call did) followed by the current state and the remaining budget."""
        text = "\n\n".join(filter(None, [text, self._state_text()]))
        text = "\n".join(filter(None, [text, self._budget_text()]))
        pictured = "image" in self.obs or "gif" in self.obs
        if not pictured:
            return text
        still = self._painter().state_image()
        if "gif" in self.obs and len(self._clip) > 1:
            from babasim.render import gif_bytes

            kind, data = "gif", gif_bytes(self._clip)
        else:
            buf = io.BytesIO()
            still.save(buf, "PNG")
            kind, data = "png", buf.getvalue()
        self._clip = [still]  # the next call's animation starts from here
        url = f"data:image/{kind};base64," + base64.b64encode(data).decode()
        parts = [{"type": "image_url", "image_url": {"url": url}}]
        if text and "text" in self.obs:
            parts.insert(0, {"type": "text", "text": text})
        return parts

    def _painter(self):
        if self._renderer is None:
            from babasim.render import Renderer

            self._renderer = Renderer(self.game, tile_px=self.tile_px)
        return self._renderer

    def _film(self):
        """Add the pictures of the step just taken to the call's animation."""
        if "gif" in self.obs:
            self._clip += self._painter().step_frames()

    def summary(self) -> dict:
        return {"level": self.game.level, "world": self.game.world, "won": self.won,
                "status": self.game.status, "turn": self.game.turn, **self.stats}
