import tkinter as tk

from .. import theme as th
from .. import services
from ..widgets import Modal, Field, RoundedButton, LinkButton


class AddEntryModal(Modal):
    def __init__(self, app, *, key, index=None, platform="", email="", password="",
                 on_saved=None):
        super().__init__(app, width=480, height=560)
        self.key = key
        self.index = index
        self.on_saved = on_saved
        self.title("Edit password" if index is not None else "Add new password",
                   sub="Saved encrypted with AES-256")

        self.f_platform = Field(self.canvas, "Platform name", placeholder="e.g. Instagram",
                                bg=th.SURFACE)
        self.add(self.f_platform, 40, 86, "nw", width=400)
        self.f_email = Field(self.canvas, "Email or username", placeholder="you@example.com",
                             bg=th.SURFACE)
        self.add(self.f_email, 40, 176, "nw", width=400)
        self.f_password = Field(self.canvas, "Password", password=True,
                                bg=th.SURFACE, on_enter=self._save)
        self.add(self.f_password, 40, 266, "nw", width=400)

        self.btn_gen = LinkButton(self.canvas, "Generate strong password",
                                  self._generate, bg=th.SURFACE, font_size=12,
                                  hover_color=th.TEAL)
        self.add(self.btn_gen, 40, 352, "nw", width=200, height=26)

        self.btn_cancel = RoundedButton(self.canvas, "Cancel", self.close,
                                        variant="secondary", height=48, bg=th.SURFACE)
        self.add(self.btn_cancel, 40, 402, "nw", width=185)
        self.btn_save = RoundedButton(self.canvas,
                                      "Save changes" if index is not None else "Save password",
                                      self._save, variant="primary", height=48,
                                      icon="check", bg=th.SURFACE)
        self.add(self.btn_save, 245, 402, "nw", width=195)

        self.f_platform.input.entry.bind("<Return>", lambda e: self.f_email.input.focus())
        self.f_email.input.entry.bind("<Return>", lambda e: self.f_password.input.focus())

        if platform:
            self.f_platform.set_value(platform)
        if email:
            self.f_email.set_value(email)
        if password:
            self.f_password.set_value(password)
        self.f_platform.input.focus()

    def _generate(self):
        self.f_password.set_value(services.generate_password())
        self.app.toast("Strong password generated", "info")

    def _save(self):
        platform = self.f_platform.value.strip()
        email = self.f_email.value.strip()
        pw = self.f_password.value
        ok = True
        if not platform:
            self.f_platform.set_error(True)
            ok = False
        if not email:
            self.f_email.set_error(True)
            ok = False
        if not pw:
            self.f_password.set_error(True)
            ok = False
        if not ok:
            return
        try:
            if self.index is None:
                services.add_entry(platform, email, pw, self.key)
                self.app.toast("Password saved", "success")
            else:
                services.update_entry(self.index, platform, email, pw, self.key)
                self.app.toast("Password updated", "success")
        except Exception:
            self.app.toast("Could not save the entry", "error")
            return
        self.close()
        if self.on_saved:
            self.on_saved()


class ConfirmModal(Modal):
    def __init__(self, app, *, title, message, confirm_text="Delete", on_confirm=None):
        super().__init__(app, width=430, height=250)
        self.on_confirm = on_confirm
        self.title(title)

        msg = tk.Label(self.canvas, text=message, bg=th.SURFACE, fg=th.MUTED,
                       font=th.F(12), justify="center", wraplength=330)
        self.add(msg, 215, 96, "center", width=350)

        self.btn_cancel = RoundedButton(self.canvas, "Cancel", self.close,
                                        variant="secondary", height=46, bg=th.SURFACE)
        self.add(self.btn_cancel, 40, 176, "nw", width=160)
        self.btn_confirm = RoundedButton(self.canvas, confirm_text, self._confirm,
                                         variant="danger", height=46, bg=th.SURFACE)
        self.add(self.btn_confirm, 230, 176, "nw", width=160)

    def _confirm(self):
        self.close()
        if self.on_confirm:
            self.on_confirm()
