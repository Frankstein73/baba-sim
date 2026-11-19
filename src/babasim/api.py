"""Model-facing API over the engine: states, per-turn events, text observations.

Follows docs/state-schema.md. `Game.step` returns a StepResult dict (events + end state);
`view="perceptual"` shows only what a player sees, `view="full"` the whole engine state.
"""

from __future__ import annotations

from babasim.runtime import Engine

ACTIONS = {"right": "r", "up": "u", "left": "l", "down": "d", "wait": "w",
           "r": "r", "u": "u", "l": "l", "d": "d", "w": "w"}
ACTION_NAMES = {"r": "right", "u": "up", "l": "left", "d": "down", "w": "wait"}
FACING = {0: "right", 1: "up", 2: "left", 3: "down"}
TEXT_CLASS = {0: "noun", 1: "verb", 2: "property", 3: "prefix", 4: "not", 6: "and", 7: "condition"}
BASE_RULES = {("text", "is", "push"), ("level", "is", "stop"), ("cursor", "is", "select")}
# Lua entry points that start a new stage of a turn (events of different stages never share a phase)
STAGES = ("movecommand", "fallblock", "conversion", "levelblock", "block",
          "dolevelconversions", "effectblock", "destroylevel_do")
DESTROY_STATUS = {"infinity": "infinite_loop", "toocomplex": "too_complex"}


class Game:
    def __init__(self, level: str, world: str = "baba", seed: int = 0, rules: str = "lit",
                 view: str = "perceptual", base_rules: bool = False, engine: Engine | None = None):
        if rules not in ("none", "lit", "list") or view not in ("perceptual", "full"):
            raise ValueError("rules must be none/lit/list and view perceptual/full")
        self.level, self.world, self.seed = level, world, seed
        self.rules_mode, self.view, self.base_rules = rules, view, base_rules
        self.engine = engine or Engine(world)
        self._hook()
        self.restart()

    # ---- engine hooks ------------------------------------------------------------------
    def _hook(self):
        G = self.engine.G
        if G.get("_api_hooked"):
            self._shared = G["_api_hooked"]
            return
        shared = self._shared = {"log": [], "stage": 0, "destroyed": None, "names": {}}
        G["_api_hooked"] = shared
        addundo = G["addundo"]

        def addundo_logged(line=None, uid=None, *_):
            shared["log"].append((shared["stage"], list(line.arr)))
            return addundo(line, uid)

        G["addundo"] = addundo_logged
        destroylevel = G["destroylevel"]

        def destroylevel_logged(special=None, *_):
            shared["destroyed"] = special or "destroyed"
            return destroylevel(special)

        G["destroylevel"] = destroylevel_logged
        for name in STAGES:
            G[name] = self._staged(G[name], shared, name)

    @staticmethod
    def _staged(fn, shared, name):
        def staged(*a):
            shared["stage"] += 1
            shared["names"][shared["stage"]] = name
            return fn(*a)

        return staged

    # ---- lifecycle ---------------------------------------------------------------------
    def restart(self) -> dict:
        self._shared["destroyed"] = None
        self.engine.load(self.level, self.world, self.seed)
        self.turn = 0
        self._info = {}
        self._status_stack = []
        self.last = None
        state = self.observe()
        self._anim = (self.last, self.last, [])
        return state

    @property
    def status(self) -> str:
        if self.engine.won:
            return "won"
        d = self._shared["destroyed"]
        if d is not None:
            return DESTROY_STATUS.get(d, "destroyed")
        return "playing"

    # ---- object description ------------------------------------------------------------
    def _describe(self, name):
        """(kind, word, class, shows_facing) for an object name."""
        info = self._info.get(name)
        if info is None:
            G = self.engine.G
            cls = G["unitreference"][name]
            typ = tiling = None
            if cls is not None and cls != "level":
                typ = G["getactualdata_objlist"](cls, "type")[0]
                tiling = G["getactualdata_objlist"](cls, "tiling")[0]
            if name.startswith("text_"):
                word = name[5:]
                info = ("letter", word, None, False) if typ == 5 else ("text", word, TEXT_CLASS.get(typ, "noun"), False)
            else:
                info = ("object", name, None, tiling in (0, 2, 3))
            self._info[name] = info
        return info

    def _ref(self, name, x, y):
        kind, word, _cls, _f = self._describe(name)
        key = {"object": "name", "text": "word", "letter": "letter"}[kind]
        return {"kind": kind, key: word, "pos": [x - 1, y - 1]}

    def _units(self):
        """Full snapshot of every unit, in engine order."""
        G = self.engine.G
        K = {k: G[k] for k in ("UNITNAME", "XPOS", "YPOS", "DIR", "ID", "FLOAT", "ZLAYER")}
        hide = G["featureindex"]["hide"] is not None
        hasfeature, getname = G["hasfeature"], G["getname"]
        out = []
        for u in G["units"].arr:
            v = u["values"]
            name = u["strings"][K["UNITNAME"]]
            hidden = bool(hide and hasfeature(getname(u), "is", "hide", u["fixed"]) is not None)
            out.append({"id": v[K["ID"]], "name": name, "x": v[K["XPOS"]], "y": v[K["YPOS"]],
                        "dir": v[K["DIR"]], "float": v[K["FLOAT"]], "z": v[K["ZLAYER"]],
                        "hidden": hidden, "fixed": u["fixed"]})
        return out

    def _rules(self):
        """Active rules with the text tiles that spell them; plus lit/crossed text ids."""
        G = self.engine.G
        objs = self.engine.objs
        K = {k: G[k] for k in ("UNITNAME", "XPOS", "YPOS", "ID")}
        rules, lit, blocked = [], set(), set()
        for f in G["features"].arr:
            r, conds, ids = f[1], f[2], f[3]
            never = any(c[1] == "never" for c in conds.arr) if conds is not None else False
            words, tiles = [], []
            for group in ids.arr if ids is not None else []:
                for fixed in group.arr:
                    u = objs.get(fixed)
                    if u is None:
                        continue
                    uid = u["values"][K["ID"]]
                    (blocked if never else lit).add(uid)
                    words.append(u["strings"][K["UNITNAME"]][5:].upper())
                    tiles.append([u["values"][K["XPOS"]] - 1, u["values"][K["YPOS"]] - 1])
            base = (r[1], r[2], r[3]) in BASE_RULES and not tiles
            if never or (base and not self.base_rules):
                continue
            text = " ".join(words) if words else f"{r[1]} {r[2]} {r[3]}".upper()
            rule = {"text": text, "tiles": tiles}
            if rule not in rules:
                rules.append(rule)
        return rules, lit, blocked - lit

    def _snapshot(self):
        rules, lit, crossed = self._rules()
        return {"units": self._units(), "rules": rules, "lit": lit, "crossed": crossed,
                "status": self.status, "turn": self.turn}

    # ---- State -------------------------------------------------------------------------
    def _text_state(self, snap, uid):
        return "lit" if uid in snap["lit"] else ("crossed" if uid in snap["crossed"] else "dim")

    def _state(self, snap) -> dict:
        G = self.engine.G
        full = self.view == "full"
        objects = []
        units = snap["units"] if full else sorted(snap["units"], key=lambda u: (u["y"], u["x"], u["z"]))
        for u in units:
            if u["hidden"] and not full:
                continue
            kind, word, cls, shows_facing = self._describe(u["name"])
            o = {"kind": kind}
            if kind == "object":
                o["name"] = word
            elif kind == "text":
                o["word"], o["class"] = word, cls
            else:
                o["letter"] = word
            o["pos"] = [u["x"] - 1, u["y"] - 1]
            if kind == "object" and (shows_facing or full):
                o["facing"] = FACING.get(u["dir"], "none")
            if kind != "object" and self.rules_mode != "none":
                o["state"] = self._text_state(snap, u["id"])
            if full:
                o.update(id=u["id"], dir=u["dir"], float=u["float"], hidden=u["hidden"])
            objects.append(o)
        state = {"turn": snap["turn"], "status": snap["status"],
                 "size": [G["roomsizex"] - 2, G["roomsizey"] - 2], "objects": objects}
        if self.rules_mode == "list":
            state["rules"] = snap["rules"]
        return state

    def observe(self) -> dict:
        self.last = self._snapshot()
        return self._state(self.last)

    # ---- events ------------------------------------------------------------------------
    def _events(self, before, after, log, full=None):
        """Events of one move from the engine's own change log (the undo buffer entries)."""
        full = self.view == "full" if full is None else full
        after_ids = {u["id"]: u["hidden"] for u in after["units"]}
        hidden = {u["id"] for u in before["units"] if u["hidden"] and after_ids.get(u["id"], True)}
        names = self._shared["names"]
        raw = []  # (stage, subject id, event)
        pending = {}  # unit id -> name it is being converted from
        for stage, line in log:
            kind = line[0]
            if kind == "update":
                _, name, ox, oy, odir, x, y, d, uid = line[:9]
                if (ox, oy) != (x, y):
                    far = abs(ox - x) + abs(oy - y) > 1
                    typ = "teleport" if far and names.get(stage) != "fallblock" else "move"
                    raw.append((stage, uid, {"type": typ, "what": self._ref(name, ox, oy),
                                             "from": [ox - 1, oy - 1], "to": [x - 1, y - 1]}))
                if odir != d and (full or self._describe(name)[3]):
                    raw.append((stage, uid, {"type": "turn", "what": self._ref(name, x, y),
                                             "from": FACING.get(odir, "none"), "to": FACING.get(d, "none")}))
            elif kind == "remove":
                _, name, x, y, _d, uid = line[:6]
                raw.append((stage, uid, {"type": "destroy", "what": self._ref(name, x, y)}))
            elif kind == "create":
                _, name, uid, _base, _src, x, y, _d = line[:8]
                old = pending.pop(uid, None)
                if old is False:  # already reported as a transform
                    continue
                if old is not None and old != name:
                    a, b = self._ref(old, x, y), self._ref(name, x, y)
                    a.pop("pos"), b.pop("pos")
                    raw.append((stage, uid, {"type": "transform", "pos": [x - 1, y - 1], "from": a, "to": b}))
                else:
                    raw.append((stage, uid, {"type": "create", "what": self._ref(name, x, y)}))
            elif kind == "convert":
                # the object at (x, y) turns into something else; the matching "create" line
                # that follows carries the name of the result
                _, old, new, uid, _base, x, y, _d = line[:8]
                if new == "empty":
                    raw.append((stage, uid, {"type": "destroy", "what": self._ref(old, x, y)}))
                elif isinstance(old, str) and old != "empty":
                    pending[uid] = old
        events, phase, last_stage, seen = [], 0, None, set()
        for stage, uid, ev in raw:
            if uid in hidden and not full:
                continue
            if stage != last_stage or uid in seen:
                phase += 1
                seen = set()
                last_stage = stage
            seen.add(uid)
            ev = {"phase": phase, **ev}
            if full:
                ev["id"] = uid
            events.append(ev)
        return events, phase

    def _diff_events(self, before, after, full=None):
        """Events for undo/restart, where the engine keeps no log: plain state difference."""
        full = self.view == "full" if full is None else full
        b = {u["id"]: u for u in before["units"]}
        a = {u["id"]: u for u in after["units"]}
        events = []
        for uid, u in b.items():
            v = a.get(uid)
            if u["hidden"] and (v is None or v["hidden"]) and not full:
                continue
            if v is None or v["name"] != u["name"]:
                events.append({"phase": 1, "type": "destroy", "what": self._ref(u["name"], u["x"], u["y"])})
                if v is not None:
                    events.append({"phase": 1, "type": "create", "what": self._ref(v["name"], v["x"], v["y"])})
                continue
            if (u["x"], u["y"]) != (v["x"], v["y"]):
                events.append({"phase": 1, "type": "move", "what": self._ref(u["name"], u["x"], u["y"]),
                               "from": [u["x"] - 1, u["y"] - 1], "to": [v["x"] - 1, v["y"] - 1]})
            if u["dir"] != v["dir"] and (full or self._describe(u["name"])[3]):
                events.append({"phase": 1, "type": "turn", "what": self._ref(u["name"], v["x"], v["y"]),
                               "from": FACING.get(u["dir"], "none"), "to": FACING.get(v["dir"], "none")})
        for uid, v in a.items():
            if uid not in b and not (v["hidden"] and not full):
                events.append({"phase": 1, "type": "create", "what": self._ref(v["name"], v["x"], v["y"])})
        return events, 1 if events else 0

    def _meta_events(self, before, after, phase):
        """Rule and text-state changes, win / loop: derived by comparing the two snapshots."""
        events = []
        p = phase + 1
        if self.rules_mode != "none":
            b = {u["id"]: u for u in before["units"]}
            for u in after["units"]:
                if not u["name"].startswith("text_") or u["id"] not in b:
                    continue
                s0, s1 = self._text_state(before, u["id"]), self._text_state(after, u["id"])
                if s0 != s1:
                    events.append({"phase": p, "type": "text_state", "what": self._ref(u["name"], u["x"], u["y"]),
                                   "from": s0, "to": s1})
        if self.rules_mode == "list":
            old = {r["text"] for r in before["rules"]}
            new = {r["text"] for r in after["rules"]}
            events += [{"phase": p, "type": "rule_off", "rule": r["text"]} for r in before["rules"] if r["text"] not in new]
            events += [{"phase": p, "type": "rule_on", "rule": r["text"]} for r in after["rules"] if r["text"] not in old]
        if after["status"] != before["status"] and after["status"] != "playing":
            events.append({"phase": p, "type": "win" if after["status"] == "won" else after["status"]})
        return events

    # ---- actions -----------------------------------------------------------------------
    def step(self, action: str) -> dict:
        """One action: up/down/left/right/wait, undo, restart."""
        before = self.last or self._snapshot()
        if action == "restart":
            self.restart()
            after = self.last
            events, phase = self._diff_events(before, after)
            anim = events
        elif action == "undo":
            if self.turn > 0:
                self.engine.undo()
                self.turn -= 1
                self.engine.won = False
                self._shared["destroyed"] = self._status_stack.pop()
            after = self._snapshot()
            events, phase = self._diff_events(before, after)
            anim = events
        else:
            key = ACTIONS.get(action)
            if key is None:
                raise ValueError(f"unknown action {action!r}")
            if before["status"] != "playing":
                raise RuntimeError(f"level is over ({before['status']}); only undo/restart are possible")
            self._shared["log"].clear()
            self._shared["names"].clear()
            self._status_stack.append(self._shared["destroyed"])
            self.engine.move(key)
            self.turn += 1
            after = self._snapshot()
            events, phase = self._events(before, after, self._shared["log"])
            anim = self._events(before, after, self._shared["log"], full=True)[0]
            action = ACTION_NAMES[key]
        events += self._meta_events(before, after, phase)
        self.last = after
        result = {"action": action, "events": events, "state": self._state(after)}
        self._anim = (before, after, anim)  # for the renderer
        return result

    def play(self, actions, max_actions: int | None = 32, stop_on=("win", "infinite_loop")) -> dict:
        """Several actions in one call; stops early on the conditions in `stop_on`."""
        actions = [ACTION_NAMES.get(ACTIONS.get(a, a), a) for a in actions]
        if max_actions is not None and len(actions) > max_actions:
            raise ValueError(f"at most {max_actions} actions per call")
        steps, stopped = [], None
        for a in actions:
            before = self.last
            r = self.step(a)
            steps.append({"action": r["action"], "events": r["events"]})
            st = r["state"]["status"]
            reason = {"won": "win"}.get(st, st)
            if reason != "playing" and reason in stop_on:
                stopped = reason
            elif "no_op" in stop_on and not r["events"]:
                stopped = "no_op"
            elif "rule_change" in stop_on and before["rules"] != self.last["rules"]:
                stopped = "rule_change"
            elif "no_you" in stop_on and self.engine.G["generaldata2"]["values"][self.engine.G["NOPLAYER"]] == 1:
                stopped = "no_you"
            if stopped or st != "playing":
                break
        return {"actions": actions, "executed": len(steps), "stopped_by": stopped, "steps": steps,
                "state": self._state(self.last)}

    def undo(self, n: int = 1) -> dict:
        r = None
        for _ in range(n):
            r = self.step("undo")
        return r

