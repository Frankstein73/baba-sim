"""Native side of the game re-implemented in Python: objects, tilemap, MF_* functions and the
order in which the engine calls into the translated logic (re/NATIVE_TURN_LOOP.md)."""

from __future__ import annotations

import importlib
import json
import math
import sys
from pathlib import Path

from babasim import gen
from babasim.luart import DefTable, LuaTable, L_ipairs, L_lib, L_noop

DATA = Path(__file__).resolve().parent / "data"
KEYS = {"r": "right", "u": "up", "l": "left", "d": "down", "w": "idle"}

sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))


class Globals(dict):
    """Lua global table: unknown names are nil; unknown MF_* natives (audio/visual) are no-ops."""

    def __missing__(self, k):
        if k.__class__ is str and k.startswith("MF_"):
            return L_noop
        return None


class Rand:
    """C rand()/srand() as used by Lua's math.random in the shipped build (see set_libc)."""

    def __init__(self):
        self.state = 1

    def seed(self, n=0, *_):
        self.state = int(n) & 0xFFFFFFFF
        self.next()  # Lua 5.3 discards the first value after seeding

    def next(self):
        # macOS libc: Park–Miller minimal standard via Schrage's method, 0 seed remapped
        x = self.state % 0x7FFFFFFF or 123459876
        hi, lo = divmod(x, 127773)
        x = 16807 * lo - 2836 * hi
        if x < 0:
            x += 0x7FFFFFFF
        self.state = x
        return x & 0x7FFFFFFF

    def random(self, m=None, n=None, *_):
        r = self.next() * (1.0 / (0x7FFFFFFF + 1.0))
        if m is None:
            return r
        low, up = (1, m) if n is None else (m, n)
        return int(r * (float(up - low) + 1.0)) + low


def _table(d):
    return LuaTable(None, dict(d))


class Engine:
    def __init__(self, world: str = "baba"):
        self.world = world
        self.objs: dict[int, LuaTable] = {}
        self.nextfixed = 0
        self.won = False
        self.tiles: dict[tuple, tuple] = {}
        self.ld: dict = {}
        self.rand = Rand()
        G = self.G = Globals()
        G["_G"] = G
        G["math"] = _table({"random": self.rand.random, "randomseed": self.rand.seed, "pi": math.pi,
                            "huge": math.inf, **{k[5:]: v for k, v in L_lib.items() if k.startswith("math.")}})
        G["string"] = _table({k[7:]: v for k, v in L_lib.items() if k.startswith("string.")})
        G["table"] = _table({k[6:]: v for k, v in L_lib.items() if k.startswith("table.")})
        for k, v in L_lib.items():
            if "." not in k:
                G[k] = v
        self._natives()
        for name in gen.MODULES:
            importlib.import_module(f"babasim.gen.{name}").load(G)
        for name in gen.UI_STUBS:  # menus, text rendering, cutscenes
            G.setdefault(name, L_noop)
        G["langtext"] = lambda *_: ""
        self._boot()

    # ---- native objects ----------------------------------------------------------------
    def newobj(self, cls):
        self.nextfixed += 1
        fixed = self.nextfixed
        obj = LuaTable(None, {
            "values": DefTable(0), "strings": DefTable(""), "flags": DefTable(False), "fixed": fixed,
            "className": cls, "x": 0, "y": 0, "visible": True, "layer": 1, "scaleX": 1, "scaleY": 1,
            "angle": 0, "direction": 0, "colour": LuaTable(),
        })
        self.objs[fixed] = obj
        return obj

    def _natives(self):
        G = self.G
        objs = self.objs

        def new_object(fixed=None, *_):
            return objs.get(fixed)

        G["mmf"] = _table({"newObject": new_object})

        def layer(l):
            def get_x(_self, x, y, *_):
                t = self.tiles.get((l, x, y))
                return t[0] if t else 255

            def get_y(_self, x, y, *_):
                t = self.tiles.get((l, x, y))
                return t[1] if t else 255

            return _table({"get_x": get_x, "get_y": get_y, "set_x": L_noop, "set_tile": L_noop,
                           "unset_tile": L_noop})

        tilemap = LuaTable(None, {i: layer(i) for i in range(3)})
        G["TileMap"] = _table({"new": lambda *_: tilemap})

        def create(cls=None, *_):
            obj = self.newobj(cls)
            obj["values"][G["ID"]] = -1
            return obj["fixed"]

        def emptycreate(cls=None, x=None, y=None, *_):
            fixed = create(cls)
            G["setundo"](1)
            return fixed

        def remove(fixed=None, *_):
            objs.pop(fixed, None)
            G["setundo"](1)

        def cleanremove(fixed=None, *_):
            obj = objs.pop(fixed, None)
            if obj is not None:
                obj["flags"][G["DEAD"]] = True

        def getfixed(id=None, *_):
            ID, DEAD = G["ID"], G["DEAD"]
            for _i, unit in L_ipairs(G["units"]):
                if unit["values"][ID] == id and unit["flags"][DEAD] is False:
                    return unit["fixed"]
            return None

        def win(*_):
            self.won = True

        def parsestring(s=None, *_):
            return LuaTable([p for p in (s or "").split(",") if p])

        def read(file=None, section=None, key=None, *_):
            if file == "level":
                return self.ld.get(section, {}).get(key, "")
            return ""

        empty = lambda *_: LuaTable()  # noqa: E731
        G.update({
            "MF_create": create, "MF_emptycreate": emptycreate, "MF_specialcreate": create,
            "MF_effectcreate": create, "MF_remove": remove, "MF_specialremove": remove,
            "MF_cleanremove": cleanremove, "MF_getfixed": getfixed,
            "MF_findfixed": lambda fixed=None, *_: fixed if fixed in objs else None,
            "MF_totalunitcount": lambda *_: len(G["units"].arr),
            "MF_getunits": lambda *_: LuaTable([u["fixed"] for u in G["units"].arr]),
            "MF_win": win, "MF_random": self.rand.random, "MF_parsestring": parsestring,
            "MF_read": read, "MF_update": lambda *_: self.turngroup(1), "MF_findpaths": empty,
            "MF_findgates": empty, "MF_findlevelunit": empty,
            "fixed_to_str": L_lib["tostring"],
        })

    def _boot(self):
        G = self.G
        ids = [self.newobj("data")["fixed"] for _ in range(14)]
        G["init"](0, 35, 20, 24, 0, 0, *ids[:7], 854, 480)
        G["setupmenu"](*ids[7:13], True)
        G["generaldata"]["strings"][G["WORLD"]] = self.world
        G["generaldata"]["strings"][G["BASEWORLD"]] = "baba"
        G["generaldata"]["values"][G["MODE"]] = 0
        G["spritedata"]["values"][G["TILEMULT"]] = 1
        G["generaldata2"]["values"][G["ZOOM"]] = 1
        G["editor"]["strings"][G["MENU"]] = "ingame"
        G["worldinit"]()

    # ---- level start (FUN_1001b9e60) -----------------------------------------------------
    def load(self, stem: str, world: str | None = None, seed: int = 0) -> None:
        level = json.loads((DATA / "levels" / (world or self.world) / f"{stem}.json").read_text())
        self.load_level(stem, level["layers"], level["ld"], seed)

    def load_level(self, name: str, layers: list, ld: dict, seed: int = 0) -> None:
        """`seed` drives math.random; the game leaves it unseeded (shared libc state), so any
        value is a legitimate play-through."""
        G = self.G
        self.rand.seed(seed)
        self.won = False
        self.tiles.clear()
        self.ld = ld
        G["clearunits"]()
        G["clear"]()
        seeding = ld.get("general", {}).get("seeding", "")
        G["setseedingtype"](int(seeding) if seeding.lstrip("-").isdigit() else 0)
        w, h = layers[0]["width"], layers[0]["height"]
        gd = G["generaldata"]
        gd["strings"][G["CURRLEVEL"]] = name
        gd["values"][G["ROOMSIZEX"]] = w
        gd["values"][G["ROOMSIZEY"]] = h
        G["roomsizex"], G["roomsizey"] = w, h
        custom = ld.get("general", {}).get("customobjects", "")
        if custom:
            G["loadcustomobjects"](custom)
        # FUN_1001ab590: every object the level redefines (name, sprite, colour, word type...) is created once
        # so that addchange() reads its [tiles] entries into `changes`; without it a renamed tile keeps the
        # default meaning of its object slot.
        tiles = ld.get("tiles", {})
        G["restoredefaults"]()
        if tiles.get("changed"):
            count = tiles.get("changed_count", "")
            lists = ["changed"] + [f"changed{i}" for i in range(2, (int(count) if count.isdigit() else 1) + 1)]
            for target in ",".join(tiles.get(key, "") for key in lists).split(","):
                if target in G["tileslist"].hash:
                    fixed = G["MF_create"](target)
                    G["addchange"](fixed)
                    G["MF_cleanremove"](fixed)
            G["handleobjectchanges"]()

        cells = sorted((x, y, li, tx, ty, d or 0)
                       for li, layer in enumerate(layers) for x, y, tx, ty, d in layer["cells"])
        V = {k: G[k] for k in ("ID", "XPOS", "YPOS", "DIR", "ONLINE")}
        for x, y, li, tx, ty, d in cells:  # x-major, then y, then layer
            if tx > 0 or ty > 0:
                obj = self.newobj(G["loadtile"](tx, ty))
                vals = obj["values"]
                vals[V["ID"]] = -1
                vals[V["XPOS"]] = x
                vals[V["YPOS"]] = y
                vals[V["DIR"]] = d
                vals[V["ONLINE"]] = 1
                obj["flags"][9] = True
                G["addunit"](obj["fixed"], None, True)
            else:
                self.tiles[(li, x, y)] = (tx, ty)

        # FUN_1001b1dc0: seed text is CURRLEVEL .. LEVELNAME
        gd["strings"][G["LEVELNAME"]] = ld.get("general", {}).get("name", "")
        G["setfixedrandom"](name + gd["strings"][G["LEVELNAME"]])
        try:
            G["overrideundoseeding"]()
        except TypeError:
            pass  # no undo entry yet: the Lua call errors and the engine carries on

        G["code"]()
        G["undostate"](False)
        G["startblock"]()
        G["animate"]()
        G["clear"]()
        G["undostate"](True)
        G["code"]()
        G["do_mod_hook"]("level_start")

    # ---- turn group (FUN_1001cf610) ------------------------------------------------------
    def turngroup(self, v: int) -> None:
        G = self.G
        gd = G["generaldata"]["values"]
        UPDATE = G["UPDATE"]
        gd[UPDATE] = v
        G["doupdate"](); G["smallclear"](); G["setunitmap"]()
        G["code"]()
        if v == 1:
            G["updateeffecthistory"](); G["fallblock"](); G["doupdate"](); G["code"]()
            G["statusblock"](); G["domaprotation"]()
            G["conversion"](True); G["fallblock"]()
        else:
            G["reseteffecthistory"](); G["statusblock"](None, True)
        G["doupdate"](); G["code"]()
        if v == 1:
            G["levelblock"](); G["block"](); G["dolevelconversions"]()
        CONVERTED = G["CONVERTED"]
        units = G["units"].arr
        for unit in units:
            unit["flags"][CONVERTED] = False
        G["doupdate"](); G["smallclear"](); G["setunitmap"]()
        G["code"](); G["findplayer"](v); G["checkturnsound"]()
        G["effectblock"](); G["diceblock"]()
        if v == 1:
            G["shorteffectblock"](); G["groupcheck"](); G["destroylevel_do"]()
        G["update_cleanup"]()
        if v == 1:
            MOVED, PUSHED = G["MOVED"], G["PUSHED"]
            for unit in G["units"].arr:
                vals = unit["values"]
                vals[MOVED] = max(0, vals[MOVED] - 1)
                vals[PUSHED] = 4
            gd[UPDATE] = 0
            G["newundo"](); G["animate"](); G["cleanup"](); G["do_mod_hook"]("turn_end")
        else:
            gd[UPDATE] = 0
            G["animate"](); G["cleanup"]()

    # ---- input ---------------------------------------------------------------------------
    def move(self, key: str) -> None:
        self.G["command"](KEYS[key], 1)

    def undo(self) -> None:
        self.G["dolog"]("undo")
        self.G["undo"]()
        self.turngroup(2)

    # ---- inspection ----------------------------------------------------------------------
    def state(self) -> list[tuple]:
        G = self.G
        out = []
        for u in G["units"].arr:
            v, s = u["values"], u["strings"]
            out.append((s[G["UNITNAME"]], v[G["XPOS"]], v[G["YPOS"]], v[G["DIR"]], v[G["ID"]],
                        v[G["FLOAT"]], s[G["UNITTYPE"]], u["className"], v[G["ZLAYER"]]))
        return out

    def rules(self) -> list[tuple]:
        out = []
        for f in self.G["features"].arr:
            r = f[1]
            conds = ",".join(str(c[1]) for c in (f[2].arr if f[2] is not None else []))
            out.append((r[1], r[2], r[3], conds))
        return out
