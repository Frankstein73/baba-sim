"""Write a JSON Lines dataset of levels: one row per level with the prompt and the starting position.

    python -m babasim.dataset baba30.jsonl --max-calls 80

The rows are what a model is shown before its first tool call; the options here must match the ones
the playing session is opened with (the prompt states the limits).
"""

from __future__ import annotations

import argparse
import json

from babasim.runtime import DATA
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


def main_all() -> tuple[str, ...]:
    """Every playable level of the main game (217), in the order of the game's areas."""
    return tuple(each["level"] for each in json.loads((DATA / "campaign_baba.json").read_text())["levels"])


def rows(levels=MAIN_30, world: str = "baba", **options):
    for order, level in enumerate(levels, 1):
        s = Session(level, world, **options)
        title = json.loads((DATA / "levels" / world / f"{level}.json").read_text())["ld"].get("general", {}).get("name", "")
        yield {"id": f"{world}:{level}", "order": order, "world": world, "level": level, "title": title,
               "prompt": s.system_prompt(), "initial_state": s.initial_observation()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("out")
    ap.add_argument("--world", default="baba")
    ap.add_argument("--levels", nargs="*", help="level stems (default: the 30 main-game levels)")
    ap.add_argument("--all", action="store_true", help="every playable level of the main game (217)")
    ap.add_argument("--rules", choices=["none", "lit", "list"], default="lit")
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--max-calls", type=int)
    ap.add_argument("--max-steps", type=int)
    a = ap.parse_args()
    n = 0
    with open(a.out, "w") as f:
        for row in rows(a.levels or (main_all() if a.all else MAIN_30), a.world, rules=a.rules, lang=a.lang, max_calls=a.max_calls,
                        max_steps=a.max_steps):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    print(f"{n} rows -> {a.out}")


if __name__ == "__main__":
    main()
