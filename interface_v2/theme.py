import tkinter as tk
import tkinter.font as tkfont

BG        = "#0a0d1d"
BG_TOP    = "#141a3a"
SURFACE   = "#151a34"
SURFACE_2 = "#1c2244"
SURFACE_3 = "#20274e"
BORDER    = "#252d55"
BORDER_2  = "#38417c"

ACCENT    = "#7b6cf6"
ACCENT_L  = "#9487ff"
ACCENT_D  = "#6655e0"
ACCENT_2  = "#b088ff"
TEAL      = "#4ee6c8"
TEAL_D    = "#2fb89d"

TEXT      = "#eef1ff"
MUTED     = "#9aa2cc"
FAINT     = "#5d6490"

SUCCESS   = "#3ddc97"
DANGER    = "#ff5c7a"
DANGER_BG = "#3a1722"
WARNING   = "#ffb86b"

AVATAR_COLORS = [
    "#7b6cf6", "#4ee6c8", "#ff6b81", "#f6c453",
    "#5aa9f6", "#c57bf6", "#ff8a4e", "#7bf6a9",
    "#f66e9b", "#8fd460",
]

_FAMILY = "Helvetica"
_MONO_FAMILY = "Courier"
_ROOT = None


def init_fonts(root):
    global _FAMILY, _MONO_FAMILY, _ROOT
    _ROOT = root
    fams = set(tkfont.families(root))
    for f in ("Noto Sans", "DejaVu Sans", "Liberation Sans", "Helvetica", "Arial"):
        if f in fams:
            _FAMILY = f
            break
    for f in ("DejaVu Sans Mono", "Noto Sans Mono", "Liberation Mono", "Courier"):
        if f in fams:
            _MONO_FAMILY = f
            break


def family():
    return _FAMILY


def mono_family():
    return _MONO_FAMILY


def F(size, weight="normal"):
    return (_FAMILY, size, weight)


def MONO(size, weight="normal"):
    return (_MONO_FAMILY, size, weight)


_font_cache = {}


def _font(size, weight):
    key = (size, weight)
    if key not in _font_cache:
        _font_cache[key] = tkfont.Font(_ROOT, family=_FAMILY, size=size, weight=weight)
    return _font_cache[key]


def measure(text, size, weight="normal"):
    return _font(size, weight).measure(text)


def ellipsize(text, size, weight, max_w):
    if not text:
        return ""
    if measure(text, size, weight) <= max_w:
        return text
    s = text
    while s and measure(s + "\u2026", size, weight) > max_w:
        s = s[:-1]
    return s + "\u2026"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in rgb)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((lerp(r1, r2, t), lerp(g1, g2, t), lerp(b1, b2, t)))


def avatar_color(key):
    if not key:
        return ACCENT
    total = sum(ord(c) for c in str(key))
    return AVATAR_COLORS[total % len(AVATAR_COLORS)]
