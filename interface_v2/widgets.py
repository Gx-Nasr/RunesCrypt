import math

import tkinter as tk

from . import theme as th
from . import icons
from . import fx
from .animations import tween


def _fade(color, amount):
    return th.lerp_color(color, th.BG, amount)


VARIANTS = {
    "primary": {
        "fill": th.ACCENT, "fill_hover": th.ACCENT_L, "fill_press": th.ACCENT_D,
        "text": "#ffffff", "text_hover": "#ffffff",
        "outline": None, "outline_hover": None,
    },
    "secondary": {
        "fill": th.SURFACE_2, "fill_hover": th.SURFACE_2, "fill_press": th.SURFACE,
        "text": th.TEXT, "text_hover": th.TEXT,
        "outline": th.BORDER_2, "outline_hover": th.ACCENT,
    },
    "subtle": {
        "fill": th.BG, "fill_hover": th.SURFACE_2, "fill_press": th.SURFACE,
        "text": th.MUTED, "text_hover": th.TEXT,
        "outline": None, "outline_hover": th.BORDER_2,
    },
    "danger": {
        "fill": th.DANGER, "fill_hover": "#ff7089", "fill_press": "#e04763",
        "text": "#ffffff", "text_hover": "#ffffff",
        "outline": None, "outline_hover": None,
    },
}


class RoundedButton(tk.Canvas):
    def __init__(self, master, text="", command=None, *, variant="primary", height=48,
                 radius=14, font_size=15, icon=None, bg=th.BG, text_color=None,
                 width=None, disabled=False):
        super().__init__(master, height=height, bg=bg, highlightthickness=0, bd=0)
        self._command = command
        self._variant = variant
        self._radius = radius
        self._text = text
        self._icon = icon
        self._font = th.F(font_size, "bold")
        self._bg = bg
        self._hp = 0.0
        self._pressed = False
        self._loading = False
        self._disabled = disabled
        self._spin = 0
        self._text_color = text_color
        if width:
            self.config(width=width)
        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        if not disabled:
            self.config(cursor="hand2")
        self._redraw()

    def _v(self):
        return VARIANTS.get(self._variant, VARIANTS["primary"])

    def _on_enter(self, e):
        if self._disabled or self._loading:
            return
        tween(self, 8, lambda t: setattr(self, "_hp", t) or self._redraw())

    def _on_leave(self, e):
        if self._disabled or self._loading:
            return
        tween(self, 8, lambda t: setattr(self, "_hp", 1 - t) or self._redraw())

    def _on_press(self, e):
        if self._disabled or self._loading:
            return
        self._pressed = True
        self._redraw()

    def _on_release(self, e):
        if self._disabled or self._loading:
            return
        self._pressed = False
        self._redraw()
        if self._command:
            self._command()

    def set_loading(self, loading):
        self._loading = bool(loading)
        if loading:
            self._spin = 0
            self._spin_loop()
        self._redraw()

    def _spin_loop(self):
        if not self._loading:
            return
        self._spin = (self._spin + 16) % 360
        self._redraw()
        self.after(30, self._spin_loop)

    def set_text(self, text):
        self._text = text
        self._redraw()

    def set_disabled(self, disabled):
        self._disabled = bool(disabled)
        self.config(cursor="arrow" if disabled else "hand2")
        self._redraw()

    def _redraw(self):
        self.delete("all")
        v = self._v()
        w = self.winfo_width() or self.winfo_reqwidth()
        h = self.winfo_height() or self._height
        if w <= 1 or h <= 1:
            return

        if self._disabled:
            fill = _fade(v["fill"], 0.55)
            text_col = th.MUTED
            outline = None
        else:
            base = v["fill_press"] if self._pressed else v["fill"]
            hover = v["fill_hover"]
            fill = th.lerp_color(base, hover, self._hp)
            text_col = v["text_hover"] if self._hp > 0.5 else v["text"]
            if self._pressed:
                text_col = v["text_hover"]
            outline = v["outline_hover"] if self._hp > 0.5 else v["outline"]

        if self._text_color:
            text_col = self._text_color

        fx.round_rect(self, 1, 1, w - 1, h - 1, self._radius,
                      fill=fill, outline=outline or "", width=1)
        if v["outline"]:
            fx.round_rect(self, 1, 1, w - 1, h - 1, self._radius,
                          fill="", outline=outline or v["outline"], width=1)

        dy = 1 if self._pressed else 0
        if self._loading:
            color = text_col
            self.create_arc(w / 2 - 11, h / 2 - 11 + dy, w / 2 + 11, h / 2 + 11 + dy,
                            start=self._spin, extent=300, style=tk.ARC, outline=color, width=3)
            return

        content = []
        icon_w = 0
        if self._icon:
            icon_w = 20
            content.append(icon_w + 10)
        text_w = th.measure(self._text, 15, "bold")
        content.append(text_w)
        total = sum(content)

        x0 = (w - total) / 2
        cy = h / 2 + dy
        if self._icon:
            icons.draw(self._icon, self, x0 + icon_w / 2, cy, 16, text_col)
            tx = x0 + icon_w + 10
        else:
            tx = x0

        max_tw = w - 32
        label = th.ellipsize(self._text, 15, "bold", max_tw)
        self.create_text(tx, cy, text=label, font=self._font, fill=text_col, anchor="w")



class IconButton(tk.Canvas):
    def __init__(self, master, icon, command, *, size=34, radius=11, icon_size=16,
                 bg=th.BG, color=th.MUTED, hover_color=th.TEXT,
                 hover_bg=th.SURFACE_2, active_bg=th.SURFACE):
        super().__init__(master, width=size, height=size, bg=bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self._icon = icon
        self._command = command
        self._size = size
        self._radius = radius
        self._icon_size = icon_size
        self._bg = bg
        self._color = color
        self._hover_color = hover_color
        self._hover_bg = hover_bg
        self._active_bg = active_bg
        self._hp = 0.0
        self._pressed = False
        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Enter>", lambda e: tween(self, 7, lambda t: setattr(self, "_hp", t) or self._redraw()))
        self.bind("<Leave>", lambda e: tween(self, 7, lambda t: setattr(self, "_hp", 1 - t) or self._redraw()))
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self._redraw()

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self._redraw()

    def _on_press(self, e):
        self._pressed = True
        self._redraw()

    def _on_release(self, e):
        self._pressed = False
        self._redraw()
        if self._command:
            self._command()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width() or self._size
        h = self.winfo_height() or self._size
        if w <= 1 or h <= 1:
            return
        if self._hp > 0.02:
            bg_col = th.lerp_color(self._bg, self._hover_bg, self._hp)
            fx.round_rect(self, 1, 1, w - 1, h - 1, self._radius, fill=bg_col)
        if self._pressed:
            fx.round_rect(self, 1, 1, w - 1, h - 1, self._radius,
                          fill=self._active_bg)
        color = th.lerp_color(self._color, self._hover_color, self._hp)
        dy = 1 if self._pressed else 0
        icons.draw(self._icon, self, w / 2, h / 2 + dy, self._icon_size, color)


class LinkButton(tk.Canvas):
    def __init__(self, master, text, command, *, font_size=13, color=th.MUTED,
                 hover_color=th.ACCENT_L, bg=th.BG):
        super().__init__(master, bg=bg, highlightthickness=0, bd=0, cursor="hand2")
        self._text = text
        self._command = command
        self._font_size = font_size
        self._color = color
        self._hover_color = hover_color
        self._hp = 0.0
        self._height = font_size + 14
        self.config(height=self._height)
        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Enter>", lambda e: tween(self, 7, lambda t: setattr(self, "_hp", t) or self._redraw()))
        self.bind("<Leave>", lambda e: tween(self, 7, lambda t: setattr(self, "_hp", 1 - t) or self._redraw()))
        self.bind("<Button-1>", lambda e: self._command())
        self._redraw()

    def set_text(self, text):
        self._text = text
        self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width() or th.measure(self._text, self._font_size, "bold")
        h = self.winfo_height() or self._height
        color = th.lerp_color(self._color, self._hover_color, self._hp)
        self.create_text(w / 2, h / 2, text=self._text,
                         font=th.F(self._font_size, "bold"), fill=color)



class TextField(tk.Canvas):
    def __init__(self, master, *, placeholder="", height=54, radius=16,
                 font_size=14, bg=th.BG, fill=th.SURFACE_2, border=th.BORDER_2,
                 focus_border=th.ACCENT, text_color=th.TEXT,
                 placeholder_color=th.MUTED, password=False,
                 right_icon=None, on_enter=None, on_change=None):
        super().__init__(master, height=height, bg=bg, highlightthickness=0, bd=0)
        self._fill = fill
        self._border = border
        self._focus_border = focus_border
        self._text_color = text_color
        self._ph_color = placeholder_color
        self._font = th.F(font_size)
        self._ph = placeholder
        self._password = password
        self._show = False
        self._radius = radius
        self._height = height
        self._focus_t = 0.0
        self._error = False
        self._right_icon = right_icon
        self._on_enter = on_enter
        self._on_change = on_change

        show = "\u2022" if (password and not self._show) else ""
        self.entry = tk.Entry(self, bd=0, highlightthickness=0, relief=tk.FLAT,
                              bg=fill, fg=text_color, insertbackground=text_color,
                              font=self._font, show=show,
                              selectbackground=th.ACCENT_D, selectforeground="#ffffff")
        self._win = self.create_window(16, height / 2, anchor="w", window=self.entry)

        self._eye_btn = None
        if password:
            self._eye_btn = IconButton(self, "eye" if not self._show else "eye_off",
                                       self._toggle_eye, size=30, bg=fill)
            self._eye_btn.place(relx=1.0, rely=0.5, anchor="e", x=-10)

        self.bind("<Configure>", self._on_resize)
        self.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyRelease>", self._on_key)
        if on_enter:
            self.entry.bind("<Return>", lambda e: on_enter())
        self._redraw()

    def _on_key(self, e):
        self._redraw()
        if self._on_change:
            self._on_change(e)

    def _toggle_eye(self):
        self._show = not self._show
        self.entry.config(show="" if self._show else "\u2022")
        if self._eye_btn:
            self._eye_btn.icon = "eye_off" if self._show else "eye"
        self.entry.icursor(len(self.entry.get()))
        self._redraw()

    def _on_resize(self, e):
        w = e.width
        right = 40 if self._eye_btn else 0
        self.itemconfigure(self._win, width=max(20, w - 32 - right))
        self.coords(self._win, 16, self._height / 2)
        if self._eye_btn:
            self._eye_btn.place_configure(relx=1.0, rely=0.5, anchor="e", x=-10)
        self._redraw()

    def _on_focus_in(self, e):
        self._focus_t = 1.0
        self._redraw()

    def _on_focus_out(self, e):
        self._focus_t = 0.0
        self._redraw()

    def set_error(self, flag):
        self._error = bool(flag)
        self._redraw()

    @property
    def value(self):
        return self.entry.get()

    def set_value(self, text):
        self.entry.delete(0, "end")
        self.entry.insert(0, text)
        self.entry.icursor("end")
        self._redraw()
        if self._on_change:
            self._on_change(None)

    def clear(self):
        self.set_value("")

    def focus(self):
        self.entry.focus_set()

    def _redraw(self):
        self.delete("bg", "ph")
        w = self.winfo_width() or self.winfo_reqwidth()
        h = self.winfo_height() or self._height
        if w <= 1 or h <= 1:
            return
        if self._error:
            outline = th.DANGER
        else:
            outline = th.lerp_color(self._border, self._focus_border, self._focus_t)
        fx.round_rect(self, 1, 1, w - 1, h - 1, self._radius,
                      fill=self._fill, outline=outline, width=2 if self._focus_t > 0 or self._error else 1)
        if self._focus_t > 0 and not self._error:
            fx.round_rect(self, 1, 1, w - 1, h - 1, self._radius,
                          fill="", outline=th.lerp_color(outline, th.ACCENT_L, 0.25), width=1)
        if not self.entry.get() and not self._ph == "":
            show_ph = self._ph if not self._password else ""
            self.create_text(16, h / 2, text=show_ph, font=self._font,
                             fill=self._ph_color, anchor="w", tags="ph")

class Field(tk.Frame):
    def __init__(self, master, label, *, bg=th.BG, label_color=th.MUTED, **input_kwargs):
        super().__init__(master, bg=bg)
        self.label_lbl = tk.Label(self, text=label, bg=bg, fg=label_color,
                                  font=th.F(10, "bold"), anchor="w")
        self.label_lbl.pack(fill="x", padx=2, pady=(0, 4))
        self.input = TextField(self, bg=bg, **input_kwargs)
        self.input.pack(fill="x", pady=(0, 0))
        self.hint = tk.Label(self, text="", bg=bg, fg=th.DANGER, font=th.F(11), anchor="w")

    def set_hint(self, msg):
        if msg:
            self.hint.config(text=msg)
            if not self.hint.winfo_manager():
                self.hint.pack(fill="x", padx=2, pady=(5, 0))
        else:
            self.hint.pack_forget()

    def set_error(self, flag):
        self.input.set_error(flag)

    @property
    def value(self):
        return self.input.value

    def set_value(self, text):
        self.input.set_value(text)

    def clear(self):
        self.input.clear()

    def focus(self):
        self.input.focus()


def _score_password(pw):
    if not pw:
        return 0
    score = 0
    if len(pw) >= 8:
        score += 1
    if len(pw) >= 12:
        score += 1
    classes = 0
    for c in pw:
        if c.islower():
            classes |= 1
        elif c.isupper():
            classes |= 2
        elif c.isdigit():
            classes |= 4
        else:
            classes |= 8
    if classes & 1:
        score += 1
    if classes & 2:
        score += 1
    if classes & 4:
        score += 1
    if classes & 8:
        score += 1
    if len(pw) >= 16:
        score += 1
    return min(4, score)


class StrengthMeter(tk.Canvas):
    HEIGHT = 30

    def __init__(self, master, *, bg=th.BG):
        super().__init__(master, height=self.HEIGHT, bg=bg, highlightthickness=0, bd=0)
        self._score = 0
        self._redraw()

    def set_password(self, pw):
        self._score = _score_password(pw)
        self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width() or self.winfo_reqwidth()
        if w <= 1:
            return
        labels = {0: "", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong"}
        colors = {0: th.FAINT, 1: th.DANGER, 2: th.WARNING, 3: th.TEAL, 4: th.SUCCESS}
        fx.round_rect(self, 0, 0, w, 6, 3, fill=th.SURFACE_2)
        if self._score > 0:
            seg = w / 4
            for i in range(self._score):
                x1 = i * seg + 2
                x2 = (i + 1) * seg - 2
                fx.round_rect(self, x1, 0, x2, 6, 3, fill=colors[self._score])
        if self._score > 0:
            self.create_text(2, 20, text=labels[self._score], font=th.F(11, "bold"),
                             fill=colors[self._score], anchor="w")
        else:
            self.create_text(2, 20, text="Password strength", font=th.F(11),
                             fill=th.FAINT, anchor="w")

class GlassCard(tk.Canvas):
    def __init__(self, master, width, height, *, bg=th.BG, panel=th.SURFACE,
                 border=th.BORDER, radius=26, pad=12):
        super().__init__(master, width=width, height=height, bg=bg,
                         highlightthickness=0, bd=0)
        self._cw = width
        self._ch = height
        self._pad = pad
        self._radius = radius
        self._panel = panel
        self._border = border
        self._t = 0.0
        self._active = True
        self._blob_items = []
        self._imgs = [
            fx.radial_image(320, "#6a5ae6", bg),
            fx.radial_image(280, "#2fb89d", bg),
            fx.radial_image(360, "#3a2f86", bg),
        ]
        self._specs = [
            (0.5, 0.0, 0.14, 0.08, 0.5, 0.9),
            (1.0, 1.0, 0.16, 0.10, 0.4, 2.2),
            (0.0, 0.8, 0.14, 0.10, 0.6, 4.1),
        ]
        self._panel_item = None
        self.bind("<Configure>", lambda e: self._draw_panel())
        self._draw_panel()
        self._animate()

    def _draw_panel(self):
        if self._panel_item is not None:
            self.delete(self._panel_item)
        self._panel_item = fx.round_rect(self, self._pad, self._pad,
                                         self._cw - self._pad, self._ch - self._pad,
                                         self._radius, fill=self._panel,
                                         outline=self._border, width=1)
        self.tag_raise(self._panel_item)

    def _animate(self):
        try:
            if not self._active:
                return
            self.delete("blobs")
            self._blob_items = []
            for i, (fx_, fy, ax, ay, sp, ph) in enumerate(self._specs):
                x = self._cw * fx_ + math.sin(self._t * sp + ph) * self._cw * ax
                y = self._ch * fy + math.cos(self._t * sp * 0.72 + ph) * self._ch * ay
                self._blob_items.append(self.create_image(x, y, image=self._imgs[i % 3], tags="blobs"))
            self.tag_lower("blobs")
            self.tag_raise(self._panel_item)
            self._t += 0.05
            self.after(42, self._animate)
        except tk.TclError:
            pass

    def destroy(self):
        self._active = False
        super().destroy()


# ---------------------------------------------------------------------------
# Animated aurora background strip
# ---------------------------------------------------------------------------

class AuroraCanvas(tk.Canvas):
    def __init__(self, master, *, bg=th.BG):
        super().__init__(master, bg=bg, highlightthickness=0, bd=0)
        self._t = 0.0
        self._active = True
        self._blob_items = []
        self._imgs = [
            fx.radial_image(360, "#5b4bd8", bg),
            fx.radial_image(300, "#2fb89d", bg),
            fx.radial_image(340, "#3a2f86", bg),
        ]
        self._specs = [
            (0.16, 0.9, 0.15, 0.4, 0.12, 0.9),
            (0.86, 0.92, 0.14, 0.42, 0.10, 2.2),
            (0.55, 0.5, 0.18, 0.5, 0.14, 4.1),
        ]
        self.bind("<Configure>", self._draw_base)
        self._draw_base()
        self._animate()

    def _draw_base(self, e=None):
        self.delete("base")
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1 or h <= 1:
            return
        bands = max(2, h // 16)
        for i in range(bands):
            t = i / (bands - 1) if bands > 1 else 0
            col = th.lerp_color(th.BG_TOP, th.BG, min(1.0, t * 0.5))
            y0 = h * i / bands
            y1 = h * (i + 1) / bands
            self.create_rectangle(0, y0, w, y1 + 1, fill=col, outline="", tags="base")
        self.tag_lower("base")

    def _animate(self):
        try:
            if not self._active:
                return
            self.delete("blob")
            self._blob_items = []
            w = self.winfo_width()
            h = self.winfo_height()
            if w > 1 and h > 1:
                for i, (fx_, fy, ax, ay, sp, ph) in enumerate(self._specs):
                    x = w * fx_ + math.sin(self._t * sp + ph) * w * ax
                    y = h * fy + math.cos(self._t * sp * 0.72 + ph) * h * ay
                    self._blob_items.append(self.create_image(x, y, image=self._imgs[i % 3], tags="blob"))
                self.tag_lower("blob")
            self._t += 0.05
            self.after(42, self._animate)
        except tk.TclError:
            pass

    def destroy(self):
        self._active = False
        super().destroy()



class SlimScrollbar(tk.Canvas):
    def __init__(self, master, *, width=8, bg=th.BG, thumb=th.BORDER_2, radius=4):
        super().__init__(master, width=width, bg=bg, highlightthickness=0, bd=0)
        self._thumb = thumb
        self._radius = radius
        self._ratio = 1.0
        self._offset = 0.0
        self._canvas_ref = None
        self._dragging = False
        self._drag_y = 0
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<ButtonPress-1>", self._on_drag_start)
        self.bind("<B1-Motion>", self._on_drag_move)
        self.bind("<ButtonRelease-1>", lambda e: setattr(self, "_dragging", False))
        self._draw()

    def sync(self, canvas):
        self._canvas_ref = canvas
        if canvas is None:
            return
        try:
            bbox = canvas.bbox("all")
            total = bbox[3] if bbox else 0
        except tk.TclError:
            total = 0
        view = canvas.winfo_height()
        if total > view > 0:
            self._ratio = view / total
            self._offset = canvas.canvasy(0) / total
        else:
            self._ratio = 1.0
            self._offset = 0.0
        self._draw()

    def _draw(self):
        self.delete("all")
        h = self.winfo_height()
        w = self.winfo_width()
        if self._ratio >= 1.0 or h <= 1 or w <= 1:
            return
        thumb_h = max(24, h * self._ratio)
        y0 = self._offset * (h - thumb_h)
        fx.round_rect(self, 1, y0, w - 1, y0 + thumb_h, self._radius, fill=self._thumb)

    def _on_drag_start(self, e):
        if self._ratio < 1.0:
            self._dragging = True
            self._drag_y = e.y

    def _on_drag_move(self, e):
        if not self._dragging or self._canvas_ref is None:
            return
        dy = e.y - self._drag_y
        self._drag_y = e.y
        self._canvas_ref.yview_scroll(int(-dy * 0.5), "pixels")
        self.sync(self._canvas_ref)


class ScrollArea(tk.Frame):
    def __init__(self, master, *, bg=th.BG, padx=0):
        super().__init__(master, bg=bg)
        self._bg = bg
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.sb = SlimScrollbar(self, bg=bg)
        self.sb.pack(side="right", fill="y", padx=(6, 0))
        self.inner.bind("<Configure>", self._on_inner)
        self.canvas.bind("<Configure>", self._on_canvas)
        self.attach(self.canvas)
        self.attach(self.inner)

    def _on_inner(self, e):
        try:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except tk.TclError:
            pass
        self.sb.sync(self.canvas)

    def _on_canvas(self, e):
        self.canvas.itemconfigure(self._win, width=e.width)
        self.sb.sync(self.canvas)

    def _on_wheel(self, e):
        if getattr(e, "num", None) == 4:
            self.canvas.yview_scroll(-2, "units")
        elif getattr(e, "num", None) == 5:
            self.canvas.yview_scroll(2, "units")
        else:
            delta = getattr(e, "delta", 0)
            if delta:
                self.canvas.yview_scroll(-1 if delta > 0 else 1, "units")
        self.sb.sync(self.canvas)
        return "break"

    def attach(self, widget):
        widget.bind("<Button-4>", self._on_wheel)
        widget.bind("<Button-5>", self._on_wheel)
        widget.bind("<MouseWheel>", self._on_wheel)

    def clear(self):
        for child in self.inner.winfo_children():
            child.destroy()
        self.sb.sync(self.canvas)

    def scroll_top(self):
        self.canvas.yview_moveto(0)
        self.sb.sync(self.canvas)


class StatCard(tk.Canvas):
    HEIGHT = 88

    def __init__(self, master, icon, value, label, color, *, bg=th.BG):
        super().__init__(master, height=self.HEIGHT, bg=bg, highlightthickness=0, bd=0)
        self._icon = icon
        self._value = str(value)
        self._label = label
        self._color = color
        self._bg = bg
        self.bind("<Configure>", lambda e: self._layout())
        self._layout()

    def set_value(self, value):
        self._value = str(value)
        self._layout()

    def _layout(self):
        self.delete("all")
        w = self.winfo_width() or 200
        h = self.HEIGHT
        if w <= 1:
            return
        fx.round_rect(self, 0, 0, w, h, 16, fill=th.SURFACE, outline=th.BORDER, width=1)
        tint = th.lerp_color(self._color, th.SURFACE, 0.72)
        self.create_oval(18, (h - 42) / 2, 60, (h - 42) / 2 + 42, fill=tint, outline="")
        icons.draw(self._icon, self, 39, h / 2, 18, self._color)
        value_w = w - 84
        label = th.ellipsize(self._value, 20, "bold", value_w)
        self.create_text(74, 27, text=label, font=th.F(20, "bold"), fill=th.TEXT, anchor="w")
        self.create_text(74, 56, text=self._label, font=th.F(11), fill=th.MUTED, anchor="w")



class EntryCard(tk.Canvas):
    HEIGHT = 112

    def __init__(self, master, *, platform, email, password, index, color,
                 on_copy_email=None, on_copy_password=None,
                 on_edit=None, on_delete=None, scrollarea=None, bg=th.BG):
        super().__init__(master, height=self.HEIGHT, bg=bg, highlightthickness=0, bd=0)
        self.platform = platform
        self.email = email
        self.password = password
        self.index = index
        self.color = color
        self._on_copy_email = on_copy_email
        self._on_copy_password = on_copy_password
        self._on_edit = on_edit
        self._on_delete = on_delete
        self._revealed = False
        self._hp = 0.0
        self._radius = 18

        self._avatar = tk.Canvas(self, width=40, height=40, bg=bg, highlightthickness=0, bd=0)
        self._avatar.place(x=24, y=(self.HEIGHT - 40) / 2)

        btn_bg = th.SURFACE
        self._btn_eye = IconButton(self, "eye", self._toggle_reveal, size=30, bg=btn_bg)
        self._btn_copy_email = IconButton(self, "copy", lambda: self._copy_email(), size=30, bg=btn_bg)
        self._btn_copy_pw = IconButton(self, "copy", lambda: self._copy_pw(), size=30, bg=btn_bg)
        self._btn_edit = IconButton(self, "edit", lambda: self._on_edit(self), size=30, bg=btn_bg)
        self._btn_delete = IconButton(self, "trash", lambda: self._on_delete(self), size=30, bg=btn_bg,
                                      color=th.MUTED, hover_color=th.DANGER, hover_bg=th.DANGER_BG)

        self.bind("<Configure>", lambda e: self._layout())
        self.bind("<Enter>", lambda e: tween(self, 8, lambda t: setattr(self, "_hp", t) or self._layout()))
        self.bind("<Leave>", lambda e: tween(self, 8, lambda t: setattr(self, "_hp", 1 - t) or self._layout()))
        if scrollarea is not None:
            scrollarea.attach(self)
        self._layout()

    def _toggle_reveal(self):
        self._revealed = not self._revealed
        self._btn_eye.icon = "eye_off" if self._revealed else "eye"
        self._layout()

    def _copy_email(self):
        if self._on_copy_email:
            self._on_copy_email(self)

    def _copy_pw(self):
        if self._on_copy_password:
            self._on_copy_password(self)

    def _draw_avatar(self):
        self._avatar.delete("all")
        r = 17
        icons.avatar(self._avatar, 20, 20, r, self.platform, self.color, "#ffffff", th.F(15, "bold"))

    def _layout(self):
        self.delete("panel", "texts")
        w = self.winfo_width() or 400
        h = self.HEIGHT
        if w <= 1:
            return

        panel_col = th.SURFACE
        outline = th.ACCENT if self._hp > 0.45 else th.BORDER
        self._panel = fx.round_rect(self, 0, 0, w, h, self._radius,
                                    fill=panel_col, outline=outline, width=1)

        self._draw_avatar()

        btns = [self._btn_delete, self._btn_edit, self._btn_copy_pw, self._btn_copy_email]
        for i, b in enumerate(btns):
            b.place_configure(x=w - 34 - i * 38, y=(h - 30) / 2)

        left = 76
        right = w - 34 - 4 * 38 - 10
        max_w = max(120, right - left)

        self.create_text(left, 28, text=th.ellipsize(self.platform, 15, "bold", max_w),
                         font=th.F(15, "bold"), fill=th.TEXT, anchor="w", tags="texts")
        self.create_text(left, 54, text=th.ellipsize(self.email, 12, "normal", max_w),
                         font=th.F(12), fill=th.MUTED, anchor="w", tags="texts")

        shown = self.password if self._revealed else "\u2022" * min(len(self.password), 22)
        pw_col = th.TEXT if self._revealed else th.FAINT
        pw_font = th.MONO(12) if self._revealed else th.F(12)
        self.create_text(left, 80, text=th.ellipsize(shown, 12, "normal", max_w - 34),
                         font=pw_font, fill=pw_col, anchor="w", tags="texts")

        pw_w = th.measure(th.ellipsize(shown, 12, "normal", max_w - 34), 12)
        eye_x = min(left + pw_w + 6, right - 18)
        self._btn_eye.place_configure(x=eye_x, y=65)


class EmptyState(tk.Frame):
    def __init__(self, master, *, icon="key", title, subtitle="", action_text=None,
                 on_action=None, bg=th.BG):
        super().__init__(master, bg=bg)
        pad = tk.Frame(self, bg=bg)
        pad.pack(expand=True)
        icon_c = tk.Canvas(pad, width=84, height=84, bg=bg, highlightthickness=0, bd=0)
        icon_c.pack(pady=(40, 0))
        icons.draw(icon, icon_c, 42, 42, 30, th.BORDER_2)
        icons.draw(icon, icon_c, 42, 42, 20, th.ACCENT)
        tk.Label(pad, text=title, bg=bg, fg=th.TEXT, font=th.F(17, "bold")).pack(pady=(18, 4))
        if subtitle:
            tk.Label(pad, text=subtitle, bg=bg, fg=th.MUTED, font=th.F(12)).pack(pady=(0, 8))
        if action_text and on_action:
            btn = RoundedButton(pad, text=action_text, command=on_action,
                                variant="primary", height=44, font_size=14, icon="plus", bg=bg)
            btn.pack(pady=(14, 0))
        pad.pack(expand=True)


class Toast:
    HEIGHT = 52

    def __init__(self, app, message, kind="success", duration=2600):
        self.app = app
        self._closed = False
        colors = {"success": th.SUCCESS, "error": th.DANGER, "info": th.ACCENT}
        icons_map = {"success": "check", "error": "close", "info": "shield"}
        color = colors.get(kind, th.SUCCESS)
        icon = icons_map.get(kind, "check")

        self.canvas = tk.Canvas(app.root, height=self.HEIGHT, bg=th.BG,
                                highlightthickness=0, bd=0)
        tw = th.measure(message, 12)
        self._w = max(240, 74 + tw + 40)
        self.canvas.config(width=self._w)
        fx.round_rect(self.canvas, 1, 1, self._w - 1, self.HEIGHT - 1, 26,
                      fill=th.SURFACE_2, outline=th.BORDER_2, width=1)
        icons.draw(icon, self.canvas, 27, self.HEIGHT / 2, 15, color)
        self.canvas.create_text(52, self.HEIGHT / 2, text=message, font=th.F(12),
                                fill=th.TEXT, anchor="w")
        self.canvas.place(relx=1.0, rely=1.0, anchor="se", x=self._w + 20, y=-22)
        self._target = -22
        self._slide_in(then=self._schedule_close, duration=duration)

    def _slide_in(self, then=None, duration=2600):
        steps = 12

        def go(i=0):
            if self._closed:
                return
            t = i / steps
            x = self._w + 20 + (self._target - (self._w + 20)) * t
            self.canvas.place_configure(x=x)
            if i < steps:
                self.canvas.after(16, lambda: go(i + 1))
            elif then:
                then(duration)

        go()

    def _schedule_close(self, duration):
        self.canvas.after(duration, self._slide_out)

    def _slide_out(self):
        steps = 10

        def go(i=0):
            if self._closed:
                return
            t = i / steps
            x = self._target + (self._w + 40) * t
            self.canvas.place_configure(x=x)
            if i < steps:
                self.canvas.after(16, lambda: go(i + 1))
            else:
                self._closed = True
                self.canvas.destroy()

        go()


class Modal:
    def __init__(self, app, width=500, height=380, on_close=None):
        self.app = app
        self._W = width
        self._H = height
        self._on_close = on_close
        self._closed = False
        self._offset = 30
        self._items = []
        self.canvas = tk.Canvas(app.root, bg=th.BG, highlightthickness=0, bd=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.create_rectangle(0, 0, 2, 2, fill="#04050c", stipple="gray50", tags="dim")
        self.canvas.bind("<Configure>", self._relayout)
        self._origin = (0, 0)
        app.modal = self
        self._relayout(None)
        self._animate_in()

    def add(self, widget, x, y, anchor="nw", width=None, height=None):
        widget.x0 = x
        widget.y0 = y
        widget.anchor0 = anchor
        self._items.append(widget)
        ox, oy = self._origin
        widget.place(x=ox + x, y=oy + y, anchor=anchor, width=width, height=height)

    def title(self, text, *, sub=None):
        ox, oy = self._origin
        self.canvas.create_text(ox + self._W / 2, oy + 30, text=text,
                                font=th.F(19, "bold"), fill=th.TEXT, anchor="center")
        if sub:
            self.canvas.create_text(ox + self._W / 2, oy + 56, text=sub,
                                    font=th.F(11), fill=th.MUTED, anchor="center")

    def _relayout(self, e=None):
        try:
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
        except tk.TclError:
            w = h = 100
        if w <= 1:
            w = self.app.root.winfo_width()
            h = self.app.root.winfo_height()
        cx, cy = w / 2, h / 2
        x1 = cx - self._W / 2
        y1 = cy - self._H / 2 + self._offset
        self._origin = (x1, y1)
        self.canvas.delete("panel")
        self.canvas.create_rectangle(0, 0, w, h, fill="#04050c", stipple="gray50", tags="dim")
        self.canvas.create_oval(cx - self._W / 2 - 60, y1 - 30, cx + self._W / 2 + 60, y1 + 10,
                                fill="", tags="dim")
        self._panel = fx.round_rect(self.canvas, x1, y1, x1 + self._W, y1 + self._H, 24,
                                    fill=th.SURFACE, outline=th.BORDER_2, width=1, tags="panel")
        for item in self._items:
            item.place_configure(x=x1 + item.x0, y=y1 + item.y0, anchor=item.anchor0)
    def _animate_in(self):
        steps = 14

        def go(i=0):
            if self._closed:
                return
            t = i / steps
            self._offset = 30 * (1 - t)
            self._relayout()
            if i < steps:
                self.canvas.after(14, lambda: go(i + 1))
            else:
                self._offset = 0
                self._relayout()

        go()

    def close(self, call_callback=True):
        if self._closed:
            return
        steps = 9

        def go(i=0):
            if self._closed:
                return
            t = i / steps
            self._offset = 30 * t
            self._relayout()
            if i < steps:
                self.canvas.after(14, lambda: go(i + 1))
            else:
                self._destroy()

        go()
        if call_callback and self._on_close:
            self._on_close()

    def _destroy(self):
        self._closed = True
        try:
            self.canvas.destroy()
        except tk.TclError:
            pass
        if self.app.modal is self:
            self.app.modal = None
