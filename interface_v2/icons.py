import tkinter as tk


def _l(c, x1, y1, x2, y2, color, w):
    return c.create_line(x1, y1, x2, y2, fill=color, width=w,
                         capstyle=tk.ROUND, joinstyle=tk.ROUND)


def _w(size):
    return max(1.7, size / 9)


def search(c, cx, cy, s, color):
    w = _w(s)
    r = s * 0.28
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=w)
    a = s * 0.32
    _l(c, cx + r * 0.65, cy + r * 0.65, cx + a, cy + a, color, w)


def plus(c, cx, cy, s, color):
    w = _w(s)
    _l(c, cx - s * 0.27, cy, cx + s * 0.27, cy, color, w)
    _l(c, cx, cy - s * 0.27, cx, cy + s * 0.27, color, w)


def close(c, cx, cy, s, color):
    w = _w(s)
    d = s * 0.27
    _l(c, cx - d, cy - d, cx + d, cy + d, color, w)
    _l(c, cx - d, cy + d, cx + d, cy - d, color, w)


def check(c, cx, cy, s, color):
    w = _w(s)
    _l(c, cx - s * 0.24, cy + s * 0.02, cx - s * 0.05, cy + s * 0.2, color, w)
    _l(c, cx - s * 0.05, cy + s * 0.2, cx + s * 0.26, cy - s * 0.2, color, w)


def eye(c, cx, cy, s, color):
    w = _w(s)
    k = s * 0.40
    top = [(cx - k + 2 * k * (i / 20), cy - s * 0.20 * (4 * (i / 20) * (1 - i / 20))) for i in range(21)]
    bot = [(cx - k + 2 * k * (i / 20), cy + s * 0.20 * (4 * (i / 20) * (1 - i / 20))) for i in range(20, -1, -1)]
    c.create_polygon(top + bot, fill="", outline=color, width=w, smooth=True)
    r = s * 0.11
    c.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color, outline="")


def eye_off(c, cx, cy, s, color):
    eye(c, cx, cy, s, color)
    w = _w(s)
    _l(c, cx - s * 0.34, cy + s * 0.28, cx + s * 0.34, cy - s * 0.28, color, w)


def copy(c, cx, cy, s, color):
    w = _w(s)
    c.create_rectangle(cx - s * 0.14, cy - s * 0.22, cx + s * 0.24, cy + s * 0.18,
                       outline=color, width=w)
    c.create_rectangle(cx - s * 0.24, cy - s * 0.34, cx + s * 0.14, cy + s * 0.06,
                       outline=color, width=w)


def trash(c, cx, cy, s, color):
    w = _w(s)
    _l(c, cx - s * 0.3, cy - s * 0.3, cx + s * 0.3, cy - s * 0.3, color, w)
    _l(c, cx - s * 0.17, cy - s * 0.3, cx - s * 0.11, cy - s * 0.4, color, w)
    _l(c, cx + s * 0.17, cy - s * 0.3, cx + s * 0.11, cy - s * 0.4, color, w)
    _l(c, cx - s * 0.24, cy - s * 0.24, cx - s * 0.12, cy + s * 0.34, color, w)
    _l(c, cx + s * 0.24, cy - s * 0.24, cx + s * 0.12, cy + s * 0.34, color, w)
    _l(c, cx - s * 0.12, cy + s * 0.34, cx + s * 0.12, cy + s * 0.34, color, w)
    _l(c, cx - s * 0.05, cy - s * 0.16, cx - s * 0.05, cy + s * 0.22, color, w)
    _l(c, cx + s * 0.09, cy - s * 0.16, cx + s * 0.09, cy + s * 0.22, color, w)


def edit(c, cx, cy, s, color):
    w = _w(s)
    _l(c, cx - s * 0.32, cy + s * 0.3, cx + s * 0.06, cy - s * 0.24, color, w)
    _l(c, cx - s * 0.18, cy + s * 0.16, cx + s * 0.2, cy - s * 0.38, color, w)
    _l(c, cx - s * 0.32, cy + s * 0.3, cx - s * 0.14, cy + s * 0.24, color, w)
    _l(c, cx + s * 0.2, cy - s * 0.38, cx + s * 0.3, cy - s * 0.28, color, w)
    _l(c, cx + s * 0.2, cy - s * 0.38, cx + s * 0.08, cy - s * 0.32, color, w)
    _l(c, cx - s * 0.14, cy + s * 0.24, cx + s * 0.08, cy - s * 0.32, color, w)


def logout(c, cx, cy, s, color):
    w = _w(s)
    c.create_rectangle(cx - s * 0.3, cy - s * 0.3, cx - s * 0.04, cy + s * 0.3,
                       outline=color, width=w)
    _l(c, cx + s * 0.04, cy, cx + s * 0.32, cy, color, w)
    _l(c, cx + s * 0.2, cy - s * 0.15, cx + s * 0.32, cy, color, w)
    _l(c, cx + s * 0.2, cy + s * 0.15, cx + s * 0.32, cy, color, w)


def user(c, cx, cy, s, color):
    w = _w(s)
    c.create_oval(cx - s * 0.13, cy - s * 0.34, cx + s * 0.13, cy - s * 0.06,
                  outline=color, width=w)
    c.create_arc(cx - s * 0.28, cy - s * 0.02, cx + s * 0.28, cy + s * 0.4,
                 start=180, extent=180, outline=color, width=w, style=tk.ARC)


def shield(c, cx, cy, s, color):
    w = _w(s)
    pts = [(cx, cy - s * 0.36), (cx + s * 0.28, cy - s * 0.22), (cx + s * 0.28, cy + s * 0.02),
           (cx, cy + s * 0.34), (cx - s * 0.28, cy + s * 0.02), (cx - s * 0.28, cy - s * 0.22)]
    c.create_polygon(pts, fill="", outline=color, width=w, smooth=True)
    _l(c, cx - s * 0.1, cy + s * 0.02, cx - s * 0.02, cy + s * 0.12, color, w)
    _l(c, cx - s * 0.02, cy + s * 0.12, cx + s * 0.14, cy - s * 0.12, color, w)


def lock(c, cx, cy, s, color):
    w = _w(s)
    c.create_arc(cx - s * 0.19, cy - s * 0.36, cx + s * 0.19, cy + s * 0.04,
                 start=0, extent=180, outline=color, width=w, style=tk.ARC)
    c.create_rectangle(cx - s * 0.26, cy - s * 0.04, cx + s * 0.26, cy + s * 0.36,
                       outline=color, width=w)
    r = s * 0.05
    c.create_oval(cx - r, cy + s * 0.09, cx + r, cy + s * 0.19, fill=color, outline="")


def key(c, cx, cy, s, color):
    w = _w(s)
    c.create_oval(cx - s * 0.22, cy - s * 0.32, cx + s * 0.0, cy - s * 0.06,
                  outline=color, width=w)
    _l(c, cx - s * 0.08, cy - s * 0.19, cx + s * 0.32, cy + s * 0.3, color, w)
    _l(c, cx + s * 0.32, cy + s * 0.3, cx + s * 0.38, cy + s * 0.24, color, w)
    _l(c, cx + s * 0.12, cy - s * 0.02, cx + s * 0.22, cy + s * 0.1, color, w)
    _l(c, cx + s * 0.22, cy - s * 0.02, cx + s * 0.32, cy + s * 0.1, color, w)


def refresh(c, cx, cy, s, color):
    w = _w(s)
    c.create_arc(cx - s * 0.3, cy - s * 0.3, cx + s * 0.3, cy + s * 0.3,
                 start=0, extent=300, outline=color, width=w, style=tk.ARC)
    a = s * 0.3
    x = cx + a * 0.5
    y = cy - a * 0.866
    _l(c, x - s * 0.12, y - s * 0.14, x, y, color, w)
    _l(c, x, y, x + s * 0.18, y - s * 0.06, color, w)


def shield_alert(c, cx, cy, s, color):
    w = _w(s)
    pts = [(cx, cy - s * 0.36), (cx + s * 0.28, cy - s * 0.22), (cx + s * 0.28, cy + s * 0.02),
           (cx, cy + s * 0.34), (cx - s * 0.28, cy + s * 0.02), (cx - s * 0.28, cy - s * 0.22)]
    c.create_polygon(pts, fill="", outline=color, width=w, smooth=True)
    _l(c, cx, cy - s * 0.18, cx, cy + s * 0.06, color, w)
    r = s * 0.05
    c.create_oval(cx - r, cy + s * 0.13, cx + r, cy + s * 0.23, fill=color, outline="")


def arrow_right(c, cx, cy, s, color):
    w = _w(s)
    _l(c, cx - s * 0.22, cy, cx + s * 0.22, cy, color, w)
    _l(c, cx + s * 0.1, cy - s * 0.15, cx + s * 0.22, cy, color, w)
    _l(c, cx + s * 0.1, cy + s * 0.15, cx + s * 0.22, cy, color, w)


_ICONS = {
    "search": search,
    "plus": plus,
    "close": close,
    "check": check,
    "eye": eye,
    "eye_off": eye_off,
    "copy": copy,
    "trash": trash,
    "edit": edit,
    "logout": logout,
    "user": user,
    "shield": shield,
    "lock": lock,
    "key": key,
    "refresh": refresh,
    "shield_alert": shield_alert,
    "arrow_right": arrow_right,
}


def draw(name, c, cx, cy, s, color):
    fn = _ICONS.get(name)
    if fn:
        fn(c, cx, cy, s, color)


def avatar(c, cx, cy, r, text, bg_color, fg_color, font):
    c.create_oval(cx - r, cy - r, cx + r, cy + r, fill=bg_color, outline="")
    c.create_text(cx, cy, text=(text[:1].upper() if text else "?"), font=font, fill=fg_color)
