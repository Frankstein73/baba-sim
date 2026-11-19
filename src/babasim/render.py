"""Procedural renderer (own visual style, no game art): states and in-between frames of a turn.

Needs Pillow (`pip install babasim[render]`). Works on the engine snapshots kept by api.Game, so
the picture shows exactly what the perceptual view describes.
"""

from __future__ import annotations

import colorsys
import hashlib

from PIL import Image, ImageDraw, ImageFont

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


class Sprite:
    __slots__ = ("id", "name", "kind", "word", "cls", "facing", "x", "y", "dir", "z", "alpha", "state",
                 "ghost")

    def copy(self):
        s = Sprite()
        for k in self.__slots__:
            setattr(s, k, getattr(self, k))
        return s


class Renderer:
    def __init__(self, game, tile_px: int = 32, axes: bool = False, motion_hints: bool = False):
        self.game = game
        self.px = tile_px
        self.axes = axes
        self.hints = motion_hints

    # ---- sprites -----------------------------------------------------------------------
    def _sprite(self, uid, name, x, y, d, z, snap):
        kind, word, cls, facing = self.game._describe(name)
        s = Sprite()
        s.id, s.name, s.kind, s.word, s.cls, s.facing = uid, name, kind, word, cls, facing
        s.x, s.y, s.dir, s.z, s.alpha, s.ghost = x - 1, y - 1, d, z, 1.0, None
        s.state = self.game._text_state(snap, uid) if self.game.rules_mode != "none" else "lit"
        return s

    def _sprites(self, snap):
        return [self._sprite(u["id"], u["name"], u["x"], u["y"], u["dir"], u["z"], snap)
                for u in snap["units"] if not u["hidden"]]

    # ---- drawing -----------------------------------------------------------------------
    def _draw_sprite(self, img, s, ox, oy):
        px = self.px
        a = max(0.0, min(1.0, s.alpha))
        if a <= 0.01:
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
        img = Image.new("RGBA", (margin + w * px + panel, margin + h * px), BG + (255,))
        d = ImageDraw.Draw(img)
        for x in range(w + 1):
            d.line((margin + x * px, margin, margin + x * px, margin + h * px), fill=GRID)
        for y in range(h + 1):
            d.line((margin, margin + y * px, margin + w * px, margin + y * px), fill=GRID)
        if self.axes:
            f = _font(max(8, int(px * 0.34)))
            for x in range(w):
                d.text((margin + x * px + px * 0.3, 1), str(x), fill=(150, 156, 170), font=f)
            for y in range(h):
                d.text((2, margin + y * px + px * 0.25), str(y), fill=(150, 156, 170), font=f)
        for s in sorted(sprites, key=lambda s: (s.z, s.kind != "object")):
            if s.ghost is not None:
                self._draw_sprite(img, s.ghost, margin, margin)
            self._draw_sprite(img, s, margin, margin)
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

    def save_gif(self, path, frames_per_phase: int = 6, ms: int = 60):
        n = max(1, len(self._phases(self.game._anim[2])))
        total = n * frames_per_phase
        ims = [self.frame(i / total) for i in range(total + 1)]
        ims[0].save(path, save_all=True, append_images=ims[1:], duration=[ms] * total + [ms * 8], loop=0)
