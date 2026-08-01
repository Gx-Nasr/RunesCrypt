import tkinter as tk

from .. import theme as th


class Screen:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.root, bg=th.BG)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        self._build()

    def _build(self):
        raise NotImplementedError

    def destroy(self):
        try:
            self.frame.destroy()
        except tk.TclError:
            pass
