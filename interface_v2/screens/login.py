import tkinter as tk

from .. import theme as th
from .. import services
from ..widgets import Field, RoundedButton, LinkButton
from .base import Screen
from .auth import AuthScreen


class LoginScreen(AuthScreen, Screen):
    card_h = 560

    def _build_card(self):
        cx = self.card_w / 2
        tk.Label(self.card, text="Welcome back", bg=self.panel, fg=th.TEXT,
                 font=th.F(26, "bold")).place(relx=0.5, y=78, anchor="n")
        tk.Label(self.card, text="Unlock your encrypted vault with your master password",
                 bg=self.panel, fg=th.MUTED, font=th.F(12)).place(relx=0.5, y=120, anchor="n")
        tk.Label(self.card, text="Protected locally with AES-256", bg=self.panel,
                 fg=th.FAINT, font=th.F(10)).place(relx=0.5, y=144, anchor="n")

        self.f_login = Field(self.card, "Login", placeholder="Your username",
                             bg=self.panel)
        self.f_login.place(x=48, y=182, width=self.card_w - 96)
        self.f_password = Field(self.card, "Password", placeholder="••••••••",
                                password=True, bg=self.panel,
                                on_enter=self._submit)
        self.f_password.place(x=48, y=276, width=self.card_w - 96)

        self.btn_login = RoundedButton(self.card, "Unlock vault", self._submit,
                                       variant="primary", height=52, icon="lock", bg=self.panel)
        self.btn_login.place(x=48, y=382, width=self.card_w - 96)

        tk.Label(self.card, text="Use your saved credentials to access your vault",
                 bg=self.panel, fg=th.MUTED, font=th.F(11)).place(relx=0.5, y=452, anchor="n")

        self.f_login.input.entry.bind("<Return>", lambda e: self.f_password.input.focus())

    def _submit(self):
        login = self.f_login.value.strip()
        pw = self.f_password.value
        self.f_login.set_error(not login)
        self.f_password.set_error(not pw)
        self.f_login.set_hint("Login is required" if not login else "")
        self.f_password.set_hint("Password is required" if not pw else "")
        if not login or not pw:
            self._shake()
            return
        self.btn_login.set_loading(True)
        self.frame.after(80, self._do_login, login, pw)

    def _do_login(self, login, pw):
        try:
            key = services.authenticate(login, pw)
        except ValueError as e:
            self.btn_login.set_loading(False)
            self.f_login.set_error(True)
            self.f_password.set_error(True)
            self.f_password.set_hint(str(e))
            self._shake()
            return
        self.app.key = key
        self.app.login = login
        self.btn_login.set_loading(False)
        from .dashboard import DashboardScreen
        self.app.transition(DashboardScreen)
