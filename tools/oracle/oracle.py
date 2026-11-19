"""Dev-only oracle: runs the original game Lua headless via lupa (see shim.lua).

Needs the installed game (BABA_DATA or ./game). Used to generate/verify traces for the port;
the engine itself never imports this.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from lupa import lua53

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from babasim.levelfile import EMPTY, read_l, read_ld  # noqa: E402

GAME = Path(os.environ.get("BABA_DATA", ROOT / "game"))
FILES = [
    "constants.lua", "colours.lua", "values.lua", "metadata.lua", "tools.lua", "conditions.lua",
    "rules.lua", "movement.lua", "blocks.lua", "effects.lua", "features.lua", "syntax.lua",
    "vision.lua", "update.lua", "load.lua", "convert.lua", "undo.lua", "clears.lua",
    "Editor/editor_constants.lua", "Editor/editor_objectlist.lua", "changes.lua",
    "letterunits.lua", "map.lua", "mapcursor.lua", "dynamictiling.lua", "modsupport.lua",
    "ending.lua", "menu.lua", "utf_decoder.lua",
]
KEYS = {"r": "right", "u": "up", "l": "left", "d": "down", "w": "idle"}


class Oracle:
    def __init__(self, world: str = "baba"):
        self.world = world
        self.lua = lua53.LuaRuntime(unpack_returned_tuples=True)
        g = self.lua.globals()
        g.ORACLE_GAME = str(GAME)
        g.ORACLE_FILES = self.lua.table_from(FILES)
        self.lua.execute((Path(__file__).parent / "shim.lua").read_text())
        self.g = g
        self._set_ini("world", read_ld(GAME / "Worlds" / world / "world_data.txt"))
        g.ORACLE_boot(world)

    def _set_ini(self, slot: str, ini: dict) -> None:
        self.g.ORACLE[slot] = self.lua.table_from(
            {s: self.lua.table_from(kv) for s, kv in ini.items()})

    def load(self, stem: str, seed: int = 0) -> None:
        self.g.ORACLE_seed(seed)
        base = GAME / "Worlds" / self.world / stem
        self._set_ini("ld", read_ld(base.with_suffix(".ld")))
        layers = read_l(base.with_suffix(".l"))
        cells = []
        for li, layer in enumerate(layers):
            for i, code in enumerate(layer.tiles):
                if code == EMPTY:
                    continue
                d = layer.dirs[i] if layer.dirs is not None else 0
                cells.append(self.lua.table_from(
                    [i % layer.width, i // layer.width, li, code & 0xFF, code >> 8, d]))
        self.g.ORACLE_loadlevel(self.lua.table_from({
            "name": stem, "width": layers[0].width, "height": layers[0].height,
            "cells": self.lua.table_from(cells)}))

    def move(self, key: str) -> None:
        self.g.ORACLE_command(KEYS[key])

    def undo(self) -> None:
        self.g.ORACLE_undo()

    @property
    def won(self) -> bool:
        return bool(self.g.ORACLE.won)

    def state(self) -> list[tuple]:
        return [tuple(u.values()) for u in self.g.ORACLE_state().values()]

    def rules(self) -> list[tuple]:
        return [tuple(r.values()) for r in self.g.ORACLE_rules().values()]

    def text(self) -> str:
        w, h = int(self.g.roomsizex), int(self.g.roomsizey)
        grid = [["." for _ in range(w)] for _ in range(h)]
        for name, x, y, *_ in sorted(self.state(), key=lambda u: u[8]):  # topmost z-layer wins
            if 0 <= x < w and 0 <= y < h:
                grid[y][x] = name[5].upper() if name.startswith("text_") else name[0]
        return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    o = Oracle()
    o.load(sys.argv[1] if len(sys.argv) > 1 else "0level")
    for ch in sys.argv[2] if len(sys.argv) > 2 else "":
        o.undo() if ch == "z" else o.move(ch)
    print(o.text())
    print("rules:", [" ".join(r[:3]) for r in o.rules()])
    print("won:", o.won, "units:", len(o.state()))
    print("alerts:", list(o.g.ORACLE.alerts.values())[:10])
    print("stubbed natives:", dict(o.g.ORACLE.missing))
