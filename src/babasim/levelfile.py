"""Readers for the original level files (`Nlevel.l` binary grid, `Nlevel.ld` INI metadata)."""

from __future__ import annotations

import configparser
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path

EMPTY = 0xFFFF


@dataclass
class Layer:
    width: int
    height: int
    header: bytes  # unparsed per-layer header (offsets/parallax), kept for later RE
    tiles: list[int]  # uint16 per cell, row-major; EMPTY = no object
    dirs: list[int] | None  # uint8 per cell, or None when the layer has no DATA chunk


def read_l(path: str | Path) -> list[Layer]:
    d = Path(path).read_bytes()
    if d[:8] != b"ACHTUNG!":
        raise ValueError(f"{path}: not a level file")
    pos = d.index(b"LAYR") + 8
    (n,) = struct.unpack_from("<H", d, pos)
    pos += 2
    layers = []
    for _ in range(n):
        w, h = struct.unpack_from("<II", d, pos)
        main = d.index(b"MAIN", pos)
        header = d[pos + 8 : main]
        (clen,) = struct.unpack_from("<I", d, main + 4)
        raw = zlib.decompress(d[main + 8 : main + 8 + clen])
        pos = main + 8 + clen
        tiles = list(struct.unpack(f"<{w * h}H", raw))
        dirs = None
        if d[pos : pos + 4] == b"DATA":
            (dlen,) = struct.unpack_from("<I", d, pos + 9)
            dirs = list(zlib.decompress(d[pos + 13 : pos + 13 + dlen]))
            pos += 13 + dlen
            assert len(dirs) == w * h
        layers.append(Layer(w, h, header, tiles, dirs))
    if pos != len(d):
        raise ValueError(f"{path}: {len(d) - pos} trailing bytes")
    return layers


def read_ld(path: str | Path) -> dict[str, dict[str, str]]:
    cp = configparser.RawConfigParser(strict=False, interpolation=None)
    cp.optionxform = str  # keys are case-sensitive in MF_read
    cp.read_string(Path(path).read_text(encoding="utf-8", errors="surrogateescape"))
    return {s: dict(cp[s]) for s in cp.sections()}
