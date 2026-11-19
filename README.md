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

## Letting a model play

`babasim.session.Session` exposes four tools (`move`, `undo`, `restart`, `look`) as function-calling
schemas and executes tool calls; prompts and observations are English by default (`lang="zh"` for
Chinese) and describe only how to interact, not how the game works.

```
# in-process agent loop against an OpenAI-compatible endpoint
OPENAI_BASE_URL=http://host:4000/v1 OPENAI_API_KEY=... python tools/play_llm.py 0level --model NAME --max-calls 30

# or as an HTTP service (stdlib only, no auth: bind to a trusted interface)
python -m babasim.server --host 127.0.0.1 --port 8765
curl -s -X POST localhost:8765/sessions -d '{"level":"0level","max_calls":30}'
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
