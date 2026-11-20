"""Renderer: states and in-between frames of a turn.

`style="game"` (default) draws the game's own sprites and palettes, exported once into
data/sprites.zip; `style="plain"` is a procedural look that needs no art. Needs Pillow
(`pip install babasim[render]`). Works on the engine snapshots kept by api.Game, so the picture
shows exactly what the perceptual view describes.
"""

from __future__ import annotations

import colorsys
import hashlib
import io
import struct
import zipfile
from functools import lru_cache

from PIL import Image, ImageChops, ImageDraw, ImageFont

from babasim.runtime import DATA

BG = (21, 24, 31)
GRID = (30, 34, 43)
PALETTE = {
    "baba": (240, 240, 240), "keke": (229, 83, 59), "me": (142, 94, 156), "wall": (72, 82, 104),
    "rock": (194, 158, 70), "flag": (237, 226, 133), "water": (95, 157, 209), "lava": (228, 153, 80),
    "grass": (75, 122, 60), "tile": (36, 40, 52), "skull": (130, 38, 28), "key": (237, 226, 133),
    "door": (229, 83, 59), "hedge": (62, 118, 80), "ice": (160, 214, 230), "love": (235, 145, 202),
    "star": (237, 226, 133), "brick": (98, 70, 52), "flower": (145, 131, 215), "tree": (92, 131, 57),
    "box": (144, 103, 62), "belt": (95, 157, 209), "bog": (95, 131, 100), "crab": (229, 83, 59),
    "jelly": (95, 157, 209), "algae": (92, 131, 57), "pillar": (115, 115, 115), "cog": (115, 115, 115),
}
FLAT = {"tile", "grass", "water", "lava", "ice", "bog", "brick", "rubble", "algae"}  # ground-like
CLASS_COLOR = {"verb": (240, 240, 240), "and": (240, 240, 240), "not": (229, 83, 59),
               "condition": (160, 214, 230), "prefix": (160, 214, 230)}
DIRS = {0: (1, 0), 1: (0, -1), 2: (-1, 0), 3: (0, 1)}
_fonts = {}
SPRITE_PX = 24
_zip = None


def _asset(path):
    """Bytes of a file in the exported art, or None."""
    global _zip
    if _zip is None:
        _zip = zipfile.ZipFile(DATA / "sprites.zip") if (DATA / "sprites.zip").exists() else False
    if not _zip:
        return None
    try:
        return _zip.read(path)
    except KeyError:
        return None


@lru_cache(maxsize=None)
def _palette(name, world):
    data = _asset(f"Worlds/{world}/Palettes/{name}") or _asset(f"Palettes/{name}") or _asset("Palettes/default.png")
    return Image.open(io.BytesIO(data)).convert("RGB") if data else None


@lru_cache(maxsize=None)
def _tile(sprite, n, root, world, color, px):
    """Sprite frame `n` tinted with `color` at `px` pixels per tile; None when the art lacks it."""
    data = None
    for k in (n, 0):
        if not root:
            data = _asset(f"Worlds/{world}/Sprites/{sprite}_{k}_1.png")
        data = data or _asset(f"Sprites/{sprite}_{k}_1.png") or _asset(f"Worlds/{world}/Sprites/{sprite}_{k}_1.png")
        if data:
            break
    if not data:
        return None
    im = Image.open(io.BytesIO(data))
    if im.mode == "RGBA":
        lum, alpha = im.convert("L"), im.getchannel("A")
    else:  # opaque sprites are white on black: brightness is coverage
        lum = im.convert("L")
        alpha = lum
        lum = Image.new("L", im.size, 255)
    out = Image.merge("RGBA", (*[lum.point(lambda v, c=c: v * c // 255) for c in color], alpha))
    if px != out.size[0]:
        out = out.resize((px * out.size[0] // SPRITE_PX, px * out.size[1] // SPRITE_PX), Image.NEAREST)
    return out


def color_of(name):
    c = PALETTE.get(name)
    if c is None:
        h = int(hashlib.md5(name.encode()).hexdigest()[:6], 16)
        r, g, b = colorsys.hls_to_rgb((h % 360) / 360, 0.6, 0.5 + (h >> 9) % 30 / 100)
        c = (int(r * 255), int(g * 255), int(b * 255))
    return c


def _font(size):
    f = _fonts.get(size)
    if f is None:
        try:
            f = ImageFont.load_default(size)
        except TypeError:  # Pillow < 10.1
            f = ImageFont.load_default()
        _fonts[size] = f
    return f


def _mix(c, bg, a):
    return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))


def _label(draw, box, text, fill, px):
    """Centered text, split over two lines when long (as the game's word tiles are)."""
    x0, y0, x1, y1 = box
    lines = [text] if len(text) <= 3 else [text[: (len(text) + 1) // 2], text[(len(text) + 1) // 2 :]]
    size = max(6, int(px * (0.5 if len(lines) == 1 else 0.42)))
    longest = max(len(s) for s in lines)
    size = min(size, int((x1 - x0) * 1.55 / max(longest, 1)))
    font = _font(max(size, 6))
    total = len(lines) * size
    y = (y0 + y1) / 2 - total / 2
    for s in lines:
        w = draw.textlength(s, font=font)
        draw.text(((x0 + x1) / 2 - w / 2, y - size * 0.12), s, fill=fill, font=font)
        y += size


class _Neighbours:
    def __init__(self, cells, w, h):
        self.cells, self.w, self.h = cells, w, h

    def __contains__(self, key):
        _name, x, y = key
        return not (0 <= x < self.w and 0 <= y < self.h) or key in self.cells


class Sprite:
    __slots__ = ("id", "name", "kind", "word", "cls", "facing", "x", "y", "dir", "z", "alpha", "state",
                 "ghost", "look")

    def copy(self):
        s = Sprite()
        for k in self.__slots__:
            setattr(s, k, getattr(self, k))
        return s


class Renderer:
    def __init__(self, game, tile_px: int = 48, axes: bool = False, motion_hints: bool = False,
                 style: str = "game"):
        self.game = game
        self.px = tile_px
        self.axes = axes
        self.hints = motion_hints
        self.style = style if _asset("Palettes/default.png") else "plain"

    # ---- game art ------------------------------------------------------------------------
    def _look(self, name):
        """(sprite, in_root, tiling, colour, active colour) of an object name in this level."""
        key = ("look", name)
        info = self.game._info.get(key)
        if info is None:
            G = self.game.engine.G
            cls = G["unitreference"][name]
            if cls is None or cls == "level":
                info = False
            else:
                get = lambda k: G["getactualdata_objlist"](cls, k)[0]  # noqa: E731

                def colour(k):
                    c = get(k)
                    return (int(c[1]), int(c[2])) if c is not None else None

                base = colour("colour") or (0, 3)
                info = (get("sprite") or name, bool(get("sprite_in_root")), get("tiling"), base, colour("active") or base)
            self.game._info[key] = info
        return info

    def _rgb(self, xy):
        ld = self.game.engine.ld.get("general", {})
        pal = _palette(ld.get("palette", "default.png"), self.game.world)
        x, y = xy
        return pal.getpixel((min(x, pal.size[0] - 1), min(y, pal.size[1] - 1)))

    def _game_tile(self, s, neighbours):
        look = s.look
        if not look:
            return None
        sprite, root, tiling, colour, active = look
        if tiling == 1:  # joins with neighbours of its kind: right 1, up 2, left 4, down 8
            x, y = round(s.x), round(s.y)
            n = sum(bit for bit, (dx, dy) in ((1, (1, 0)), (2, (0, -1)), (4, (-1, 0)), (8, (0, 1)))
                    if (s.name, x + dx, y + dy) in neighbours)
        elif tiling in (0, 2, 3):
            n = (s.dir if s.dir in DIRS else 0) * 8
        else:
            n = 0
        lit = s.kind == "object" or s.state != "dim"
        return _tile(sprite, n, root, self.game.world, self._rgb(active if lit and s.kind != "object" else colour),
                     self.px)

    # ---- sprites -----------------------------------------------------------------------
    def _sprite(self, uid, name, x, y, d, z, snap):
        kind, word, cls, facing = self.game._describe(name)
        s = Sprite()
        s.id, s.name, s.kind, s.word, s.cls, s.facing = uid, name, kind, word, cls, facing
        s.x, s.y, s.dir, s.z, s.alpha, s.ghost = x - 1, y - 1, d, z, 1.0, None
        s.look = self._look(name) if self.style == "game" else None
        s.state = self.game._text_state(snap, uid) if self.game.rules_mode != "none" else "lit"
        return s

    def _sprites(self, snap):
        return [self._sprite(u["id"], u["name"], u["x"], u["y"], u["dir"], u["z"], snap)
                for u in snap["units"] if not u["hidden"]]

    # ---- drawing -----------------------------------------------------------------------
    def _draw_sprite(self, img, s, ox, oy, neighbours=frozenset()):
        px = self.px
        a = max(0.0, min(1.0, s.alpha))
        if a <= 0.01:
            return
        tile = self._game_tile(s, neighbours) if self.style == "game" else None
        if tile is not None:
            if a < 0.99:
                tile = tile.copy()
                tile.putalpha(tile.getchannel("A").point(lambda v: int(v * a)))
            x0, y0 = round(ox + s.x * px), round(oy + s.y * px)
            img.alpha_composite(tile, (max(x0, 0), max(y0, 0)),
                                (max(-x0, 0), max(-y0, 0), tile.size[0], tile.size[1]))
            if s.state == "crossed" and s.kind != "object":
                d = ImageDraw.Draw(img)
                w = max(2, px // 12)
                d.line((x0 + 3, y0 + 3, x0 + px - 4, y0 + px - 4), fill=(229, 83, 59), width=w)
                d.line((x0 + px - 4, y0 + 3, x0 + 3, y0 + px - 4), fill=(229, 83, 59), width=w)
            return
        layer = img if a >= 0.99 else Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        x0, y0 = ox + s.x * px, oy + s.y * px
        box = (x0 + 1, y0 + 1, x0 + px - 2, y0 + px - 2)
        if s.kind == "object":
            c = color_of(s.word)
            if s.word in FLAT:
                d.rectangle((x0, y0, x0 + px - 1, y0 + px - 1), fill=_mix(c, BG, 0.75))
                _label(d, box, s.word[:4], _mix(c, (255, 255, 255), 0.22), px * 0.7)
            else:
                d.rounded_rectangle(box, radius=px // 5, fill=c)
                ink = (20, 20, 24) if sum(c) > 380 else (240, 240, 240)
                _label(d, box, s.word[:6], ink, px * 0.8)
                if s.facing and s.dir in DIRS:
                    dx, dy = DIRS[s.dir]
                    cx, cy = x0 + px / 2 + dx * px * 0.36, y0 + px / 2 + dy * px * 0.36
                    r = px * 0.13
                    tri = [(cx + dx * r, cy + dy * r), (cx - dx * r + dy * r, cy - dy * r + dx * r),
                           (cx - dx * r - dy * r, cy - dy * r - dx * r)]
                    d.polygon(tri, fill=ink)
        else:
            base = color_of(s.word) if s.cls in ("noun", "property", None) else CLASS_COLOR[s.cls]
            if sum(base) < 420:  # dark object colours would read as "dim"
                base = _mix(base, (255, 255, 255), 0.5)
            c = base if s.state != "dim" else _mix(base, BG, 0.42)
            if s.kind == "letter":
                _label(d, box, s.word.upper(), c, px * 1.3)
            elif s.cls == "property":  # filled block with dark word, like the game's properties
                d.rounded_rectangle(box, radius=px // 8, fill=c)
                _label(d, box, s.word.upper(), BG, px)
            else:
                _label(d, box, s.word.upper(), c, px)
            if s.state == "crossed":
                d.line((x0 + 3, y0 + 3, x0 + px - 4, y0 + px - 4), fill=(229, 83, 59), width=max(2, px // 12))
                d.line((x0 + px - 4, y0 + 3, x0 + 3, y0 + px - 4), fill=(229, 83, 59), width=max(2, px // 12))
        if layer is not img:
            alpha = layer.getchannel("A").point(lambda v: int(v * a))
            layer.putalpha(alpha)
            img.alpha_composite(layer)

    def _canvas(self, sprites, snap, hints=()):
        G = self.game.engine.G
        w, h = G["roomsizex"] - 2, G["roomsizey"] - 2
        px = self.px
        margin = int(px * 0.6) if self.axes else 0
        panel = int(px * 7) if self.game.rules_mode == "list" else 0
        game_style = self.style == "game"
        img = Image.new("RGBA", (margin + w * px + panel, margin + h * px), (self._rgb((1, 0)) if game_style else BG) + (255,))
        d = ImageDraw.Draw(img)
        if game_style:
            d.rectangle((margin, margin, margin + w * px - 1, margin + h * px - 1), fill=self._rgb((0, 4)))
        else:
            for x in range(w + 1):
                d.line((margin + x * px, margin, margin + x * px, margin + h * px), fill=GRID)
            for y in range(h + 1):
                d.line((margin, margin + y * px, margin + w * px, margin + y * px), fill=GRID)
        # the level edge and everything outside the field counts as "same kind" for joining sprites
        neighbours = _Neighbours({(s.name, round(s.x), round(s.y)) for s in sprites if s.look and s.look[2] == 1}, w, h)
        if self.axes:
            f = _font(max(8, int(px * 0.34)))
            for x in range(w):
                d.text((margin + x * px + px * 0.3, 1), str(x), fill=(150, 156, 170), font=f)
            for y in range(h):
                d.text((2, margin + y * px + px * 0.25), str(y), fill=(150, 156, 170), font=f)
        for s in sorted(sprites, key=lambda s: s.z):
            if s.ghost is not None:
                self._draw_sprite(img, s.ghost, margin, margin, neighbours)
            self._draw_sprite(img, s, margin, margin, neighbours)
        if self.hints:
            for (ax, ay), (bx, by) in hints:
                d.line((margin + (ax + 0.5) * px, margin + (ay + 0.5) * px,
                        margin + (bx + 0.5) * px, margin + (by + 0.5) * px), fill=(255, 255, 255), width=1)
        if panel:
            f = _font(max(9, int(px * 0.38)))
            x = margin + w * px + 8
            d.text((x, 6), "RULES", fill=(150, 156, 170), font=f)
            for i, r in enumerate(snap["rules"][: (h * px) // int(px * 0.5) - 2]):
                d.text((x, 6 + (i + 1.4) * px * 0.5), r["text"], fill=(240, 240, 240), font=f)
        return img, d, (margin, w * px, h * px)

    def _finish(self, img, d, geom, status):
        margin, W, H = geom
        if status == "won":
            for i in range(max(3, self.px // 8)):
                d.rectangle((margin + i, margin + i, margin + W - 1 - i, margin + H - 1 - i), outline=(237, 226, 133))
        elif status != "playing":
            for i in range(max(3, self.px // 8)):
                d.rectangle((margin + i, margin + i, margin + W - 1 - i, margin + H - 1 - i), outline=(229, 83, 59))
        return img.convert("RGB")

    def state_image(self, snap=None) -> Image.Image:
        snap = snap or self.game.last
        img, d, geom = self._canvas(self._sprites(snap), snap)
        return self._finish(img, d, geom, snap["status"])

    # ---- in-between frames -------------------------------------------------------------
    def _phases(self, events):
        phases = {}
        for e in events:
            if e["type"] in ("move", "teleport", "turn", "destroy", "create", "transform"):
                phases.setdefault(e["phase"], []).append(e)
        return [phases[k] for k in sorted(phases)]

    def _find(self, sprites, e, name=None, pos=None):
        uid = e.get("id")
        for s in sprites:
            if s.id == uid and s.alpha > 0:
                return s
        if name is not None:
            for s in sprites:
                if s.name == name and (round(s.x), round(s.y)) == tuple(pos) and s.alpha > 0:
                    return s
        return None

    @staticmethod
    def _refname(ref):
        return ref["name"] if ref["kind"] == "object" else "text_" + (ref.get("word") or ref.get("letter"))

    def _apply(self, sprites, phase, u, snap, hints):
        """Advance `sprites` through one phase; u in [0,1] is the progress within it."""
        for e in phase:
            t = e["type"]
            if t in ("move", "teleport"):
                s = self._find(sprites, e, self._refname(e["what"]), e["from"])
                if s is None:
                    continue
                (fx, fy), (tx, ty) = e["from"], e["to"]
                if t == "move":
                    s.x, s.y = fx + (tx - fx) * u, fy + (ty - fy) * u
                    hints.append(((fx, fy), (s.x, s.y)))
                elif u < 1:
                    g = s.copy()
                    g.ghost, g.alpha = None, 1 - u
                    s.ghost = g
                    s.x, s.y, s.alpha = tx, ty, u
                else:
                    s.x, s.y, s.alpha, s.ghost = tx, ty, 1.0, None
            elif t == "turn":
                s = self._find(sprites, e, self._refname(e["what"]), e["what"]["pos"])
                if s is not None and u >= 0.5:
                    s.dir = {"right": 0, "up": 1, "left": 2, "down": 3}.get(e["to"], s.dir)
            elif t == "destroy":
                s = self._find(sprites, e, self._refname(e["what"]), e["what"]["pos"])
                if s is not None:
                    s.alpha = 1 - u
            elif t == "create":
                x, y = e["what"]["pos"]
                s = self._sprite(e.get("id"), self._refname(e["what"]), x + 1, y + 1, 3, 15, snap)
                s.alpha = u
                sprites.append(s)
            elif t == "transform":
                old, new = self._refname(e["from"]), self._refname(e["to"])
                s = self._find(sprites, {"id": None}, old, e["pos"])
                if s is None:
                    continue
                n = self._sprite(e.get("id"), new, e["pos"][0] + 1, e["pos"][1] + 1, s.dir, s.z, snap)
                n.alpha = u
                if u < 1:
                    s.alpha = 1 - u
                    n.ghost = s.copy()
                sprites[sprites.index(s)] = n

    def frame(self, t: float) -> Image.Image:
        """Picture at time t of the last step: 0 = before, 1 = after; phases play one after another."""
        before, after, events = self.game._anim
        phases = self._phases(events)
        if t >= 1 or not phases:
            return self.state_image(after if t >= 1 or not phases and t > 0 else before)
        if t <= 0:
            return self.state_image(before)
        pos = t * len(phases)
        k = min(int(pos), len(phases) - 1)
        sprites = self._sprites(before)
        hints = []
        for i in range(k):
            self._apply(sprites, phases[i], 1.0, before, [])
            sprites = [s for s in sprites if s.alpha > 0]
        self._apply(sprites, phases[k], pos - k, before, hints)
        img, d, geom = self._canvas(sprites, before, hints)
        return self._finish(img, d, geom, "playing")

    def frames(self, mode="phases", dedupe: bool = False):
        """[(t, image)] for the last step. mode: 'endpoints' | 'phases' | int n."""
        n = len(self._phases(self.game._anim[2]))
        if mode == "endpoints":
            ts = [0.0, 1.0]
        elif mode == "phases":
            ts = [0.0] + [x for k in range(n) for x in ((k + 0.5) / n, (k + 1) / n)] if n else [0.0, 1.0]
        else:
            ts = [i / (int(mode) - 1) for i in range(int(mode))] if int(mode) > 1 else [1.0]
        out = [(round(t, 4), self.frame(t)) for t in ts]
        if dedupe:
            kept = []
            for t, im in out:
                if not kept or im.tobytes() != kept[-1][1].tobytes():
                    kept.append((t, im))
            out = kept
        return out

    def step_frames(self, per_phase: int = 2) -> list[Image.Image]:
        """In-between and end pictures of the last step, without its starting picture."""
        n = len(self._phases(self.game._anim[2]))
        if n == 0:
            return [self.frame(1.0)]
        total = n * per_phase
        return [self.frame(i / total) for i in range(1, total + 1)]

    def save_gif(self, path, frames_per_phase: int = 6, ms: int = 60):
        n = max(1, len(self._phases(self.game._anim[2])))
        total = n * frames_per_phase
        ims = [self.frame(i / total) for i in range(total + 1)]
        ims[0].save(path, save_all=True, append_images=ims[1:], duration=[ms] * total + [ms * 8], loop=0)


def gif_bytes(frames: list[Image.Image], ms: int = 110, hold_ms: int = 1500) -> bytes:
    """Animated GIF of `frames`; the last one is held so the end state can be read."""
    palette = frames[-1].quantize(colors=255, method=Image.MEDIANCUT, dither=Image.NONE)
    paletted = [f.quantize(palette=palette, dither=Image.NONE) for f in frames]
    buf = io.BytesIO()
    paletted[0].save(buf, "GIF", save_all=True, append_images=paletted[1:], loop=0, optimize=False,
                     duration=[ms] * (len(frames) - 1) + [hold_ms])
    return buf.getvalue()


def _gif_image(data: bytes) -> tuple[bytes, int, bytes]:
    """(colour table, interlace flag, LZW data) of the first image in a GIF file."""
    flags, pos, table = data[10], 13, b""
    if flags & 0x80:
        n = 3 * (2 << (flags & 7))
        table, pos = data[pos:pos + n], pos + n

    def blocks(at):
        while data[at]:
            at += data[at] + 1
        return at + 1

    while data[pos] == 0x21:  # extensions
        pos = blocks(pos + 2)
    assert data[pos] == 0x2C, "no image in GIF"
    flags, pos = data[pos + 9], pos + 10
    if flags & 0x80:
        n = 3 * (2 << (flags & 7))
        table, pos = data[pos:pos + n], pos + n
    return table, flags & 0x40, data[pos:blocks(pos + 1)]


class GifWriter:
    """An animated GIF built one frame at a time.

    Of each frame only the rectangle that differs from the frame before is kept, already compressed, so a
    long animation needs the memory of one picture and not of all of them. A frame equal to the one before
    lengthens it.
    """

    def __init__(self, ms: int = 110):
        self.ms = ms
        self.size = None
        self._last = None
        self._frames = []  # [delay in 1/100 s, box, colour table, interlace flag, LZW data]

    def add(self, frame: Image.Image, ms: int | None = None) -> None:
        frame = frame.convert("RGB")
        delay = round((self.ms if ms is None else ms) / 10)
        if self._last is None:
            self.size, box = frame.size, (0, 0, *frame.size)
        else:
            box = ImageChops.difference(self._last, frame).getbbox()
            if box is None:
                self._frames[-1][0] += delay
                return
        self._last = frame
        part = frame.crop(box).quantize(colors=256, method=Image.MEDIANCUT, dither=Image.NONE)
        buf = io.BytesIO()
        part.save(buf, "GIF", optimize=False, interlace=0)
        self._frames.append([delay, box, *_gif_image(buf.getvalue())])

    def hold(self, ms: int) -> None:
        """Show the latest frame for `ms`."""
        self._frames[-1][0] = round(ms / 10)

    def getvalue(self) -> bytes:
        w, h = self.size
        out = [b"GIF89a", struct.pack("<HHBBB", w, h, 0x70, 0, 0),
               b"\x21\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00"]  # loop forever
        for delay, (x0, y0, x1, y1), table, interlace, data in self._frames:
            bits = (len(table) // 3).bit_length() - 2
            out += [struct.pack("<BBBBHBB", 0x21, 0xF9, 4, 0x04, min(delay, 0xFFFF), 0, 0),  # keep the frame in place
                    struct.pack("<BHHHHB", 0x2C, x0, y0, x1 - x0, y1 - y0, 0x80 | interlace | bits), table, data]
        return b"".join(out) + b"\x3b"
