# babasim

Standalone Python engine that reproduces Baba Is You's game logic (single level + undo), for
offline testing. Internal use only.

## Layout

| path | what |
|---|---|
| `src/babasim/runtime.py` | native side re-implemented: objects, tilemap, `MF_*`, level start and per-turn call order |
| `src/babasim/gen/` | game logic translated from the original Lua by `tools/lua2py.py` (generated, do not edit) |
| `src/babasim/luart.py` | Lua 5.3 value semantics used by the generated code (tables incl. exact `pairs` order for integer keys, `#`, strings, `rand()`) |
| `src/babasim/api.py`, `text.py`, `render.py` | model-facing layer: states, per-turn events, text and image observations (`docs/state-schema.md`) |
| `src/babasim/data/` | levels, object tables and sprites/palettes exported once from the game (`tools/export_data.py`, `tools/export_sprites.py`), shipped inside the package |
| `re/NATIVE_TURN_LOOP.md` | what the native binary calls, in which order (recovered from the binary) |
| `tools/oracle/` | dev only: runs the original Lua headless (lupa) to compare against |
| `docs/state-schema.md` | observation/event format, with implementation status in §10 |

At run time the installed package is self-contained — no game install, no Lua. Images need the `render` extra (Pillow).

## Use

```python
from babasim.runtime import Engine
e = Engine()            # world "baba"
e.load("0level", seed=0)
e.move("r")             # r/u/l/d, w = wait
e.undo()
e.won, e.state(), e.rules()

from babasim.api import Game
from babasim.text import format_step
g = Game("0level", rules="list")     # perceptual view by default
r = g.step("right")                  # {"action", "events", "state"}
print(format_step(r))
g.play(["right"] * 8)                # stops on win

from babasim.render import Renderer
Renderer(g).frames("phases")         # [(t, PIL image)] of the last step
```

```
python -m babasim 0level --moves rrrrrrrr --gif last.gif
python -m babasim 0level              # interactive
```

## Levels

A level is asked for by its in-game name (`Game("baba is you")`, `{"level": "baba is you"}`); the file stem
(`0level`) is taken too. `data/campaign_<world>.json` lists the playable levels of a world in playing order,
each with a name that is unique in the world (a name used twice gets its map appended: `prison (Neon City)`).

| world | what | levels |
|---|---|---|
| `baba` | main game | 217 |
| `repose` | Repose 2.5, Marlowe — marlowowe.itch.io/repose | 160 |
| `alphons` | Alphons Allstars, Alphons6 — alphons6.itch.io/alphons-allstars | 156 |
| `babagang` | Baba Gang Adventures, quickmimic — quickmimic.itch.io/babagang-adventures-a-baba-is-you-levelpack | 154 |
| `disappearance` | Disappearance v1b, trollbreeder — trollbreeder.itch.io/disappearance | 41 |
| `ruins_of_text` | Ruins of Text 1.0.6 — notaninart.itch.io/ruins-of-text-baba | 11 |
| `lost_and_found` | Lost And Found, olie — itsolie.itch.io/lostandfound | 9 |
| `rescripted` | Rescripted v1, acb — acben.itch.io/rescripted | 9 |
| `perennial` | Perennial, hutthutthutt — hutt3.itch.io/baba-is-you-levelpack-perennial | 8 |
| `ferchus` | Ferchus' Complete Pack — ferchus.itch.io/baba-is-you-level-pack | 6 |

The packs are community level packs without Lua mods, so the translated game logic plays them as the game does.
Every level loads and survives random play; none has been checked for being winnable here. `new_adv` and
`museum` (shipped with the game) have level files but no campaign list yet. To add a pack, unpack its world
directory to `packs/Worlds/<world>/` and run

```
uv run python tools/export_data.py game packs       # levels
uv run python tools/export_sprites.py game packs    # the packs' own sprites and palettes
uv run python tools/export_campaign.py packs        # data/campaign_<world>.json
```

## Letting a model play

`babasim.session.Session` exposes four tools (`move`, `undo`, `restart`, `look`) as function-calling
schemas and executes tool calls; prompts and observations are English by default (`lang="zh"` for
Chinese) and describe only how to interact, not how the game works.

```
# in-process agent loop against an OpenAI-compatible endpoint
OPENAI_BASE_URL=http://host:4000/v1 OPENAI_API_KEY=... python tools/play_llm.py 0level --model NAME --max-calls 30

# or as an HTTP service (stdlib only, no auth: bind to a trusted interface)
python -m babasim.server --host 127.0.0.1 --port 8765
curl -s -X POST localhost:8765/sessions -d '{"level":"baba is you","max_calls":30}'
curl -s -X POST localhost:8765/sessions -d '{"world":"repose","level":"double moat"}'
curl -s -X POST localhost:8765/sessions/<id>/call -d '{"name":"move","arguments":{"actions":["right","right"]}}'
```

Endpoints: `GET /health`, `GET /levels?world=`, `POST /sessions`, `POST /sessions/<id>/call`,
`GET /sessions/<id>`, `DELETE /sessions/<id>` (see `src/babasim/server.py`).

## Dev (needs the game at ./game)

```
uv run python tools/lua2py.py            # regenerate src/babasim/gen
uv run pytest                            # engine tests + oracle comparison
uv run python tools/oracle/diff.py baba 80 1   # random-walk differential test over a world
```

## Known limits of "exact"

- Where the Lua iterates a string-keyed table with `pairs`, the real game's order depends on a
  per-launch hash seed. The engine uses insertion order; rule order and the creation order of
  simultaneously spawned objects can therefore differ from a given run of the game (as two runs
  of the game differ from each other).
- `math.random` is unseeded in the game (shared libc state). The engine takes a `seed`; the
  generator itself is macOS `rand()` as used by the Mac build.
- World map, menus, editor, 3D mode visuals are out of scope.
