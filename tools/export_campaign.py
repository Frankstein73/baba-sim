"""Write data/campaign_<world>.json for level packs: the playable levels of a world, under their in-game names.

A pack's levels are found from the map its world_data.txt starts on: a level that lists other levels is a
map and is followed, any other level is playable. Order is breadth-first, so the levels of the first map come
first. A name that occurs twice in a world gets its map's name appended; names are what a level is asked for by.

    uv run python tools/export_campaign.py packs            # every world under packs/Worlds
    uv run python tools/export_campaign.py --names baba     # only (re)write the names of an existing campaign
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

from babasim.levelfile import read_ld

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "babasim" / "data"


def general(world: str, stem: str) -> tuple[dict, dict]:
    ld = json.loads((DATA / "levels" / world / f"{stem}.json").read_text())["ld"]
    return ld.get("general", {}), ld.get("levels", {})


def playable(world: str, start: str) -> list[dict]:
    seen, out, queue = {start}, [], collections.deque([(start, "")])
    while queue:
        stem, area = queue.popleft()
        if not (DATA / "levels" / world / f"{stem}.json").is_file():
            continue  # a map entry whose level file the pack does not ship
        g, listed = general(world, stem)
        count = g.get("levels", "0")
        inner = [listed.get(f"{i}file") for i in range(int(count) if count.isdigit() else 0)]
        if any(inner):
            for each in inner:
                if each and each not in seen:
                    seen.add(each)
                    queue.append((each, g.get("name", "")))
        else:
            out.append({"level": stem, "area": area})
    return out


def named(world: str, levels: list[dict]) -> list[dict]:
    """The entries with a `name` each: the in-game name, made unique within the world."""
    names = [general(world, each["level"])[0].get("name", "").strip() or each["level"] for each in levels]
    twice = {name for name, n in collections.Counter(name.casefold() for name in names).items() if n > 1}
    out, used = [], set()
    for each, name in zip(levels, names):
        if name.casefold() in twice:
            name = f"{name} ({each['area']})"
        base, n = name, 1
        while name.casefold() in used:
            n += 1
            name = f"{base} #{n}"
        used.add(name.casefold())
        out.append({"name": name, **{k: v for k, v in each.items() if k != "name"}})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("packs", nargs="?", help="directory holding Worlds/<world>/world_data.txt of each pack")
    ap.add_argument("--names", nargs="*", default=[], metavar="WORLD", help="rewrite the names of these campaigns")
    a = ap.parse_args()
    for world in a.names:
        path = DATA / f"campaign_{world}.json"
        campaign = json.loads(path.read_text())
        campaign["levels"] = named(world, campaign["levels"])
        path.write_text(json.dumps(campaign, indent=1, ensure_ascii=False) + "\n")
        print(f"{world}: {len(campaign['levels'])} names")
    for data in sorted(Path(a.packs).glob("Worlds/*/world_data.txt")) if a.packs else ():
        world, info = data.parent.name, read_ld(data).get("general", {})
        levels = named(world, playable(world, info["start"]))
        note = "Playable levels reachable from the pack's starting map, breadth-first (tools/export_campaign.py)."
        campaign = {"_note": note, "title": re.sub(r"\$\d+,\d+\s*", "", info.get("name", world)), "author": info.get("author", ""), "levels": levels}
        (DATA / f"campaign_{world}.json").write_text(json.dumps(campaign, indent=1, ensure_ascii=False) + "\n")
        print(f"{world}: {len(levels)} levels")


if __name__ == "__main__":
    main()
