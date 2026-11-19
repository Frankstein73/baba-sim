"""Replay known move-string solutions (baba-is-harbor tasks/*/solution/solve.sh) in the oracle."""

import json
import re
import sys
from pathlib import Path

from oracle import Oracle

ref = Path(sys.argv[1])
levels = json.loads((ref / "level_map.json").read_text())["levels"]
o = Oracle()
ok = bad = 0
for task, info in sorted(levels.items()):
    sh = ref / "tasks" / task / "solution" / "solve.sh"
    if not sh.exists():
        continue
    m = max(re.findall(r"[lrudpw]{4,}", sh.read_text()), key=len, default=None)
    if m is None:
        continue
    o.load(info["file"])
    for i, ch in enumerate(m):
        o.move("w" if ch == "p" else ch)
        if o.won:
            break
    ok += o.won
    bad += not o.won
    if not o.won:
        print("NOT WON", task, info["file"], len(m))
print(f"won {ok}, not won {bad}")
