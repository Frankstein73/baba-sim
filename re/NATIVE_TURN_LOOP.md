# Native call order around the Lua logic (macOS Chowdren build, x86_64)

Recovered from the decompiled event groups (`re/out/funcs2/<addr>.c`). Addresses are Ghidra VAs.

Conventions used by the native → Lua bridge:

| native | meaning |
|---|---|
| `FUN_10048c940(&s_name)` | call Lua global `name` with the arguments pushed so far |
| `FUN_10048c370(str)` / `c400(int)` / `c430(double)` / `c680(bool)` / `c6b0()` | push string / int / number / bool / nil argument |
| `FUN_10048e340(i)` | read i-th return value (int) of the last Lua call |
| `FUN_10048c190(&s_MF_x, fn)` | register native `MF_x` (all in `FUN_1003f6400`) |

Object memory: alterable values are doubles at `obj+0x280 + 8*(i-1)` for Lua `values[i]`; flags are a
bitfield at `obj+0x350`, bit `n` = Lua `flags[n]` (verified: MF_cleanremove sets `0x8000` = DEAD 15).
`V` below is `generaldata.values[UPDATE]` (generaldata = frame object at `+0x108`).

## 1. A move — `command(key, player)`

Input handler `FUN_1001d0410` → Lua `command(key)`. Lua runs `movecommand(...)` and then the native
`MF_update()` (`FUN_100278f70` → `FUN_1002525e0`), which sets `generaldata.values[DELAY_INGAME]`
(visual delay), sets `V = 1` and runs the turn group **synchronously, once**.

## 2. Turn group `FUN_1001cf610` (V = 1 after a move, V = 2 after an undo)

| # | condition | Lua calls, in order |
|---|---|---|
| 1 | V ≥ 1 | `doupdate()`, `smallclear()`, `setunitmap()` |
| 2 | V ≥ 1 | `code()` |
| 3 | V = 1 | `updateeffecthistory()`, `fallblock()`, `doupdate()`, `code()`, `statusblock()`, `domaprotation()` |
| 4 | V = 2 | `reseteffecthistory()`, `statusblock(nil, true)` |
| 5 | V = 1 | `conversion(true)`, `fallblock()` |
| 6 | V ≥ 1 | `doupdate()`, `code()` |
| 7 | V = 1 | `levelblock()`, `block()`, `dolevelconversions()` |
| 8 | V ≥ 1 | native `FUN_1001ce3b0`: clear `flags[CONVERTED]` on **every** unit object |
| 9 | V ≥ 1 | `doupdate()`, `smallclear()`, `setunitmap()` |
| 10 | V ≥ 1 | `code()`, `findplayer(V)`, `checkturnsound()` |
| 11 | V = 1 | sound bookkeeping only (`FUN_1001ce600/7f0/ea50`, TURNSOUND strings) |
| 12 | V = 2 | native: destroy leftover effect objects (three object lists) — visual only |
| 13 | V ≥ 1 | `effectblock()`, `diceblock()` |
| 14 | V ≥ 1 and spritedata VISION = 1 | native 3D-vision refresh (`FUN_1001cde80`) — visual only |
| 15 | V ≥ 1 and CURRLEVEL string ≠ a stored string | `cursorcheck()` (map cursor; result stored in an object value) |
| 16 | V = 1 | `shorteffectblock()`, `groupcheck()`, `destroylevel_do()` |
| 17 | V ≥ 1 | `update_cleanup()` |
| 18 | V = 1 | `FUN_1001cf350`: for every unit `values[MOVED] = max(0, MOVED-1)`, `values[PUSHED] = 4` (animation timers); `V = 0`; `newundo()`, `animate()`, `cleanup()`, `do_mod_hook("turn_end")` |
| 19 | V = 2 | `V = 0`; `animate()`, `cleanup()` |

Notes
- `block()` is called without arguments (small = nil). The second caller `FUN_1001ce350` is the same
  group split out (levelblock/block/dolevelconversions).
- `conversion` gets `true` (dolevels). `findplayer` gets V (1 or 2 → `undoing` is truthy in both).
- Nothing else touches Lua state between these calls.

## 3. Undo

`FUN_1002b49e0` (key repeat logic) → `dolog("undo")` → `FUN_1001d0350`:
`undo()` → if it returned 1 play an undo sound (`FUN_1001d0150`; uses the native LCG
`x = x*0x343fd + 0x269ec3`, sound only) → `V = 2` → turn group above (rows with V ≥ 1 and V = 2).

## 4. Level start `FUN_1001b9e60`

1. `FUN_1001b7a70` → `clearunits()`; `FUN_1001b82c0` → `clear()`
2. `setseedingtype(n)` from the level `.ld` `[general] seeding`, else from settings
3. (logging only) `resetlogrules()`
4. Level load `FUN_1001b2dc0`:
   - `.ld` reading, `loadcustomobjects(str)` if `[general] customobjects` is non-empty, object changes (`FUN_1001ab590` → `handleobjectchanges`)
   - tiles: `for x = 0 .. ROOMSIZEX-1: for y = 0 .. ROOMSIZEY-1: for layer = 0,1,2:` if a tile exists →
     `loadtile(tx, ty)` → create object → `values[XPOS]=x, values[YPOS]=y, values[DIR]=tile dir, values[ONLINE]=1`, flag bit 9 set →
     `addunit(fixed, nil, true)`. **Unit order is x-major, then y, then layer.**
   - then map-only content: `[levels]`, `[paths]`, `[specials]` entries, `loadpathgate()`, `createcobjectlist()`,
     `setfixedrandom`/`overrideundoseeding` (`FUN_1001b1dc0`), `levelparticles(...)`
5. `createobjectpalette()` (editor) ; `code()` ; `mapcursor_load()`
6. `undostate(false)`, `startblock()`, `animate()`, `clear()`, `undostate(true)` — `clear()` resets the rule/feature
   tables (not the units; that is `clearunits()`), so the `code()` in step 7 rebuilds rules from scratch
7. `code()`, `cursorcheck()`, `do_mod_hook("level_start")`

## 5. Natives that matter for logic

- `fixed` ids are derived from the object pointer (`ptr >> 3 | tag`). Their numeric order is not
  meaningful and not stable between runs, so any Lua behaviour depending on `pairs()` order over
  fixed-keyed tables is already nondeterministic in the game; the port picks creation order.
- `MF_getfixed(id)`: first unit with `values[ID] == id` and DEAD flag clear.
- `MF_create(name)` / `MF_emptycreate(name, x, y)`: create object of class `name`, return fixed;
  `MF_emptycreate` then calls `setundo(1)`.
- `MF_remove(fixed)` / `MF_specialremove(fixed, type)`: destroy object, `setundo(1)`.
  `MF_cleanremove(fixed)`: set DEAD flag, destroy.
- `MF_random(a, b)`: Mersenne Twister seeded from the clock → not reproducible; gameplay randomness
  that must be reproducible goes through Lua `math.random` + `Fixedseed` (see `setfixedrandom`).
- `MF_restart(true)` → `FUN_1001dc780` → level transition/reload (same as level start).
- `MF_win()` → `do_mod_hook("level_win")`, sets the win state, `customending_win()` in special cases.
