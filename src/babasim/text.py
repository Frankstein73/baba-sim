"""Plain-text rendering of State / StepResult (docs/state-schema.md §7)."""

from __future__ import annotations

from collections import defaultdict

STATUS = {"playing": "进行中", "won": "胜利", "infinite_loop": "死循环（关卡被摧毁）",
          "too_complex": "过于复杂（关卡被摧毁）", "destroyed": "关卡被摧毁"}
FACING = {"right": "朝右", "up": "朝上", "left": "朝左", "down": "朝下", "none": "无朝向"}
TEXT_STATE = {"lit": "亮", "dim": "暗", "crossed": "划掉"}
ARROW = {"right": "→", "up": "↑", "left": "←", "down": "↓", "wait": "等待", "undo": "撤销", "restart": "重开"}


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


def format_state(state: dict, grid: bool = False) -> str:
    w, h = state["size"]
    lines = [f"第 {state['turn']} 回合 · {STATUS.get(state['status'], state['status'])} · "
             f"场地 {w}×{h}（x 0–{w - 1} 向右，y 0–{h - 1} 向下）"]
    objs = defaultdict(list)
    texts = []
    for o in state["objects"]:
        if o["kind"] == "object":
            objs[(o["name"], o.get("facing"))].append(tuple(o["pos"]))
        else:
            texts.append(o)
    lines.append("物体：")
    for (name, facing), cells in sorted(objs.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        dup = len(cells) - len(set(cells))
        extra = f"（其中 {dup} 个叠放）" if dup else ""
        lines.append(f"  {name}  {_ranges(cells)}{' ' + FACING[facing] if facing else ''}{extra}")
    if texts:
        has_state = "state" in texts[0]
        lines.append("文字（亮：组成生效规则 / 暗：未组成 / 划掉：被否定）：" if has_state else "文字：")
        rows = defaultdict(list)
        for t in texts:
            rows[t["pos"][1]].append(t)
        for y in sorted(rows):
            parts = []
            for t in sorted(rows[y], key=lambda t: t["pos"][0]):
                s = f"{_name(t)} ({t['pos'][0]},{t['pos'][1]})"
                if has_state:
                    s += " " + TEXT_STATE[t["state"]]
                parts.append(s)
            lines.append("  " + " · ".join(parts))
    if "rules" in state:
        lines.append("生效规则：" + "；".join(r["text"] for r in state["rules"]))
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


def _event(e):
    t = e["type"]
    if t in ("move", "teleport"):
        return f"{_name(e['what'])} {_pos(e['from'])}{'→' if t == 'move' else '⇒瞬移'}{_pos(e['to'])}"
    if t == "turn":
        return f"{_name(e['what'])} {_pos(e['what']['pos'])} 转向{FACING[e['to']][1:]}"
    if t == "destroy":
        return f"{_pos(e['what']['pos'])} 的 {_name(e['what'])} 消失"
    if t == "create":
        return f"{_pos(e['what']['pos'])} 出现 {_name(e['what'])}"
    if t == "transform":
        return f"{_pos(e['pos'])} 的 {_name(e['from'])} 变成 {_name(e['to'])}"
    if t == "text_state":
        return f"{_name(e['what'])} {_pos(e['what']['pos'])} {TEXT_STATE[e['from']]}→{TEXT_STATE[e['to']]}"
    if t == "rule_on":
        return f"规则成立：{e['rule']}"
    if t == "rule_off":
        return f"规则失效：{e['rule']}"
    return {"win": "胜利", "infinite_loop": "死循环，关卡被摧毁", "too_complex": "过于复杂，关卡被摧毁",
            "destroyed": "关卡被摧毁"}.get(t, t)


def format_events(action: str, events: list) -> str:
    head = f"本回合（{ARROW.get(action, action)}）："
    if not events:
        return head + "什么都没发生"
    phases = defaultdict(list)
    for e in events:
        phases[e["phase"]].append(_event(e))
    return "\n".join([head] + [f"  {i}. " + "；".join(parts) for i, (_, parts) in enumerate(sorted(phases.items()), 1)])


def format_step(result: dict, before: dict | None = None, grid: bool = False) -> str:
    """Events then end state. Pass the previous State to flag 'looks the same but things happened'."""
    out = [format_state(result["state"], grid), "", format_events(result["action"], result["events"])]
    if before is not None and result["events"] and before["objects"] == result["state"]["objects"]:
        out.append("  （终点与起点外观相同）")
    return "\n".join(out)
