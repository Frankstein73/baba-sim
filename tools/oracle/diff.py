"""Differential test: translated Python engine vs the original Lua oracle, step by step.

    python tools/oracle/diff.py [world] [moves_per_level] [seed] [stem ...]
"""

import random
import sys
import time
from collections import Counter

from oracle import GAME, Oracle

from babasim.runtime import Engine

world = sys.argv[1] if len(sys.argv) > 1 else "baba"
nmoves = int(sys.argv[2]) if len(sys.argv) > 2 else 40
seed = sys.argv[3] if len(sys.argv) > 3 else "0"
stems = sys.argv[4:] or sorted(p.stem for p in (GAME / "Worlds" / world).glob("*.l"))

o, e = Oracle(world), Engine(world)
bad = {}
soft = {}
t_o = t_e = 0.0
steps = 0
order_only = 0
for stem in stems:
    rng = random.Random(f"{seed}:{stem}")
    try:
        o.load(stem)
        e.load(stem)
        hist = ""
        for i in range(nmoves + 1):
            so, se = o.state(), e.state()
            if so != se or sorted(o.rules()) != sorted(e.rules()) or o.won != e.won:
                what = "state" if so != se else ("rules" if sorted(o.rules()) != sorted(e.rules()) else "won")
                detail = ""
                noid = lambda st: sorted((u[:4] + u[5:] for u in st), key=str)  # noqa: E731
                if what == "state" and noid(so) == noid(se):
                    # same objects, different creation order / ids: the Lua side iterated a
                    # string-keyed table, whose order is random per run in the game itself
                    soft[stem] = hist
                    break
                if what == "state":
                    if len(so) != len(se):
                        detail = f"units {len(so)} vs {len(se)}"
                    else:
                        j = next(j for j in range(len(so)) if so[j] != se[j])
                        detail = f"#{j} lua={so[j]} py={se[j]}"
                elif what == "rules":
                    ro, re_ = o.rules(), e.rules()
                    detail = f"lua-only={[r for r in ro if r not in re_][:3]} py-only={[r for r in re_ if r not in ro][:3]}"
                    if not (set(ro) ^ set(re_)):
                        detail = "same set, different order"
                bad[stem] = f"{what} after {hist!r}: {detail}"
                break
            order_only += o.rules() != e.rules()
            if i == nmoves:
                break
            k = rng.choice("rrrruuuullllddddwz")
            hist += k
            t = time.perf_counter()
            o.undo() if k == "z" else o.move(k)
            t_o += time.perf_counter() - t
            t = time.perf_counter()
            e.undo() if k == "z" else e.move(k)
            t_e += time.perf_counter() - t
            steps += 1
    except Exception as ex:  # noqa: BLE001
        bad[stem] = f"EXC {type(ex).__name__}: {str(ex).splitlines()[0][:200]}"
        o, e = Oracle(world), Engine(world)
print(f"{len(stems)} levels, {steps} steps, {len(bad)} diverged; lua {t_o:.1f}s, py {t_e:.1f}s; "
      f"{order_only} steps with same rules in a different order (Lua hash order, random per run)")
print(f"{len(soft)} levels stopped early on unit-order-only differences (Lua hash order): {list(soft)[:8]}")
kinds = Counter(v.split(" after")[0].split(":")[0] for v in bad.values())
print(kinds.most_common())
for stem, msg in list(bad.items())[:25]:
    print(" ", stem, msg[:330])
