"""Plain-text rendering of State / StepResult (docs/state-schema.md §7)."""

from __future__ import annotations

from collections import defaultdict

L = {
    "zh": {
        "status": {"playing": "进行中", "won": "胜利", "infinite_loop": "死循环（关卡被摧毁）",
                   "too_complex": "过于复杂（关卡被摧毁）", "destroyed": "关卡被摧毁"},
        "facing": {"right": "朝右", "up": "朝上", "left": "朝左", "down": "朝下", "none": "无朝向"},
        "text_state": {"lit": "亮", "dim": "暗", "crossed": "划掉"},
        "action": {"right": "→", "up": "↑", "left": "←", "down": "↓", "wait": "等待", "undo": "撤销", "restart": "重开"},
        "head": "第 {turn} 回合 · {status} · 场地 {w}×{h}（x 0–{x1} 向右，y 0–{y1} 向下）",
        "objects": "物体：", "stacked": "（其中 {n} 个叠放）",
        "texts_state": "文字（亮 / 暗 / 划掉）：", "texts": "文字：", "rules": "生效规则：", "rule_sep": "；",
        "turn_head": "本回合（{a}）：", "nothing": "什么都没发生", "sep": "；",
        "move": "{n} {a}→{b}", "teleport": "{n} {a}⇒瞬移{b}", "turn": "{n} {p} 转{d}",
        "destroy": "{p} 的 {n} 消失", "create": "{p} 出现 {n}", "transform": "{p} 的 {a} 变成 {b}",
        "text_state_ev": "{n} {p} {a}→{b}", "rule_on": "规则成立：{r}", "rule_off": "规则失效：{r}",
        "end": {"win": "胜利", "infinite_loop": "死循环，关卡被摧毁", "too_complex": "过于复杂，关卡被摧毁",
                "destroyed": "关卡被摧毁"},
        "same": "  （终点与起点外观相同）",
    },
    "en": {
        "status": {"playing": "playing", "won": "won", "infinite_loop": "infinite loop (level destroyed)",
                   "too_complex": "too complex (level destroyed)", "destroyed": "level destroyed"},
        "facing": {"right": "facing right", "up": "facing up", "left": "facing left", "down": "facing down",
                   "none": "no facing"},
        "text_state": {"lit": "bright", "dim": "dim", "crossed": "crossed out"},
        "action": {"right": "right", "up": "up", "left": "left", "down": "down", "wait": "wait", "undo": "undo",
                   "restart": "restart"},
        "head": "Turn {turn} · {status} · field {w}×{h} (x 0–{x1} rightwards, y 0–{y1} downwards)",
        "objects": "Objects:", "stacked": " ({n} stacked on another)",
        "texts_state": "Text tiles (bright / dim / crossed out):", "texts": "Text tiles:",
        "rules": "Active rules: ", "rule_sep": "; ",
        "turn_head": "This turn ({a}):", "nothing": " nothing happened", "sep": "; ",
        "move": "{n} {a}→{b}", "teleport": "{n} {a}⇒teleports to {b}", "turn": "{n} {p} turns {d}",
        "destroy": "{n} at {p} disappears", "create": "{n} appears at {p}", "transform": "{a} at {p} becomes {b}",
        "text_state_ev": "{n} {p} {a}→{b}", "rule_on": "rule formed: {r}", "rule_off": "rule broken: {r}",
        "end": {"win": "level won", "infinite_loop": "infinite loop, level destroyed",
                "too_complex": "too complex, level destroyed", "destroyed": "level destroyed"},
        "same": "  (the end state looks identical to the start)",
    },
}


def _ranges(cells):
    """Compress cells into '(3–7,2)' style runs: horizontal runs first, then vertical ones."""
    cells = sorted(set(cells), key=lambda c: (c[1], c[0]))
    rows = defaultdict(list)
    for x, y in cells:
        rows[y].append(x)
    runs = []  # (x0, x1, y)
    for y, xs in rows.items():
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            runs.append((start, prev, y))
            start = prev = x
    singles = defaultdict(list)
    out = []
    for x0, x1, y in runs:
        if x0 == x1:
            singles[x0].append(y)
        else:
            out.append(((y, x0), f"({x0}–{x1},{y})"))
    for x, ys in singles.items():
        ys.sort()
        start = prev = ys[0]
        for y in ys[1:] + [None]:
            if y is not None and y == prev + 1:
                prev = y
                continue
            out.append(((start, x), f"({x},{start})" if start == prev else f"({x},{start}–{prev})"))
            start = prev = y
    return " ".join(s for _, s in sorted(out))


def _name(ref):
    if ref["kind"] == "object":
        return ref["name"]
    return (ref.get("word") or ref.get("letter")).upper()


def format_state(state: dict, grid: bool = False, lang: str = "en") -> str:
    T = L[lang]
    w, h = state["size"]
    lines = [T["head"].format(turn=state["turn"], status=T["status"].get(state["status"], state["status"]),
                              w=w, h=h, x1=w - 1, y1=h - 1)]
    objs = defaultdict(list)
    texts = []
    for o in state["objects"]:
        if o["kind"] == "object":
            objs[(o["name"], o.get("facing"))].append(tuple(o["pos"]))
        else:
            texts.append(o)
    lines.append(T["objects"])
    for (name, facing), cells in sorted(objs.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        dup = len(cells) - len(set(cells))
        extra = T["stacked"].format(n=dup) if dup else ""
        lines.append(f"  {name}  {_ranges(cells)}{' ' + T['facing'][facing] if facing else ''}{extra}")
    if texts:
        has_state = "state" in texts[0]
        lines.append(T["texts_state"] if has_state else T["texts"])
        rows = defaultdict(list)
        for t in texts:
            rows[t["pos"][1]].append(t)
        for y in sorted(rows):
            parts = []
            for t in sorted(rows[y], key=lambda t: t["pos"][0]):
                s = f"{_name(t)} ({t['pos'][0]},{t['pos'][1]})"
                if has_state:
                    s += " " + T["text_state"][t["state"]]
                parts.append(s)
            lines.append("  " + " · ".join(parts))
    if "rules" in state:
        lines.append(T["rules"] + T["rule_sep"].join(r["text"] for r in state["rules"]))
    if grid:
        lines += ["", format_grid(state)]
    return "\n".join(lines)


def format_grid(state: dict) -> str:
    """Auxiliary character grid: text tiles upper-case initial, objects lower-case initial."""
    w, h = state["size"]
    g = [["." for _ in range(w)] for _ in range(h)]
    for o in state["objects"]:
        x, y = o["pos"]
        if 0 <= x < w and 0 <= y < h:
            g[y][x] = o["name"][0].lower() if o["kind"] == "object" else _name(o)[0]
    head = "   " + "".join(str(x % 10) for x in range(w))
    return "\n".join([head] + [f"{y:2d} " + "".join(row) for y, row in enumerate(g)])


def _pos(p):
    return f"({p[0]},{p[1]})"


def _event(e, T):
    t = e["type"]
    if t in ("move", "teleport"):
        return T[t].format(n=_name(e["what"]), a=_pos(e["from"]), b=_pos(e["to"]))
    if t == "turn":
        return T["turn"].format(n=_name(e["what"]), p=_pos(e["what"]["pos"]), d=T["action"].get(e["to"], e["to"]))
    if t in ("destroy", "create"):
        return T[t].format(n=_name(e["what"]), p=_pos(e["what"]["pos"]))
    if t == "transform":
        return T[t].format(p=_pos(e["pos"]), a=_name(e["from"]), b=_name(e["to"]))
    if t == "text_state":
        return T["text_state_ev"].format(n=_name(e["what"]), p=_pos(e["what"]["pos"]),
                                         a=T["text_state"][e["from"]], b=T["text_state"][e["to"]])
    if t in ("rule_on", "rule_off"):
        return T[t].format(r=e["rule"])
    return T["end"].get(t, t)


def format_events(action: str, events: list, lang: str = "en") -> str:
    T = L[lang]
    head = T["turn_head"].format(a=T["action"].get(action, action))
    if not events:
        return head + T["nothing"]
    phases = defaultdict(list)
    for e in events:
        phases[e["phase"]].append(_event(e, T))
    return "\n".join([head] + [f"  {i}. " + T["sep"].join(parts) for i, (_, parts) in enumerate(sorted(phases.items()), 1)])


def format_step(result: dict, before: dict | None = None, grid: bool = False, lang: str = "en") -> str:
    """Events then end state. Pass the previous State to flag 'looks the same but things happened'."""
    out = [format_state(result["state"], grid, lang), "", format_events(result["action"], result["events"], lang)]
    if before is not None and result["events"] and before["objects"] == result["state"]["objects"]:
        out.append(L[lang]["same"])
    return "\n".join(out)
