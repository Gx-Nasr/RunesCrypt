import math

import tkinter as tk

from . import theme as th


def radial_image(size, color, base=None, power=2.4):
    base = base or th.BG
    img = tk.PhotoImage(width=size, height=size)
    cr, cg, cb = th.hex_to_rgb(color)
    br, bg_, bb = th.hex_to_rgb(base)
    half = (size - 1) / 2.0
    rows = []
    for y in range(size):
        dy = (y - half) / half
        row = []
        for x in range(size):
            dx = (x - half) / half
            d = math.sqrt(dx * dx + dy * dy)
            t = min(1.0, d ** power)
            row.append("#%02x%02x%02x" % (
                int(cr + (br - cr) * t),
                int(cg + (bg_ - cg) * t),
                int(cb + (bb - cb) * t),
            ))
        rows.append(" ".join(row))
    img.put("\n".join(rows))
    return img


def round_rect(c, x1, y1, x2, y2, r, **kw):
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    pts = [
        (x1 + r, y1), (x2 - r, y1),
        (x2, y1), (x2, y1 + r),
        (x2, y2 - r), (x2, y2),
        (x2 - r, y2), (x1 + r, y2),
        (x1, y2), (x1, y2 - r),
        (x1, y1 + r), (x1, y1),
    ]
    return c.create_polygon(pts, smooth=True, splinesteps=24, **kw)
