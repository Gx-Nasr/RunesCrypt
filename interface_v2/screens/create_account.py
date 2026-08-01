import tkinter as tk
import os
from .. import theme as th
from .. import services
from ..widgets import Field, RoundedButton, StrengthMeter, LinkButton
from .base import Screen
from .auth import AuthScreen
from .login import LoginScreen


class CreateAccountScreen(AuthScreen, Screen):
    card_h = 660

    def _build_card(self):
        tk.Label(self.card, text="Create your account", bg=self.panel, fg=th.TEXT,
                 font=th.F(25, "bold")).place(relx=0.5, y=78, anchor="n")
        tk.Label(self.card, text="Set up a master password to protect your vault",
                 bg=self.panel, fg=th.MUTED, font=th.F(12)).place(relx=0.5, y=118, anchor="n")
        tk.Label(self.card, text="A strong password keeps your secrets safe",
                 bg=self.panel, fg=th.FAINT, font=th.F(10)).place(relx=0.5, y=142, anchor="n")

        self.f_login = Field(self.card, "Login", placeholder="4\u201312 letters, _ or -",
                             bg=self.panel)
        self.f_login.place(x=48, y=180, width=self.card_w - 96)

        self.f_password = Field(self.card, "Master password", placeholder="Min 8 chars, upper, lower, number, special",
                                password=True, bg=self.panel,
                                on_enter=lambda: self.f_confirm.input.focus())
        self.f_password.place(x=48, y=272, width=self.card_w - 96)

        self.meter = StrengthMeter(self.card, bg=self.panel)
        self.meter.place(x=48, y=354, width=self.card_w - 96)
        self.f_password.input.entry.bind("<KeyRelease>",
                                         lambda e: self.meter.set_password(self.f_password.value))

        self.f_confirm = Field(self.card, "Confirm password", placeholder="Repeat your master password",
                               password=True, bg=self.panel,
                               on_enter=self._submit)
        self.f_confirm.place(x=48, y=394, width=self.card_w - 96)

        self.btn_create = RoundedButton(self.card, "Create account", self._submit,
                                        variant="primary", height=50, icon="check", bg=self.panel)
        self.btn_create.place(x=48, y=488, width=self.card_w - 96)

        tk.Label(self.card, text="Your vault is protected with AES-256",
                 bg=self.panel, fg=th.FAINT, font=th.F(11)).place(relx=0.5, y=554, anchor="n")

        self.f_login.input.entry.bind("<Return>", lambda e: self.f_password.input.focus())

    def _go_login(self):
        self.app.transition(LoginScreen)

    def _submit(self):
        login = self.f_login.value.strip()
        pw = self.f_password.value
        confirm = self.f_confirm.value
        ok = True
        if not login:
            self.f_login.set_error(True)
            self.f_login.set_hint("Login is required")
            ok = False
        if not pw:
            self.f_password.set_error(True)
            self.f_password.set_hint("Password is required")
            ok = False
        if pw and confirm != pw:
            self.f_confirm.set_error(True)
            self.f_confirm.set_hint("Passwords do not match")
            ok = False
        if not ok:
            self._shake()
            return

        try:
            services.create_user(login, pw)
        except ValueError as e:
            msg = str(e)
            if "login" in msg.lower() or "invalid" in msg.lower():
                self.f_login.set_error(True)
                self.f_login.set_hint(msg)
            else:
                self.f_password.set_error(True)
                self.f_password.set_hint(msg)
            self._shake()
            return

        self.app.toast("Account created \u2014 sign in to continue", "success")
        file_path = ".passwords.json"

        if os.path.exists(file_path):
            os.remove(file_path)
        self.app.transition(LoginScreen)
