"""Load every level of a world in the oracle and play random moves; report Lua errors."""

import random
import sys
import traceback
from collections import Counter
from pathlib import Path

from oracle import GAME, Oracle

world = sys.argv[1] if len(sys.argv) > 1 else "baba"
nmoves = int(sys.argv[2]) if len(sys.argv) > 2 else 30
stems = sorted(p.stem for p in (GAME / "Worlds" / world).glob("*.l"))
o = Oracle(world)
errors, missing, alerts = {}, Counter(), Counter()
for stem in stems:
    rng = random.Random(stem)
    try:
        o.load(stem)
        for _ in range(nmoves):
            k = rng.choice("rrrruuuullllddddwz")
            o.undo() if k == "z" else o.move(k)
    except Exception as e:  # noqa: BLE001
        errors[stem] = str(e).splitlines()[0][:300]
        o = Oracle(world)
    alerts.update(o.g.ORACLE.alerts.values())
    o.g.ORACLE.alerts = o.lua.table()
missing.update(dict(o.g.ORACLE.missing))
print(f"{len(stems)} levels, {len(errors)} with errors")
for msg, n in Counter(errors.values()).most_common(15):
    print(n, msg, [s for s, m in errors.items() if m == msg][:4])
print("alerts:", alerts.most_common(8))
print("stubbed:", sorted(missing))
