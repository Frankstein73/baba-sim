"""One-time export of the game's sprites and palettes into src/babasim/data/sprites.zip.

Only the first wobble frame of every sprite is kept (still pictures need no more).

    uv run python tools/export_sprites.py [GAME_DATA_DIR] [PACKS_DIR ...]

A packs directory holds Worlds/<world>/ like the game does; only its worlds' own sprites and palettes are taken.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "babasim" / "data" / "sprites.zip"


def main() -> None:
    game = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "game"
    n = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(game.glob("Sprites/*_1.png")):
            z.write(p, f"Sprites/{p.name}")
            n += 1
        for p in sorted(game.glob("Palettes/*.png")):
            z.write(p, str(p.relative_to(game)))
            n += 1
        for root in (game, *map(Path, sys.argv[2:])):
            for p in sorted(root.glob("Worlds/*/Sprites/*_1.png")):
                z.write(p, f"Worlds/{p.parent.parent.name}/Sprites/{p.name}")
                n += 1
            for p in sorted(root.glob("Worlds/*/Palettes/*.png")):
                z.write(p, str(p.relative_to(root)))
                n += 1
    print(f"{n} files -> {OUT} ({OUT.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
