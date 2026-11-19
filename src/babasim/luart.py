"""Lua 5.3 value semantics for the transpiled game logic (see tools/lua2py.py).

Only what the game's Lua actually uses is implemented. nil is None; a Lua function returning
several values returns a Python tuple (the transpiler knows statically which ones do).
"""

from __future__ import annotations

import math
import re

__all__ = [
    "LuaTable", "DefTable", "L_T", "L_t", "L_first", "L_adjust", "L_concat", "L_len", "L_div",
    "L_pow", "L_range", "L_pairs", "L_ipairs", "L_invoke", "L_tostring", "L_tonumber", "L_type",
    "L_insert", "L_remove", "L_sort", "L_sub", "L_strlen", "L_find", "L_gmatch", "L_floor",
    "L_max", "L_min", "L_noop", "L_lib",
]


class _Nodes:
    """Hash part of a Lua 5.3 table holding integer keys only (ltable.c, node for node).

    Only key placement is tracked (values live in LuaTable); it exists so that pairs() visits
    sparse integer keys in the same order as the real implementation. Integer keys hash to
    `key & (size-1)`, so unlike string keys this order is the same on every run of the game.
    """

    __slots__ = ("size", "keys", "alive", "next", "lastfree")

    def __init__(self, n):
        size = 1 << (n - 1).bit_length()
        self.size = size
        self.keys = [None] * size
        self.alive = [False] * size
        self.next = [0] * size
        self.lastfree = size

    def set(self, k, alive):
        """Record `t[k] = v` (alive = v is not nil). Returns True when the table must rehash."""
        keys, nxt, live = self.keys, self.next, self.alive
        mask = self.size - 1
        n = k & mask
        while True:  # luaH_getint
            if keys[n] == k:
                live[n] = alive
                return False
            d = nxt[n]
            if d == 0:
                break
            n += d
        mp = k & mask  # luaH_newkey
        if live[mp]:
            f = self.lastfree
            while True:
                if f == 0:
                    self.lastfree = 0
                    return True
                f -= 1
                if keys[f] is None:
                    break
            self.lastfree = f
            othern = keys[mp] & mask
            if othern != mp:
                while othern + nxt[othern] != mp:
                    othern += nxt[othern]
                nxt[othern] = f - othern
                keys[f], live[f], nxt[f] = keys[mp], live[mp], nxt[mp]
                if nxt[mp] != 0:
                    nxt[f] += mp - f
                    nxt[mp] = 0
                live[mp] = False
            else:
                nxt[f] = (mp + nxt[mp] - f) if nxt[mp] != 0 else 0
                nxt[mp] = f - mp
                mp = f
        keys[mp] = k
        live[mp] = alive
        return False


class LuaTable:
    """Lua table. Values: `arr` holds keys 1..n, `hash` everything else.

    `asize` and `nodes` mirror the real table's array-part size and node vector so that pairs()
    order matches Lua for integer keys; `nodes is False` once a non-integer key was stored (string
    hashes are seeded per run in the game, so insertion order is used there).
    """

    __slots__ = ("arr", "hash", "asize", "nodes", "holes")

    def __init__(self, arr=None, hash=None):
        self.arr = arr if arr is not None else []
        self.hash = hash if hash is not None else {}
        self.asize = len(self.arr)
        self.nodes = False if self.hash else None
        self.holes = False  # a positive integer key outside the dense prefix was ever stored

    def __getitem__(self, k):
        if k.__class__ is int:
            arr = self.arr
            if 0 < k <= len(arr):
                return arr[k - 1]
            return self.hash.get(k)
        if k.__class__ is float and k.is_integer():
            return self[int(k)]
        return self.hash.get(k)

    def __setitem__(self, k, v):
        if k.__class__ is not int:
            if k.__class__ is float and k.is_integer():
                self[int(k)] = v
                return
            self.nodes = False
            if v is None:
                self.hash.pop(k, None)
            else:
                self.hash[k] = v
            return
        if not 0 < k <= self.asize and self.nodes is not False:
            nodes = self.nodes
            if nodes is None or nodes.set(k, v is not None):
                self._rehash(k)
                if not 0 < k <= self.asize:
                    self.nodes.set(k, v is not None)
        arr = self.arr
        n = len(arr)
        if 0 < k <= n:
            arr[k - 1] = v
            if v is None:
                if k == n:
                    while arr and arr[-1] is None:
                        arr.pop()
                else:
                    self.holes = True
            return
        if k == n + 1:
            if v is None:
                self.hash.pop(k, None)
                return
            arr.append(v)
            h = self.hash
            if h:
                h.pop(k, None)
                k += 1
                while k in h:
                    arr.append(h.pop(k))
                    k += 1
            return
        if v is None:
            self.hash.pop(k, None)
        else:
            self.hash[k] = v
            if k > 0:
                self.holes = True

    def _rehash(self, ek):
        """ltable.c rehash(): recompute array/node sizes for the live keys plus `ek`."""
        nums = [0] * 64
        na = 0
        asize = self.asize
        for i, v in enumerate(self.arr[:asize]):
            if v is not None:
                nums[i.bit_length()] += 1  # ceil(log2(i + 1))
                na += 1
        if self.hash and asize > len(self.arr):
            for k in self.hash:
                if k.__class__ is int and len(self.arr) < k <= asize:
                    nums[(k - 1).bit_length()] += 1
                    na += 1
        total = na
        old = self.nodes
        if old:
            for k, alive in zip(old.keys, old.alive):
                if alive:
                    total += 1
                    if k > 0:
                        nums[(k - 1).bit_length()] += 1
                        na += 1
        if ek > 0:
            nums[(ek - 1).bit_length()] += 1
            na += 1
        total += 1
        a = optimal = cnt = 0
        twotoi = 1
        i = 0
        while na > twotoi // 2:
            if nums[i] > 0:
                a += nums[i]
                if a > twotoi // 2:
                    optimal = twotoi
                    cnt = a
            i += 1
            twotoi *= 2
        nh = total - cnt
        new = self.nodes = _Nodes(nh) if nh > 0 else None
        self.asize = optimal
        if optimal < asize:  # array shrinks: the cut-off slots move to the node vector
            for k in range(optimal + 1, asize + 1):
                if self[k] is not None:
                    new.set(k, True)
        if old:
            for j in range(old.size - 1, -1, -1):
                if old.alive[j] and not 0 < old.keys[j] <= optimal:
                    new.set(old.keys[j], True)

    def __repr__(self):
        return f"LuaTable({self.arr!r}, {self.hash!r})"


class DefTable:
    """`values` / `strings` / `flags` of a native object: missing keys read as a default.

    The native side stores doubles and hands integral ones back as integers.
    """

    __slots__ = ("d", "default")

    def __init__(self, default):
        self.d = {}
        self.default = default

    def __getitem__(self, k):
        return self.d.get(k, self.default)

    def __setitem__(self, k, v):
        if v.__class__ is float and v.is_integer():
            v = int(v)
        self.d[k] = v


def _fb(n):
    """Size hint as OP_NEWTABLE sees it (luaO_int2fb / luaO_fb2int round trip)."""
    if n < 8:
        return n
    e = 0
    while n >= 128:
        n = (n + 0xF) >> 4
        e += 4
    while n >= 16:
        n = (n + 1) >> 1
        e += 1
    return n << e


def L_T(arr=None, hash=None):
    """Table constructor: `arr` positional values, `hash` keyed fields in source order."""
    if arr:
        n = len(arr)
        while arr and arr[-1] is None:
            arr.pop()
        t = LuaTable(arr)
        t.asize = max(_fb(n), n)
    else:
        t = LuaTable()
    if hash:
        if all(k.__class__ is int for k in hash):
            t.nodes = _Nodes(_fb(len(hash)))
        for k, v in hash.items():
            if k.__class__ is int and 0 < k <= len(t.arr):
                continue  # positional entries are stored last and win
            if v is not None:
                t[k] = v
    return t


def L_t(x):
    return x is not None and x is not False


def L_first(x):
    return x[0] if x else None


def L_adjust(vals, n):
    k = len(vals)
    if k == n:
        return vals
    if k > n:
        return vals[:n]
    return tuple(vals) + (None,) * (n - k)


def _fmt_float(x):
    if x != x:
        return "nan" if math.copysign(1, x) > 0 else "-nan"
    if x in (math.inf, -math.inf):
        return "inf" if x > 0 else "-inf"
    s = "%.14g" % x
    if "." not in s and "e" not in s and "n" not in s:
        s += ".0"
    return s


def L_tostring(x=None, *_):
    c = x.__class__
    if c is str:
        return x
    if c is int:
        return str(x)
    if c is float:
        return _fmt_float(x)
    if x is None:
        return "nil"
    if x is True:
        return "true"
    if x is False:
        return "false"
    return f"{'table' if isinstance(x, (LuaTable, DefTable)) else 'function'}: 0x{id(x):08x}"


def L_concat(*parts):
    out = []
    for p in parts:
        c = p.__class__
        if c is str:
            out.append(p)
        elif c is int:
            out.append(str(p))
        elif c is float:
            out.append(_fmt_float(p))
        else:
            raise TypeError(f"attempt to concatenate a {L_type(p)} value")
    return "".join(out)


def L_len(x):
    if x.__class__ is LuaTable:
        if not x.holes or x.nodes is False:
            return len(x.arr)
        # luaH_getn: with holes the border Lua reports depends on the table's layout
        j = x.asize
        if j > 0 and x[j] is None:
            i = 0
            while j - i > 1:
                m = (i + j) // 2
                if x[m] is None:
                    j = m
                else:
                    i = m
            return i
        if x.nodes is None:
            return j
        i = j
        j += 1
        while x[j] is not None:
            i = j
            j *= 2
        while j - i > 1:
            m = (i + j) // 2
            if x[m] is None:
                j = m
            else:
                i = m
        return i
    if x.__class__ is str:
        return len(x)
    raise TypeError(f"attempt to get length of a {L_type(x)} value")


def L_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        if a == 0 or a != a:
            return math.nan
        return math.inf if (a > 0) == (math.copysign(1, b) > 0) else -math.inf


def L_pow(a, b):
    return math.pow(a, b)


def L_range(a, b, step=1):
    if a.__class__ is int and b.__class__ is int and step.__class__ is int:
        return range(a, b + (1 if step > 0 else -1), step)
    return _frange(float(a), float(b), float(step))


def _frange(a, b, step):
    if step > 0:
        while a <= b:
            yield a
            a += step
    else:
        while a >= b:
            yield a
            a += step


def L_ipairs(t, *_):
    i = 1
    while True:
        v = t[i]
        if v is None:
            return
        yield i, v
        i += 1


def L_pairs(t, *_):
    arr = t.arr
    h = t.hash
    nodes = t.nodes
    if nodes is False:
        i = 0
        while i < len(arr):
            v = arr[i]
            i += 1
            if v is not None:
                yield i, v
        for k in list(h):
            v = h.get(k)
            if v is not None:
                yield k, v
        return
    asize = t.asize
    i = 0
    while i < len(arr) and i < asize:
        v = arr[i]
        i += 1
        if v is not None:
            yield i, v
    if h and asize > len(arr):
        for k in sorted(k for k in h if 0 < k <= asize):
            v = t[k]
            if v is not None:
                yield k, v
    if nodes:
        for k, alive in list(zip(nodes.keys, nodes.alive)):
            if alive:
                v = t[k]
                if v is not None:
                    yield k, v


def L_invoke(obj, name, *args):
    return obj[name](obj, *args)


def L_type(x=None, *_):
    if x is None:
        return "nil"
    c = x.__class__
    if c is str:
        return "string"
    if c is int or c is float:
        return "number"
    if c is bool:
        return "boolean"
    if c is LuaTable or c is DefTable or isinstance(x, LuaTable):
        return "table"
    return "function"


_NUM = re.compile(r"^\s*(-?)\s*(0[xX][0-9a-fA-F]+|(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\s*$")


def L_tonumber(x=None, base=None, *_):
    c = x.__class__
    if c is int or c is float:
        return x
    if c is not str:
        return None
    m = _NUM.match(x)
    if m is None:
        return None
    sign, body = m.groups()
    if body[:2] in ("0x", "0X"):
        v = int(body, 16)
    elif body.isdigit():
        v = int(body)
    else:
        v = float(body)
    return -v if sign else v


def L_insert(t, a, b=None, *_):
    arr = t.arr
    n = len(arr) if not t.holes else L_len(t)
    if b is None:
        t[n + 1] = a
    elif a == n + 1:
        t[a] = b
    elif not t.holes:
        t[n + 1] = arr[n - 1]  # the only new key; then shift a..n up by one
        arr[a:n] = arr[a - 1 : n - 1]
        arr[a - 1] = b
    else:
        for i in range(n + 1, a, -1):
            t[i] = t[i - 1]
        t[a] = b


def L_remove(t, pos=None, *_):
    arr = t.arr
    if not t.holes and pos is not None and 0 < pos < len(arr):
        n = len(arr)
        v = arr[pos - 1]
        arr[pos - 1 : n - 1] = arr[pos:n]
        t[n] = None
        return v
    size = L_len(t)  # ltablib.c tremove, literally
    if pos is None:
        pos = size
    v = t[pos]
    while pos < size:
        t[pos] = t[pos + 1]
        pos += 1
    t[pos] = None
    return v


def L_sort(t, cmp=None, *_):
    # the game only sorts plain number/string lists without a comparator, where Lua's
    # unstable quicksort and Python's sort agree
    if cmp is not None:
        raise NotImplementedError("table.sort with comparator")
    t.arr.sort()


def L_sub(s, i=1, j=-1, *_):
    n = len(s)
    if i < 0:
        i = max(n + i + 1, 1)
    elif i == 0:
        i = 1
    if j < 0:
        j = n + j + 1
    elif j > n:
        j = n
    if i > j:
        return ""
    return s[int(i) - 1 : int(j)]


def L_strlen(s, *_):
    return len(s)


_CLASSES = {"a": "a-zA-Z", "d": "0-9", "l": "a-z", "u": "A-Z", "w": "a-zA-Z0-9", "s": r" \t\n\r\f\v",
            "p": r"!-/:-@\[-`{-~", "x": "0-9a-fA-F"}


def _lua_pattern(pat):
    """Translate the subset of Lua patterns the game uses into a Python regex."""
    out = []
    i = 0
    inset = False
    while i < len(pat):
        ch = pat[i]
        if ch == "%" and i + 1 < len(pat):
            nx = pat[i + 1]
            i += 2
            if nx.lower() in _CLASSES:
                body = _CLASSES[nx.lower()]
                if inset:
                    if nx.isupper():
                        raise NotImplementedError(pat)
                    out.append(body)
                else:
                    out.append(f"[{'^' if nx.isupper() else ''}{body}]")
            else:
                out.append(re.escape(nx))
            continue
        i += 1
        if inset:
            if ch == "]":
                inset = False
            out.append("\\\\" if ch == "\\" else ch)
        elif ch == "[":
            inset = True
            out.append(ch)
        elif ch == "-":
            out.append("*?")
        elif ch in ".^$*+?()":
            out.append(ch)
        else:
            out.append(re.escape(ch))
    return re.compile("".join(out), re.S)


_PATS = {}


def _pat(p):
    r = _PATS.get(p)
    if r is None:
        r = _PATS[p] = _lua_pattern(p)
    return r


def L_find(s, pat, init=1, plain=None, *_):
    """string.find → (start, end, captures...) or (None,)."""
    start = init - 1 if init > 0 else max(len(s) + init, 0)
    if plain:
        i = s.find(pat, start)
        return (None,) if i < 0 else (i + 1, i + len(pat))
    m = _pat(pat).search(s, start)
    if m is None:
        return (None,)
    return (m.start() + 1, m.end(), *m.groups())


def L_gmatch(s, pat, *_):
    for m in _pat(pat).finditer(s):
        g = m.groups()
        yield (g if len(g) > 1 else g[0]) if g else m.group(0)


def L_floor(x, *_):
    return math.floor(x)


def L_max(*a):
    return max(a)


def L_min(*a):
    return min(a)


def L_noop(*_):
    return None


def _atan(y, x=1, *_):
    return math.atan2(y, x)


# library functions reached as `math.x` / `string.x` / `table.x` / bare builtins
L_lib = {
    "math.abs": abs, "math.floor": L_floor, "math.ceil": math.ceil, "math.max": L_max,
    "math.min": L_min, "math.sqrt": math.sqrt, "math.sin": math.sin, "math.cos": math.cos,
    "math.rad": math.radians, "math.deg": math.degrees, "math.atan2": _atan, "math.atan": _atan,
    "string.sub": L_sub, "string.len": L_strlen, "string.find": L_find, "string.gmatch": L_gmatch,
    "string.lower": str.lower, "string.upper": str.upper,
    "table.insert": L_insert, "table.remove": L_remove, "table.sort": L_sort,
    "tostring": L_tostring, "tonumber": L_tonumber, "type": L_type, "pairs": L_pairs,
    "ipairs": L_ipairs, "print": L_noop, "collectgarbage": L_noop,
}
