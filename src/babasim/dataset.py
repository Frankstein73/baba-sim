"""Write a JSON Lines dataset of levels: one row per level with the prompt and the starting position.

    python -m babasim.dataset baba30.jsonl --max-calls 80

The rows are what a model is shown before its first tool call; the options here must match the ones
the playing session is opened with (the starting position states the calls that are left). Each row
also carries a picture of the starting position, `initial_image`, as a PNG data URL, and the whole task
as one Markdown text, `problem_statement`: the prompt, that picture and the starting position. A viewer
of the stored instances shows the latter as the task.
"""

from __future__ import annotations

import argparse
import base64
import io
import json

from babasim.runtime import campaign
from babasim.session import Session

# Thirty levels of the main game ("baba" world) in the order the game presents them, easiest first.
MAIN_30 = (
    *("0level", "1level", "189level", "3level", "2level", "90level", "5level", "6level"),  # opening area
    *("20level", "10level", "4level", "93level", "209level", "15level"),  # the lake
    *("205level", "218level", "171level", "172level", "107level"),  # solitary island
    *("199level", "52level", "58level", "33level"),  # temple ruins
    *("238level", "221level", "235level"),  # forest of fall
    *("66level", "246level"),  # deep forest
    *("9level", "59level"),  # rocket trip, flower garden
)


def world_all(world: str = "baba") -> tuple[str, ...]:
    """Every playable level of a world by name, in playing order: the 217 of the main game, or a pack's."""
    return tuple(each["name"] for each in campaign(world))


def picture(session: Session, tile_px: int) -> str:
    """The session's current state drawn as a PNG data URL."""
    from babasim.render import Renderer

    buf = io.BytesIO()
    Renderer(session.game, tile_px=tile_px).state_image().save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def rows(levels=MAIN_30, world: str = "baba", images: bool = True, tile_px: int = 48, **options):
    for order, level in enumerate(levels, 1):
        s = Session(level, world, **options)
        name = s.game.level  # the in-game name, unique in the world; `file` is the level file it comes from
        row = {"id": f"{world}:{name}", "order": order, "world": world, "level": name, "file": s.game.file,
               "prompt": s.system_prompt(), "initial_state": s.initial_observation()}
        shown = [row["prompt"]]
        if images:
            row["initial_image"] = picture(s, tile_px)
            shown.append(f"![starting position]({row['initial_image']})")
        if isinstance(row["initial_state"], str):
            shown.append(f"```\n{row['initial_state']}\n```")
        row["problem_statement"] = "\n\n".join(shown)
        yield row


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("out")
    ap.add_argument("--world", default="baba")
    ap.add_argument("--levels", nargs="*", help="level names or file stems (default: the 30 main-game levels; all of another world)")
    ap.add_argument("--all", action="store_true", help="every playable level of the world: the 217 of the main game, or a pack's")
    ap.add_argument("--rules", choices=["none", "lit", "list"], default="lit")
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--max-calls", type=int)
    ap.add_argument("--max-steps", type=int)
    ap.add_argument("--no-images", action="store_true", help="leave out the picture of the starting position")
    ap.add_argument("--tile-px", type=int, default=48, help="size of a grid cell in the picture")
    a = ap.parse_args()
    n = 0
    with open(a.out, "w") as f:
        for row in rows(a.levels or (world_all(a.world) if a.all or a.world != "baba" else MAIN_30), a.world, images=not a.no_images, tile_px=a.tile_px, rules=a.rules, lang=a.lang,
                        max_calls=a.max_calls, max_steps=a.max_steps):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    print(f"{n} rows -> {a.out}")


if __name__ == "__main__":
    main()
