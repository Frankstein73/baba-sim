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


class Session:
    def __init__(self, level: str, world: str = "baba", seed: int = 0, rules: str = "lit",
                 obs: str = "text", grid: bool = False, max_actions_per_call: int = 32,
                 max_calls: int | None = None, max_steps: int | None = None, tile_px: int = 32):
        if obs not in ("text", "json", "image", "text+image"):
            raise ValueError("obs must be text, json, image or text+image")
        self.game = Game(level, world, seed, rules)
        self.obs, self.grid, self.tile_px = obs, grid, tile_px
        self.max_actions_per_call = max_actions_per_call
        self.max_calls, self.max_steps = max_calls, max_steps
        # calls and executed steps are counted separately (docs/state-schema.md §9)
        self.stats = {"calls": 0, "steps": 0, "undos": 0, "restarts": 0, "invalid_calls": 0}
        self.history: list[dict] = []  # every executed call, for replay / scoring
        self._renderer = None

    # ---- what the model is told ------------------------------------------------------------
    def tools(self) -> list[dict]:
        def fn(name, description, properties=None, required=()):
            return {"type": "function", "function": {
                "name": name, "description": description,
                "parameters": {"type": "object", "properties": properties or {},
                               "required": list(required), "additionalProperties": False}}}

        return [
            fn("move", f"按顺序执行一个或多个操作（最多 {self.max_actions_per_call} 个）。"
                       "wait 表示原地等待一回合。胜利或关卡被摧毁时提前停止，后面的操作不执行。",
               {"actions": {"type": "array", "items": {"type": "string", "enum": MOVES},
                            "minItems": 1, "maxItems": self.max_actions_per_call}}, ["actions"]),
            fn("undo", "撤销最近的若干回合，回到之前的状态。",
               {"steps": {"type": "integer", "minimum": 1, "default": 1}}),
            fn("restart", "把关卡重置到初始状态。"),
            fn("look", "重新查看当前状态，不消耗回合。"),
        ]

    def system_prompt(self) -> str:
        budget = []
        if self.max_calls is not None:
            budget.append(f"最多 {self.max_calls} 次工具调用")
        if self.max_steps is not None:
            budget.append(f"最多 {self.max_steps} 个回合")
        return "\n".join(filter(None, [
            "你在玩一个推箱子式的规则解谜游戏。场地上的文字方块组成规则（例如 BABA IS YOU），"
            "推动文字可以改变规则。目标是让你控制的对象（YOU）碰到带有 WIN 属性的对象。",
            "通过工具与游戏交互：move 执行操作，undo 撤销，restart 重置，look 查看当前状态。",
            "坐标 (x,y)：x 向右增大，y 向下增大，从 0 开始。up 使 y 减小，down 使 y 增大。",
            "每次工具调用会返回这些操作引起的变化和之后的状态。",
            "限制：" + "，".join(budget) + "。" if budget else "",
        ]))

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
            return "游戏已结束：" + ("已胜利。" if self.won else "已用完限制。")
        try:
            args = json.loads(arguments) if isinstance(arguments, str) and arguments.strip() else (arguments or {})
            if not isinstance(args, dict):
                raise ValueError("参数必须是对象")
            self.stats["calls"] += 1
            body = getattr(self, f"_tool_{name}", None)
            if body is None:
                raise ValueError(f"没有名为 {name} 的工具；可用：move、undo、restart、look")
            text = body(args)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            self.stats["invalid_calls"] += 1
            return f"调用无效：{e}"
        self.history.append({"tool": name, "arguments": args})
        return self._content(text, final=True)

    def _tool_move(self, args):
        actions = args.get("actions")
        if isinstance(actions, str):  # tolerate "rrul" or "right,right"
            actions = [a for a in actions.replace(",", " ").split()] if (" " in actions or "," in actions) else list(actions)
        if not isinstance(actions, list) or not actions:
            raise ValueError("actions 必须是非空数组，元素为 up/down/left/right/wait")
        if len(actions) > self.max_actions_per_call:
            raise ValueError(f"一次最多 {self.max_actions_per_call} 个操作")
        keys = []
        for a in actions:
            k = ACTIONS.get(str(a).lower())
            if k is None:
                raise ValueError(f"未知操作 {a!r}；可用：up、down、left、right、wait")
            keys.append(k)
        if self.game.status != "playing":
            raise ValueError("关卡已被摧毁，只能 undo 或 restart")
        out, executed = [], 0
        for k in keys:
            if self.max_steps is not None and self.stats["steps"] >= self.max_steps:
                out.append("（回合数已用完，后面的操作没有执行）")
                break
            r = self.game.step(ACTION_NAMES[k])
            executed += 1
            self.stats["steps"] += 1
            out.append(self._events_text(r, executed))
            if r["state"]["status"] != "playing":
                if executed < len(keys):
                    out.append(f"（提前停止，后面 {len(keys) - executed} 个操作没有执行）")
                break
        return "\n".join(out)

    def _tool_undo(self, args):
        n = args.get("steps", 1)
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ValueError("steps 必须是正整数")
        done = min(n, self.game.turn)
        for _ in range(done):
            self.game.step("undo")
        self.stats["undos"] += done
        return f"已撤销 {done} 回合。" if done else "已经在初始状态，没有可撤销的回合。"

    def _tool_restart(self, args):
        self.game.step("restart")
        self.stats["restarts"] += 1
        return "关卡已重置。"

    def _tool_look(self, args):
        return ""

    # ---- formatting ------------------------------------------------------------------------
    def _events_text(self, result, i):
        if self.obs == "json":
            return json.dumps({"action": result["action"], "events": result["events"]}, ensure_ascii=False)
        if self.obs == "image":
            return ""
        return f"[{i}] " + format_events(result["action"], result["events"])

    def _state_text(self):
        state = self.game._state(self.game.last)
        if self.obs == "json":
            return json.dumps(state, ensure_ascii=False)
        if self.obs == "image":
            return ""
        return format_state(state, self.grid)

    def _budget_text(self):
        parts = []
        if self.max_calls is not None:
            parts.append(f"剩余调用 {self.max_calls - self.stats['calls']}")
        if self.max_steps is not None:
            parts.append(f"剩余回合 {self.max_steps - self.stats['steps']}")
        return "（" + "，".join(parts) + "）" if parts else ""

    def _content(self, text, final):
        """`text` (what the call did) followed by the current state and the remaining budget."""
        text = "\n\n".join(filter(None, [text, self._state_text()]))
        text = "\n".join(filter(None, [text, self._budget_text()]))
        if "image" not in self.obs:
            return text
        if self._renderer is None:
            from babasim.render import Renderer

            self._renderer = Renderer(self.game, tile_px=self.tile_px, axes=True)
        buf = io.BytesIO()
        self._renderer.state_image().save(buf, "PNG")
        url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
        parts = [{"type": "image_url", "image_url": {"url": url}}]
        if text:
            parts.insert(0, {"type": "text", "text": text})
        return parts

    def summary(self) -> dict:
        return {"level": self.game.level, "world": self.game.world, "won": self.won,
                "status": self.game.status, "turn": self.game.turn, **self.stats}
