import tkinter as tk

from .. import theme as th
from .. import icons
from ..widgets import GlassCard


class AuthScreen:
    card_w = 460
    card_h = 560
    panel = th.SURFACE

    def _build(self):
        self.card = GlassCard(self.frame, self.card_w, self.card_h,
                              panel=self.panel, bg=th.BG)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self._build_brand()
        self._build_card()
        self._animate_entrance()

    def _build_brand(self):
        cx = self.card_w / 2
        icon_c = tk.Canvas(self.card, width=48, height=48, bg=self.panel,
                           highlightthickness=0, bd=0)
        icon_c.place(x=cx - 116, y=34)
        icon_c.create_oval(2, 2, 46, 46, fill=th.lerp_color(th.ACCENT, self.panel, 0.18), outline=th.ACCENT_L, width=1)
        icons.draw("lock", icon_c, 24, 24, 18, th.ACCENT_L)
        tk.Label(self.card, text="RunesCrypt", bg=self.panel, fg=th.TEXT,
                 font=th.F(20, "bold")).place(x=cx - 56, y=36)
        tk.Label(self.card, text="Secure vault access", bg=self.panel, fg=th.MUTED,
                 font=th.F(11)).place(x=cx - 56, y=65)

    def _build_card(self):
        raise NotImplementedError

    def _animate_entrance(self):
        steps = 15

        def go(i=0):
            try:
                if not self.frame.winfo_exists():
                    return
            except tk.TclError:
                return
            t = i / steps
            dy = 26 * (1 - t) * (1 - t)
            self.card.place_configure(relx=0.5, rely=0.5, anchor="center", y=dy)
            if i < steps:
                self.frame.after(14, lambda: go(i + 1))
            else:
                self.card.place_configure(relx=0.5, rely=0.5, anchor="center", y=0)

        go()

    def _shake(self):
        seq = [0, -11, 9, -7, 6, -4, 3, 0]

        def go(i=0):
            try:
                if not self.frame.winfo_exists():
                    return
            except tk.TclError:
                return
            self.card.place_configure(relx=0.5, rely=0.5, anchor="center",
                                      y=0, x=seq[i])
            if i + 1 < len(seq):
                self.frame.after(42, lambda: go(i + 1))

        go()
