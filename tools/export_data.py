"""One-time export of the game's data into repo-owned JSON under data/.

Raw, lossless dump: object tables from values.lua / editor_objectlist.lua, and every level's
layers (tile code + direction per occupied cell) plus its .ld sections. Interpreting tile codes
and applying per-level [tiles] changes is the engine loader's job, not this script's.

    uv run python tools/export_data.py [GAME_DATA_DIR]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from lupa import lua51

from babasim.levelfile import EMPTY, read_l, read_ld

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "babasim" / "data"


def lua_to_py(v):
    if lua51.lua_type(v) != "table":
        return v
    keys = list(v.keys())
    if keys and all(isinstance(k, int) for k in keys) and sorted(keys) == list(range(1, len(keys) + 1)):
        return [lua_to_py(v[k]) for k in sorted(keys)]
    return {str(k): lua_to_py(v[k]) for k in keys}


def export_objects(game: Path) -> None:
    lua = lua51.LuaRuntime()
    lua.execute((game / "values.lua").read_text())
    lua.execute((game / "Editor/editor_objectlist.lua").read_text())
    g = lua.globals()
    out = {
        "tileslist": lua_to_py(g.tileslist),
        "editor_objlist": lua_to_py(g.editor_objlist),
    }
    (OUT / "objects.json").write_text(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False))
    print(f"objects: {len(out['tileslist'])} tileslist, {len(out['editor_objlist'])} editor objects")


def export_levels(game: Path) -> None:
    n = 0
    for lpath in sorted((game / "Worlds").glob("*/*.l")):
        world, stem = lpath.parent.name, lpath.stem
        layers = []
        for layer in read_l(lpath):
            cells = []
            for i, code in enumerate(layer.tiles):
                if code == EMPTY:
                    continue
                d = layer.dirs[i] if layer.dirs is not None else None
                cells.append([i % layer.width, i // layer.width, code & 0xFF, code >> 8, d])
            layers.append({
                "width": layer.width,
                "height": layer.height,
                "header": layer.header.hex(),
                "has_dirs": layer.dirs is not None,
                "cells": cells,  # [x, y, tile_col, tile_row, dir]
            })
        ldpath = lpath.with_suffix(".ld")
        level = {
            "world": world,
            "stem": stem,
            "layers": layers,
            "ld": read_ld(ldpath) if ldpath.exists() else {},
        }
        dest = OUT / "levels" / world / f"{stem}.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(level, separators=(",", ":"), ensure_ascii=False))
        n += 1
    print(f"levels: {n}")


def main() -> None:
    game = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "game"
    OUT.mkdir(exist_ok=True)
    export_objects(game)
    export_levels(game)


if __name__ == "__main__":
    main()
