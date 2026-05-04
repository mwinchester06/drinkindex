#!/usr/bin/env python3
"""Remove near-black/opaque black matte from PNG corners for transparent web export."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image


def remove_black_matte(im: Image.Image, black_end: float = 34.0, fade_end: float = 88.0) -> Image.Image:
    """Pixels close to black become transparent; soft fringe between black_end and fade_end."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    span = max(fade_end - black_end, 1e-6)

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            d = math.sqrt(r * r + g * g + b * b)
            if d <= black_end:
                px[x, y] = (r, g, b, 0)
            elif d < fade_end:
                t = (d - black_end) / span
                na = int(a * max(0.0, min(1.0, t)))
                px[x, y] = (r, g, b, na)
    return im


def main() -> None:
    root = Path(__file__).resolve().parent.parent / "assets"
    names = [
        "mainstar.png",
        "p3-mug-picker-chip.png",
        "hp-star-a.png",
        "hp-star-b.png",
        "profile-star-a.png",
        "profile-star-b.png",
    ]
    for name in names:
        path = root / name
        if not path.exists():
            print("skip (missing)", path.name)
            continue
        im = Image.open(path)
        out = remove_black_matte(im)
        out.save(path, "PNG", optimize=True)
        print("updated", path.name)


if __name__ == "__main__":
    main()
