"""LuaTable must iterate and measure integer-keyed tables exactly like Lua 5.3 (ltable.c)."""

import random

import pytest

from babasim.luart import L_insert, L_len, L_pairs, L_remove, LuaTable

lupa = pytest.importorskip("lupa.lua53")


def test_pairs_order_and_length_match_lua():
    lua = lupa.LuaRuntime()
    for trial in range(1500):
        rng = random.Random(trial)
        span = rng.choice([8, 40, 300, 5000])
        src = ["local t={}"]
        t = LuaTable()
        for _ in range(rng.randint(1, 60)):
            r = rng.random()
            if r < 0.8:
                k, v = rng.randint(-2, span), r < 0.55
                src.append(f"t[{k}]={'true' if v else 'nil'}")
                t[k] = True if v else None
            elif r < 0.9:
                src.append("table.insert(t,true)")
                L_insert(t, True)
            else:
                src.append("table.remove(t)")
                L_remove(t)
        src.append("local o={} for k in pairs(t) do o[#o+1]=k end return table.concat(o,',')..'#'..#t")
        want = lua.execute("\n".join(src))
        got = ",".join(str(k) for k, _ in L_pairs(t)) + "#" + str(L_len(t))
        assert got == want, src
