#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""card.py — the share card, 1200×630, drawn from the same mirror math as the pages.

Four round mirrors and their reflections in each other, placed right, under the title.

    python3 tools/card.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures as F  # noqa: E402

SITE = Path(__file__).resolve().parent.parent / "build" / "site"
W, H = 1200, 630
BG = (7, 7, 11)
INK = (243, 239, 230)
HOT = (255, 200, 97)
MUTE = (179, 172, 158)
HUES = [(255, 179, 71), (143, 208, 255), (200, 166, 255), (255, 106, 94), (127, 224, 168), (255, 210, 122)]

COND = "/System/Library/Fonts/Avenir Next Condensed.ttc"
BODY = "/System/Library/Fonts/Avenir Next.ttc"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def build():
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    cx, cy, sc = 945 * S, 315 * S, 192 * S
    cs = F.pearls(F.ring(4, 0.995), 12, 0.0008)
    for x, y, r, d in sorted(cs, key=lambda t: -t[2]):
        pr = r * sc
        if pr < 0.8:
            continue
        col = HUES[d % len(HUES)]
        a = 245 if d == 0 else max(90, 230 - 14 * d)
        w = 5 if d == 0 else max(1, 4 - d // 2)
        X, Y = cx + x * sc, cy + y * sc
        ld.ellipse([X - pr, Y - pr, X + pr, Y + pr], outline=col + (a,), width=w)
    lay = lay.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(Image.new("RGBA", (W, H), BG + (255,)), lay)

    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = int(230 * max(0, 1 - x / (W * 0.62)))
        sd.line([(x, 0), (x, H)], fill=BG + (a,))
    img = Image.alpha_composite(img, scrim).convert("RGB")
    dr = ImageDraw.Draw(img, "RGBA")

    # a jewel, like the brand mark
    jx, jy, jr = 92, 96, 24
    dr.ellipse([jx - jr - 7, jy - jr - 7, jx + jr + 7, jy + jr + 7], fill=HOT + (60,))
    dr.ellipse([jx - jr, jy - jr, jx + jr, jy + jr], fill=(0, 0, 0), outline=HOT, width=5)
    dr.ellipse([jx - 11, jy - 12, jx - 4, jy - 5], fill=(255, 255, 255, 200))

    kick = font(COND, 30, index=2)
    title = font(COND, 118, index=2)
    sub = font(BODY, 33, index=0)
    tiny = font(BODY, 26, index=0)
    dr.text((140, 78), "A 'SPLAINER, DRAWN FROM THE MATH", font=kick, fill=HOT)
    dr.text((64, 150), "INDRA'S NET,", font=title, fill=INK)
    dr.text((64, 272), "DRAWN", font=title, fill=HOT)
    dr.text((68, 450), "Every jewel shows every jewel.", font=sub, fill=INK)
    dr.text((68, 492), "Read sixteen ways, drawn live from mirrors.", font=sub, fill=INK)
    dr.text((68, H - 58), "nanobotco.github.io/indras-net  ·  hongdam.net", font=tiny, fill=MUTE)

    SITE.mkdir(parents=True, exist_ok=True)
    out = SITE / "card.jpg"
    img.save(out, format="JPEG", quality=88, optimize=True)
    print(f"card → {out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
