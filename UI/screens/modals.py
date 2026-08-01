from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .. import theme as th
from ..widgets import Button, Field


class ModalCard(QWidget):
    def __init__(self, app, width, height, title):
        super().__init__(app.modal_host)
        self.app = app
        self._w = width
        self._h = height
        self.title = title
        self.setFixedSize(width, height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(30, 96, 30, 26)
        self.body.setSpacing(0)
        app.open_modal(self)

    def paintEvent(self, e):
        from PyQt5.QtGui import QColor, QPainter, QPen, QLinearGradient
        from PyQt5.QtCore import QRectF
        from .. import fx
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = fx.rounded_path(self._w, self._h, 24)
        p.fillPath(path, QColor(0, 0, 0, 0))
        p.setPen(QPen(th.BORDER, 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)
        g = QLinearGradient(0, 0, self._w, 0)
        g.setColorAt(0, th.with_alpha(th.ACCENT, 34))
        g.setColorAt(1, th.with_alpha(th.TEAL, 22))
        p.setPen(Qt.NoPen)
        p.setBrush(g)
        p.drawRoundedRect(QRectF(0, 0, self._w, 96), 24, 24)
        p.setFont(th.font(20, "heavy"))
        p.setPen(th.TEXT)
        p.drawText(QRectF(28, 26, self._w - 56, 40), Qt.AlignLeft | Qt.AlignVCenter, self.title)

    def close(self):
        self.app.close_modal()


class AddEntryModal(ModalCard):
    def __init__(self, app, *, key, index=None, platform="", email="", password="",
                 on_saved=None):
        title = "Edit password" if index is not None else "Add password"
        super().__init__(app, 480, 540, title)
        self.key = key
        self.index = index
        self.on_saved = on_saved

        self.f_platform = Field(self, "Platform", placeholder="e.g. GitHub",
                                on_return=lambda: self.f_email.focus())
        self.body.addWidget(self.f_platform)

        self.f_email = Field(self, "Email or username", placeholder="you@example.com",
                             on_return=lambda: self.f_password.focus())
        self.body.addWidget(self.f_email)

        self.f_password = Field(self, "Password", placeholder="Your password",
                                password=True, mono=True,
                                on_return=self._save)
        self.body.addWidget(self.f_password)
        self.body.addSpacing(4)

        gen_row = QHBoxLayout()
        gen_row.setSpacing(10)
        self.btn_generate = Button(self, "Generate password", self._generate,
                                   variant="secondary", height=40, radius=12,
                                   icon="sparkle", font_size=13)
        gen_row.addWidget(self.btn_generate)
        gen_row.addStretch(1)
        self.body.addLayout(gen_row)
        self.body.addSpacing(14)

        btns = QHBoxLayout()
        btns.setSpacing(10)
        self.btn_cancel = Button(self, "Cancel", self.close,
                                 variant="ghost", height=46, radius=13, font_size=14)
        self.btn_save = Button(self, "Save password", self._save,
                               variant="primary", height=46, radius=13, icon="check", font_size=14)
        btns.addWidget(self.btn_cancel)
        btns.addWidget(self.btn_save, 1)
        self.body.addLayout(btns)

        if index is not None:
            self.f_platform.set_value(platform)
            self.f_email.set_value(email)
            self.f_password.set_value(password)

    def focus_first(self):
        self.f_platform.focus()

    def _generate(self):
        from .. import services
        self.f_password.set_value(services.generate_password())
        self.app.toast("Strong password generated", "info")

    def _save(self):
        platform = self.f_platform.value.strip()
        email = self.f_email.value.strip()
        pw = self.f_password.value
        ok = True
        if not platform:
            self.f_platform.set_error(True)
            self.f_platform.set_hint("Platform is required")
            ok = False
        if not email:
            self.f_email.set_error(True)
            self.f_email.set_hint("Login is required")
            ok = False
        if not pw:
            self.f_password.set_error(True)
            self.f_password.set_hint("Password is required")
            ok = False
        if not ok:
            return

        services = self.app.services
        if self.index is None:
            services.add_entry(platform, email, pw, self.key)
            self.app.toast("Password added to your vault", "success")
        else:
            services.update_entry(self.index, platform, email, pw, self.key)
            self.app.toast("Password updated", "success")
        self.app.close_modal()
        if self.on_saved:
            self.on_saved()


class ConfirmModal(ModalCard):
    def __init__(self, app, *, title, message, confirm_text="Delete", on_confirm=None):
        super().__init__(app, 430, 280, title)
        self.on_confirm = on_confirm
        self.body.addStretch(1)

        m = QLabel(message, self)
        m.setFont(th.font(13))
        m.setStyleSheet(f"""
                    color: {th.TEXT.name()};
                    background-color: transparent;
                """)
        m.setWordWrap(True)
        m.setAlignment(Qt.AlignCenter)
        self.body.addWidget(m)
        self.body.addSpacing(6)

        btns = QHBoxLayout()
        btns.setSpacing(10)
        self.btn_cancel = Button(self, "Cancel", self.close,
                                 variant="ghost", height=44, radius=13, font_size=14)
        self.btn_confirm = Button(self, confirm_text, self._confirm,
                                  variant="danger", height=44, radius=13, icon="trash", font_size=14)
        btns.addWidget(self.btn_cancel)
        btns.addWidget(self.btn_confirm, 1)
        self.body.addLayout(btns)
        self.body.addStretch(1)

    def focus_first(self):
        self.btn_cancel.setFocus()

    def _confirm(self):
        self.app.close_modal()
        if self.on_confirm:
            self.on_confirm()
