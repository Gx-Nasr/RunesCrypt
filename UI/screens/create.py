from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout
import os
from .. import theme as th
from ..widgets import Button, Field, LinkButton, StrengthMeter
from .auth import AuthScreen, Brand


class CreateScreen(AuthScreen):
    card_max_h = 820

    def _build_card(self):
        lay = QVBoxLayout(self.card)
        lay.setContentsMargins(46, 36, 46, 28)
        lay.setSpacing(0)

        lay.addStretch(1)
        lay.addWidget(Brand(self.card, 54), 0, Qt.AlignHCenter)
        lay.addSpacing(10)

        t = QLabel("Create your account", self.card)
        t.setFont(th.font(24, "heavy"))
        t.setStyleSheet(f"""
            color: {th.TEXT.name()};
            background-color: transparent;
        """)
        t.setAlignment(Qt.AlignCenter)
        lay.addWidget(t)
        lay.addSpacing(8)

        s = QLabel("Set a master password to encrypt your vault", self.card)
        s.setFont(th.font(12))
        s.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        s.setAlignment(Qt.AlignCenter)
        lay.addWidget(s)
        lay.addSpacing(22)

        self.f_login = Field(self.card, "Login", placeholder="4\u201312 letters, _ or -",
                             on_return=lambda: self.f_password.focus())
        lay.addWidget(self.f_login)
        lay.addSpacing(40)

        self.f_password = Field(self.card, "Master password",
                                placeholder="Min 8 chars \u2014 upper, lower, number, special",
                                password=True, on_return=lambda: self.f_confirm.focus())
        lay.addWidget(self.f_password)
        lay.addSpacing(40)

        self.f_confirm = Field(self.card, "Confirm password",
                               placeholder="Repeat your master password",
                               password=True, on_return=self._submit)
        lay.addWidget(self.f_confirm)
        lay.addSpacing(60)

        self.btn_create = Button(self.card, "Create account", self._submit,
                                 variant="primary", height=52, radius=15, icon="check", font_size=15)
        lay.addWidget(self.btn_create)
        lay.addSpacing(10)

        note = QLabel("Your vault is protected with AES-256 encryption", self.card)
        note.setFont(th.font(11))
        note.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        note.setAlignment(Qt.AlignCenter)
        lay.addWidget(note)
        lay.addSpacing(2)

        lay.addStretch(1)

    def _go_login(self):
        from .login import LoginScreen
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
            self.app.services.create_user(login, pw)
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
        if os.path.exists(".passwords.json"):
            os.remove(".passwords.json")
        self.app.toast("Account created \u2014 sign in to continue", "success")
        from .login import LoginScreen
        self.app.transition(LoginScreen)
