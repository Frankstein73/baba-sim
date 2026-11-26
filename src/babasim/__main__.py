"""Command line: play a level from a move string or interactively.

    python -m babasim 0level --moves rrrrrrrr
    python -m babasim 0level                      # interactive: r/u/l/d/w, z = undo, x = restart, q
    python -m babasim 245level --rules list --png out.png --gif last_move.gif
    python -m babasim --list [world]
"""

from __future__ import annotations

import argparse
import json
import sys

from babasim.api import Game
from babasim.runtime import level_name, list_levels
from babasim.text import format_state, format_step

KEYS = {"r": "right", "u": "up", "l": "left", "d": "down", "w": "wait", "z": "undo", "x": "restart"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="babasim", description=__doc__.splitlines()[0])
    ap.add_argument("level", nargs="?", help="level name or file stem, e.g. \"baba is you\" or 0level")
    ap.add_argument("--world", default="baba")
    ap.add_argument("--list", action="store_true", help="list levels of the world and exit")
    ap.add_argument("--moves", help="string of r/u/l/d/w/z/x")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rules", choices=["none", "lit", "list"], default="lit")
    ap.add_argument("--view", choices=["perceptual", "full"], default="perceptual")
    ap.add_argument("--json", action="store_true", help="print StepResult JSON lines instead of text")
    ap.add_argument("--grid", action="store_true", help="add the character grid to text output")
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--png", help="write the final state image")
    ap.add_argument("--gif", help="write an animation of the last move")
    a = ap.parse_args(argv)

    if a.list or not a.level:
        for p in list_levels(a.world):
            print(f"{p.stem}\t{level_name(a.world, p.stem)}")
        return 0

    g = Game(a.level, a.world, a.seed, a.rules, a.view)
    state = g.observe()
    print(json.dumps(state, ensure_ascii=False) if a.json else format_state(state, a.grid, a.lang))

    def run(keys):
        nonlocal state
        for k in keys:
            if k not in KEYS:
                print(f"unknown key {k!r}", file=sys.stderr)
                continue
            try:
                r = g.step(KEYS[k])
            except RuntimeError as e:
                print(e, file=sys.stderr)
                return
            print(json.dumps(r, ensure_ascii=False) if a.json else "\n" + format_step(r, state, a.grid, a.lang))
            state = r["state"]

    if a.moves is not None:
        run(a.moves)
    else:
        while True:
            try:
                line = input("> ").strip()
            except EOFError:
                break
            if line == "q":
                break
            run(line)
    if a.png or a.gif:
        from babasim.render import Renderer

        r = Renderer(g)
        if a.png:
            r.state_image().save(a.png)
        if a.gif:
            r.save_gif(a.gif)
    return 0 if g.status == "won" else 1


if __name__ == "__main__":
    sys.exit(main())
