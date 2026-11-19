"""Translate the game's Lua logic into Python modules under src/babasim/gen/.

    uv run python tools/lua2py.py [GAME_DATA_DIR]

One-time build step (needs the installed game); the generated modules are committed and are what
the engine runs. Each module exposes `load(G)`, which executes the file's top-level code against the
global table `G`. Semantics helpers live in babasim.luart.
"""

from __future__ import annotations

import keyword
import sys
from pathlib import Path

from luaparser import ast
from luaparser import astnodes as N

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "babasim" / "gen"

FILES = [
    "constants", "colours", "values", "metadata", "tools", "conditions", "rules", "movement",
    "blocks", "effects", "features", "syntax", "vision", "update", "load", "convert", "undo",
    "clears", "Editor/editor_constants", "Editor/editor_objectlist", "changes", "letterunits",
    "map", "mapcursor", "modsupport", "dynamictiling",
]

# library calls bound directly to runtime helpers (everything else goes through G)
DIRECT = {
    "math.abs": "abs", "math.floor": "L_floor", "math.max": "L_max", "math.min": "L_min",
    "string.sub": "L_sub", "string.len": "L_strlen", "string.find": "L_find",
    "string.gmatch": "L_gmatch", "table.insert": "L_insert", "table.remove": "L_remove",
    "table.sort": "L_sort", "tostring": "L_tostring", "tonumber": "L_tonumber", "type": "L_type",
    "pairs": "L_pairs", "ipairs": "L_ipairs", "print": "L_noop", "collectgarbage": "L_noop",
}
# files that are menus/cutscenes/editor UI: not translated, their functions become no-op stubs
UI_FILES = ["menu", "ending", "debug", "utf_decoder", "Editor/editor", "Editor/editor_menudata",
            "Editor/editor_objectlist_func", "Editor/editor_tutorial", "Editor/editor_undo"]
BUILTIN_MULTI = {"string.find"}
RESERVED = set(keyword.kwlist) | set(keyword.softkwlist) | {"G", "abs", "load", "print", "len", "id",
                                                            "type", "max", "min", "range", "str", "int",
                                                            "float", "list", "dict", "tuple", "set", "dir"}
BOOL_OPS = (N.EqToOp, N.NotEqToOp, N.LessThanOp, N.GreaterThanOp, N.LessOrEqThanOp,
            N.GreaterOrEqThanOp, N.ULNotOp, N.TrueExpr, N.FalseExpr)
ARITH = {N.AddOp: "+", N.SubOp: "-", N.MultOp: "*", N.ModOp: "%", N.FloorDivOp: "//"}
REL = {N.LessThanOp: "<", N.GreaterThanOp: ">", N.LessOrEqThanOp: "<=", N.GreaterOrEqThanOp: ">="}


def lib_name(node):
    """'string.sub' for `string.sub`, 'pairs' for a bare builtin name, else None."""
    if isinstance(node, N.Name):
        return node.id
    if (isinstance(node, N.Index) and node.notation == N.IndexNotation.DOT
            and isinstance(node.value, N.Name) and node.value.id in ("string", "table", "math")):
        return f"{node.value.id}.{node.idx.id}"
    return None


def func_key(node):
    """Name under which a function definition is known for the multi-return analysis."""
    if isinstance(node, N.Name):
        return node.id
    if isinstance(node, N.Index) and isinstance(node.idx, N.Name):
        return node.idx.id
    return None


def own_returns(body):
    """Return statements of a function body, not descending into nested functions."""
    stack = [body]
    while stack:
        n = stack.pop()
        if isinstance(n, N.Return):
            yield n
        for v in vars(n).values() if isinstance(n, N.Node) else ():
            for c in v if isinstance(v, list) else (v,):
                if isinstance(c, N.Node) and not isinstance(
                        c, (N.Function, N.LocalFunction, N.AnonymousFunction, N.Method)):
                    stack.append(c)


def find_multi(trees):
    """Names of functions that can return more or fewer than one value used as several."""
    funcs = {}
    for tree in trees:
        for n in ast.walk(tree):
            if isinstance(n, (N.Function, N.LocalFunction)):
                funcs.setdefault(func_key(n.name), []).append(n)
    multi = set(BUILTIN_MULTI)
    changed = True
    while changed:
        changed = False
        for name, defs in funcs.items():
            if name in multi:
                continue
            for d in defs:
                for r in own_returns(d.body):
                    vals = r.values or []
                    last = vals[-1] if vals else None
                    tail_multi = (isinstance(last, N.Call) and not last.wrapped
                                  and (lib_name(last.func) in multi or func_key(last.func) in multi))
                    if len(vals) > 1 or tail_multi:
                        multi.add(name)
                        changed = True
                        break
                if name in multi:
                    break
    return multi


class Func:
    """Per-Python-function emission state."""

    def __init__(self, parent, multi):
        self.parent = parent
        self.multi = multi
        self.scopes = [{}]
        self.declared = set()
        self.nonlocals = set()
        self.tmp = 0


class Emitter:
    def __init__(self, multi):
        self.multi = multi
        self.lines = []
        self.fn = None
        self.used = set()  # python local names used anywhere in this module
        self.anon = 0

    # ---- names -------------------------------------------------------------------------
    def declare(self, name):
        base = name + "_" if name in RESERVED or name.startswith("L_") else name
        py, i = base, 1
        while py in self.used:
            i += 1
            py = f"{base}_{i}"
        self.used.add(py)
        self.fn.scopes[-1][name] = py
        self.fn.declared.add(py)
        return py

    def lookup(self, name, assign=False):
        fn = self.fn
        while fn is not None:
            for scope in reversed(fn.scopes):
                if name in scope:
                    if assign and fn is not self.fn:
                        self.fn.nonlocals.add(scope[name])
                    return scope[name]
            fn = fn.parent
        return None

    def temp(self):
        self.fn.tmp += 1
        py = f"_t{self.fn.tmp}"
        return py

    # ---- expressions -------------------------------------------------------------------
    def is_multi_call(self, e):
        if not isinstance(e, N.Call) or e.wrapped:
            return False
        f = e.func
        if isinstance(f, N.Name) and self.lookup(f.id) is not None:
            return f.id in self.multi and f.id not in DIRECT
        return lib_name(f) in self.multi or func_key(f) in self.multi

    def exprs(self, es):
        """Comma-separated argument list with a trailing multi-value call expanded."""
        out = [self.expr(e) for e in es[:-1]]
        if es:
            last = es[-1]
            out.append("*" + self.call(last) if self.is_multi_call(last) else self.expr(last))
        return ", ".join(out)

    def call(self, e):
        f = e.func
        name = lib_name(f)
        if isinstance(f, N.Name) and self.lookup(f.id) is not None:
            target = self.lookup(f.id)
        elif name in DIRECT:
            target = DIRECT[name]
        else:
            target = self.expr(f)
        return f"{target}({self.exprs(e.args)})"

    def cond(self, e):
        if isinstance(e, N.AndLoOp):
            return f"({self.cond(e.left)} and {self.cond(e.right)})"
        if isinstance(e, N.OrLoOp):
            return f"({self.cond(e.left)} or {self.cond(e.right)})"
        if isinstance(e, N.ULNotOp):
            return f"(not {self.cond(e.operand)})"
        if isinstance(e, BOOL_OPS):
            return self.expr(e)
        if isinstance(e, N.Nil):
            return "False"
        if isinstance(e, N.Name) and self.lookup(e.id) is not None:
            py = self.lookup(e.id)
            return f"({py} is not None and {py} is not False)"
        return f"L_t({self.expr(e)})"

    def expr(self, e):
        if isinstance(e, N.Nil):
            return "None"
        if isinstance(e, N.TrueExpr):
            return "True"
        if isinstance(e, N.FalseExpr):
            return "False"
        if isinstance(e, N.Number):
            return repr(e.n)
        if isinstance(e, N.String):
            s = e.s
            return repr(s.decode("utf-8", errors="replace") if isinstance(s, bytes) else s)
        if isinstance(e, N.Name):
            py = self.lookup(e.id)
            return py if py is not None else f"G[{e.id!r}]"
        if isinstance(e, N.Index):
            key = repr(e.idx.id) if e.notation == N.IndexNotation.DOT else self.expr(e.idx)
            return f"{self.expr(e.value)}[{key}]"
        if isinstance(e, N.Call):
            c = self.call(e)
            return f"L_first({c})" if self.is_multi_call(e) or (
                e.wrapped and self.is_multi_call(_unwrapped(e))) else c
        if isinstance(e, N.Invoke):
            args = self.exprs(e.args)
            return f"L_invoke({self.expr(e.source)}, {e.func.id!r}{', ' + args if args else ''})"
        if isinstance(e, N.AnonymousFunction):
            self.anon += 1
            name = f"_anon{self.anon}"
            self.used.add(name)
            self.function(name, e.args, e.body, False, getattr(e, "line", None))
            return name
        if isinstance(e, N.Table):
            return self.table(e)
        if isinstance(e, N.AndLoOp):
            if isinstance(e.left, BOOL_OPS):
                return f"({self.expr(e.right)} if {self.expr(e.left)} else False)"
            t = self.temp()
            return f"({self.expr(e.right)} if L_t({t} := {self.expr(e.left)}) else {t})"
        if isinstance(e, N.OrLoOp):
            if isinstance(e.left, BOOL_OPS):
                return f"(True if {self.expr(e.left)} else {self.expr(e.right)})"
            t = self.temp()
            return f"({t} if L_t({t} := {self.expr(e.left)}) else {self.expr(e.right)})"
        if isinstance(e, N.ULNotOp):
            return f"(not {self.cond(e.operand)})"
        if isinstance(e, (N.EqToOp, N.NotEqToOp)):
            neg = isinstance(e, N.NotEqToOp)
            for a, b in ((e.left, e.right), (e.right, e.left)):
                if isinstance(b, (N.Nil, N.TrueExpr, N.FalseExpr)):
                    return f"({self.expr(a)} is {'not ' if neg else ''}{self.expr(b)})"
            return f"({self.expr(e.left)} {'!=' if neg else '=='} {self.expr(e.right)})"
        if type(e) in REL:
            return f"({self.expr(e.left)} {REL[type(e)]} {self.expr(e.right)})"
        if type(e) in ARITH:
            return f"({self.expr(e.left)} {ARITH[type(e)]} {self.expr(e.right)})"
        if isinstance(e, N.FloatDivOp):
            return f"L_div({self.expr(e.left)}, {self.expr(e.right)})"
        if isinstance(e, N.ExpoOp):
            return f"L_pow({self.expr(e.left)}, {self.expr(e.right)})"
        if isinstance(e, N.UMinusOp):
            return f"(-{self.expr(e.operand)})"
        if isinstance(e, N.ULengthOP):
            return f"L_len({self.expr(e.operand)})"
        if isinstance(e, N.Concat):
            parts = []
            stack = [e]
            while stack:
                n = stack.pop()
                if isinstance(n, N.Concat) and (n is e or not n.wrapped):
                    stack.append(n.right)
                    stack.append(n.left)
                else:
                    parts.append(self.expr(n))
            return f"L_concat({', '.join(parts)})"
        raise NotImplementedError(f"expression {type(e).__name__} at line {getattr(e, 'line', '?')}")

    def table(self, e):
        pos, keyed = [], []
        for i, f in enumerate(e.fields):
            if f.key is None:
                last = i == len(e.fields) - 1
                pos.append("*" + self.call(f.value) if last and self.is_multi_call(f.value)
                           else self.expr(f.value))
            else:
                key = self.expr(f.key) if f.between_brackets else repr(f.key.id)
                keyed.append(f"{key}: {self.expr(f.value)}")
        if not pos and not keyed:
            return "L_T()"
        if not keyed:
            return f"L_T([{', '.join(pos)}])"
        return f"L_T([{', '.join(pos)}], {{{', '.join(keyed)}}})"

    # ---- statements --------------------------------------------------------------------
    def emit(self, depth, text):
        self.lines.append("\t" * depth + text)

    def block(self, body, depth, new_scope=True):
        if new_scope:
            self.fn.scopes.append({})
        start = len(self.lines)
        for s in body.body:
            self.stmt(s, depth)
        if len(self.lines) == start:
            self.emit(depth, "pass")
        if new_scope:
            self.fn.scopes.pop()

    def target(self, t):
        if isinstance(t, N.Name):
            py = self.lookup(t.id, assign=True)
            return py if py is not None else f"G[{t.id!r}]"
        return self.expr(t)

    def assign(self, targets, values, depth):
        n = len(targets)
        if n == 1 and len(values) == 1:
            self.emit(depth, f"{targets[0]} = {self.expr(values[0])}")
            return
        tail_multi = bool(values) and self.is_multi_call(values[-1])
        if not tail_multi:
            vals = [self.expr(v) for v in values[:n]]
            extra = values[n:]
            vals += ["None"] * (n - len(vals))
            for x in extra:  # evaluated for side effects, value dropped
                self.emit(depth, self.expr(x))
            self.emit(depth, f"{', '.join(targets)} = {', '.join(vals)}")
            return
        self.emit(depth, f"{', '.join(targets)}{',' if n == 1 else ''} = L_adjust(({self.exprs(values)},), {n})")

    def function(self, pyname, args, body, multi, line, depth=None):
        """Emit `def pyname(...)` at the current statement position."""
        depth = self.cur_depth if depth is None else depth
        outer = self.fn
        self.fn = Func(outer, multi)
        params = []
        for a in args:
            if isinstance(a, N.Varargs):
                raise NotImplementedError("varargs")
            params.append(self.declare(a.id))
        head = len(self.lines)
        saved_depth = self.cur_depth
        self.block(body, depth + 1, new_scope=False)
        if multi:
            self.emit(depth + 1, "return ()")
        self.cur_depth = saved_depth
        sig = ", ".join(f"{p}=None" for p in params)
        header = ["\t" * depth + f"def {pyname}({sig + ', ' if sig else ''}*_):" + (f"  # L{line}" if line else "")]
        if self.fn.nonlocals:
            header.append("\t" * (depth + 1) + "nonlocal " + ", ".join(sorted(self.fn.nonlocals)))
        self.lines[head:head] = header
        self.fn = outer

    def stmt(self, s, depth):
        self.cur_depth = depth
        if isinstance(s, (N.SemiColon, N.Comment)):
            return
        if isinstance(s, N.Call):
            self.emit(depth, self.call(s))
        elif isinstance(s, N.Invoke):
            self.emit(depth, self.expr(s))
        elif isinstance(s, N.LocalAssign):
            # values are evaluated before the new names come into scope
            if len(s.targets) == 1 and len(s.values) <= 1:
                v = self.expr(s.values[0]) if s.values else "None"
                self.emit(depth, f"{self.declare(s.targets[0].id)} = {v}")
            else:
                tmp_scope = {}
                self.fn.scopes.append(tmp_scope)
                names = [self.declare(t.id) for t in s.targets]
                self.fn.scopes.pop()
                self.assign(names, s.values, depth)
                self.fn.scopes[-1].update(tmp_scope)
        elif isinstance(s, N.Assign):
            self.assign([self.target(t) for t in s.targets], s.values, depth)
        elif isinstance(s, N.Function):
            key = func_key(s.name)
            multi = key in self.multi
            if isinstance(s.name, N.Name) and self.lookup(s.name.id) is None:
                py = f"f_{s.name.id}"
                self.used.add(py)
                self.function(py, s.args, s.body, multi, s.line)
                self.emit(depth, f"G[{s.name.id!r}] = {py}")
            else:
                self.anon += 1
                py = f"_fn{self.anon}"
                self.function(py, s.args, s.body, multi, s.line)
                self.emit(depth, f"{self.target(s.name)} = {py}")
        elif isinstance(s, N.LocalFunction):
            py = self.declare(s.name.id)
            self.function(py, s.args, s.body, s.name.id in self.multi, s.line)
        elif isinstance(s, N.If):
            self.emit(depth, f"if {self.cond(s.test)}:")
            self.block(s.body, depth + 1)
            o = s.orelse
            while isinstance(o, N.ElseIf):
                self.emit(depth, f"elif {self.cond(o.test)}:")
                self.block(o.body, depth + 1)
                o = o.orelse
            if o is not None:
                self.emit(depth, "else:")
                self.block(o, depth + 1)
        elif isinstance(s, N.While):
            self.emit(depth, f"while {self.cond(s.test)}:")
            self.block(s.body, depth + 1)
        elif isinstance(s, N.Repeat):
            self.emit(depth, "while True:")
            self.fn.scopes.append({})
            self.block(s.body, depth + 1, new_scope=False)
            self.emit(depth + 1, f"if {self.cond(s.test)}:")
            self.emit(depth + 2, "break")
            self.fn.scopes.pop()
        elif isinstance(s, N.Fornum):
            step = s.step if isinstance(s.step, N.Node) else None
            rng = f"{self.expr(s.start)}, {self.expr(s.stop)}" + (f", {self.expr(step)}" if step is not None else "")
            self.fn.scopes.append({})
            self.emit(depth, f"for {self.declare(s.target.id)} in L_range({rng}):")
            self.block(s.body, depth + 1)
            self.fn.scopes.pop()
        elif isinstance(s, N.Forin):
            it = ", ".join(self.expr(i) for i in s.iter)
            self.fn.scopes.append({})
            names = ", ".join(self.declare(t.id) for t in s.targets)
            self.emit(depth, f"for {names} in {it}:")
            self.block(s.body, depth + 1)
            self.fn.scopes.pop()
        elif isinstance(s, N.Return):
            vals = s.values or []
            if self.fn.multi:
                if len(vals) == 1 and self.is_multi_call(vals[0]):
                    self.emit(depth, f"return {self.call(vals[0])}")
                else:
                    self.emit(depth, f"return ({self.exprs(vals)}{',' if vals else ''})")
            else:
                self.emit(depth, f"return {self.expr(vals[0])}" if vals else "return None")
        elif isinstance(s, N.Break):
            self.emit(depth, "break")
        elif isinstance(s, N.Do):
            self.block(s.body, depth)
        else:
            raise NotImplementedError(f"statement {type(s).__name__} at line {getattr(s, 'line', '?')}")

    def module(self, tree, source):
        self.fn = Func(None, False)
        self.cur_depth = 1
        self.block(tree.body, 1, new_scope=False)
        head = [
            f'"""Generated from {source} by tools/lua2py.py. Do not edit."""',
            "from babasim.luart import *  # noqa: F403",
            "",
            "",
            "def load(G):",
        ]
        return "\n".join(head + self.lines) + "\n"


def _unwrapped(e):
    c = N.Call(e.func, e.args)
    c.wrapped = False
    return c


def main():
    game = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "game"
    trees = {f: ast.parse((game / f"{f}.lua").read_text(encoding="utf-8", errors="replace")) for f in FILES}
    multi = find_multi(trees.values())
    OUT.mkdir(exist_ok=True)
    ui = set()
    for f in UI_FILES:
        tree = ast.parse((game / f"{f}.lua").read_text(encoding="utf-8", errors="replace"))
        ui |= {n.name.id for n in ast.walk(tree) if isinstance(n, N.Function) and isinstance(n.name, N.Name)}
    (OUT / "__init__.py").write_text(
        '"""Game logic translated from Lua (tools/lua2py.py)."""\n\nMODULES = '
        + repr([f.split("/")[-1] for f in FILES]) + "\n\n# UI-only functions of the untranslated files\nUI_STUBS = "
        + repr(sorted(ui)) + "\n")
    for f, tree in trees.items():
        code = Emitter(multi).module(tree, f"{f}.lua")
        compile(code, f, "exec")
        (OUT / f"{f.split('/')[-1]}.py").write_text(code)
    print(f"{len(FILES)} modules; multi-return functions: {sorted(multi)}")


if __name__ == "__main__":
    main()
