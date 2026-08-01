import tkinter as tk

from . import theme as th
from . import services
from .widgets import Toast
from .screens.login import LoginScreen
from .screens.create_account import CreateAccountScreen


class App:
    def __init__(self, root):
        self.root = root
        th.init_fonts(root)
        root.title("RunesCrypt")
        root.geometry("1040x700")
        root.minsize(880, 620)
        root.configure(bg=th.BG)
        self.key = None
        self.login = None
        self.screen = None
        self.modal = None
        self._fading = False
        self._toasts = []
        try:
            root.attributes("-alpha", 1.0)
        except tk.TclError:
            pass
        self.show(LoginScreen if services.user_file_exists() else CreateAccountScreen)
        root.protocol("WM_DELETE_WINDOW", self.quit)

    def show(self, cls, **kw):
        self.close_modal()
        if self.screen:
            self.screen.destroy()
        self.screen = cls(self, **kw)
        self._fade_in()

    def transition(self, cls, **kw):
        if self._fading:
            return
        self._fading = True

        def done():
            self._fading = False
            self.show(cls, **kw)

        self._fade_out(done)

    def _fade_out(self, done, steps=8):
        def go(i=0):
            try:
                self.root.attributes("-alpha", max(0.0, 1.0 - i / steps))
            except tk.TclError:
                pass
            if i < steps:
                self.root.after(14, lambda: go(i + 1))
            else:
                done()

        go()

    def _fade_in(self, steps=10):
        def go(i=0):
            try:
                self.root.attributes("-alpha", max(0.05, i / steps))
            except tk.TclError:
                pass
            if i < steps:
                self.root.after(14, lambda: go(i + 1))

        go()

    def toast(self, message, kind="success"):
        for t in self._toasts:
            try:
                t.canvas.destroy()
            except tk.TclError:
                pass
        self._toasts = [Toast(self, message, kind)]

    def close_modal(self):
        if self.modal is not None:
            modal = self.modal
            self.modal = None
            modal.close()

    def copy(self, text, label="Copied to clipboard"):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        self.toast(label, "success")

    def quit(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass


def run():
    root = tk.Tk()
    App(root)
    root.mainloop()
