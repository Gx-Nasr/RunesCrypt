from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from .. import theme as th
from ..widgets import Button, Field, LinkButton
from .base import GlassCard, Screen
from .auth import AuthScreen, Brand
from .create import CreateScreen


class LoginScreen(AuthScreen):
    card_max_h = 640

    def _build_card(self):
        lay = QVBoxLayout(self.card)
        lay.setContentsMargins(46, 34, 46, 30)
        lay.setSpacing(0)

        lay.addStretch(1)
        lay.addWidget(Brand(self.card, 58), 0, Qt.AlignHCenter)
        lay.addSpacing(16)

        t = QLabel("Welcome back", self.card)
        t.setFont(th.font(26, "heavy"))
        t.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        t.setAlignment(Qt.AlignCenter)
        lay.addWidget(t)

        s = QLabel("Enter your master password to unlock your vault", self.card)
        s.setFont(th.font(12))
        s.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        s.setAlignment(Qt.AlignCenter)
        lay.addWidget(s)
        lay.addSpacing(26)

        self.f_login = Field(self.card, "Login", placeholder="Your username",
                             on_return=lambda: self.f_password.focus())
        lay.addWidget(self.f_login)

        self.f_password = Field(self.card, "Password", placeholder="\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022",
                                password=True, on_return=self._submit)
        lay.addWidget(self.f_password)
        lay.addSpacing(6)

        self.btn_login = Button(self.card, "Unlock vault", self._submit,
                                variant="primary", height=52, radius=15, icon="lock", font_size=15)
        lay.addWidget(self.btn_login)
        lay.addSpacing(14)

        self.link = LinkButton(self.card, "Don\u2019t have an account? Create one",
                               self._go_create)
        lay.addWidget(self.link, 0, Qt.AlignHCenter)

        lay.addStretch(1)

    def _go_create(self):
        self.app.transition(CreateScreen)

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
        QTimer.singleShot(90, lambda: self._do_login(login, pw))

    def _do_login(self, login, pw):
        try:
            key = self.app.services.authenticate(login, pw)
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
