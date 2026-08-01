import math

from PyQt5.QtCore import QEasingCurve, QPointF, QRectF, Qt, QTimer, QEvent
from PyQt5.QtGui import QColor, QPainter, QRadialGradient, QFont, QLinearGradient, QPen
from PyQt5.QtWidgets import QApplication, QWidget

from . import theme as th
from . import fx
from .widgets import Toast


# ---------------------------------------------------------------------------
# Animated aurora background
# ---------------------------------------------------------------------------

class Aurora(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.t = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(40)

    def _tick(self):
        self.t += 0.004
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, th.BG)
        t = self.t
        blobs = [
            (0.82, 0.18, 0.40, th.ACCENT, 0.20, 2.1),
            (0.16, 0.75, 0.38, th.TEAL, 0.13, 1.4),
            (0.90, 0.85, 0.34, th.ACCENT_2, 0.11, 1.8),
            (0.30, 0.06, 0.32, QColor("#2a2f6b"), 0.32, 0.9),
        ]
        for bx, by, br, color, alpha, speed in blobs:
            cx = w * (bx + 0.06 * math.sin(t * speed))
            cy = h * (by + 0.05 * math.cos(t * speed * 0.8))
            r = w * br
            g = QRadialGradient(QPointF(cx, cy), r)
            c = QColor(color)
            c.setAlphaF(alpha)
            g.setColorAt(0, c)
            c0 = QColor(color)
            c0.setAlphaF(0)
            g.setColorAt(1, c0)
            p.setPen(Qt.NoPen)
            p.setBrush(g)
            p.drawEllipse(QRectF(cx - r, cy - r, 2 * r, 2 * r))


# ---------------------------------------------------------------------------
# Modal host (dim overlay + centered card)
# ---------------------------------------------------------------------------

class ModalHost(QWidget):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, app.width(), app.height())
        self._content = None
        self._dim = 0.0
        self.hide()

    def paintEvent(self, e):
        if self._dim <= 0.0:
            return
        p = QPainter(self)
        c = QColor(th.OVERLAY)
        c.setAlphaF(self._dim)
        p.fillRect(0, 0, self.width(), self.height(), c)

    def open(self, content):
        self._content = content
        content.setParent(self)
        self._center(content)
        self._dim = 0.0
        self.show()
        self.raise_()
        fx.tween(lambda v: (setattr(self, "_dim", v) or self.update()),
                 0.0, 1.0, 180)
        g = content.geometry()
        fx.tween(lambda v: content.setGeometry(g.x(), int(v), g.width(), g.height()),
                 g.y() - 18.0, float(g.y()), 340, QEasingCurve.OutBack)

    def _center(self, content):
        g = content.geometry()
        content.setGeometry(int((self.width() - g.width()) / 2),
                            int((self.height() - g.height()) / 2),
                            g.width(), g.height())

    def close(self):
        if not self.isVisible():
            return

        def done():
            self._content.setParent(None)
            self._content.deleteLater()
            self._content = None
            self.hide()

        fx.tween(lambda v: (setattr(self, "_dim", v) or self.update()),
                 1.0, 0.0, 150, on_finish=done)

    def resizeEvent(self, e):
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        if self._content:
            self._center(self._content)
        super().resizeEvent(e)

    def mousePressEvent(self, e):
        if self._content and not self._content.geometry().contains(e.pos()):
            self.app.close_modal()
            return
        super().mousePressEvent(e)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.app.close_modal()
            return
        super().keyPressEvent(e)


# ---------------------------------------------------------------------------
# Main application window
# ---------------------------------------------------------------------------

class App(QWidget):
    def __init__(self, services):
        super().__init__()
        self.services = services
        self.key = None
        self.login = None
        self.screen = None
        self.modal = None
        self._toast = None

        self.setWindowTitle("RunesCrypt")
        self.resize(1040, 920)
        self.setMinimumSize(880, 620)
        self.setStyleSheet(f"background-color: {th.BG.name()};")

        self.aurora = Aurora(self)
        self.aurora.setGeometry(0, 0, self.width(), self.height())

        self.screen_box = QWidget(self)
        self.screen_box.setAttribute(Qt.WA_TranslucentBackground)
        self.screen_box.setGeometry(0, 0, self.width(), self.height())

        self.modal_host = ModalHost(self)

        from .screens.login import LoginScreen
        from .screens.create import CreateScreen
        self.show_screen(LoginScreen if services.user_file_exists() else CreateScreen)

    def resizeEvent(self, e):
        self.aurora.setGeometry(0, 0, self.width(), self.height())
        self.screen_box.setGeometry(0, 0, self.width(), self.height())
        if self.screen is not None:
            self.screen.setGeometry(0, 0, self.width(), self.height())
        self.modal_host.setGeometry(0, 0, self.width(), self.height())
        if self._toast:
            try:
                self._toast.move(self.width() - self._toast.width() - 24, self._toast.pos().y())
            except RuntimeError:
                self._toast = None
        super().resizeEvent(e)

    # ------------------------------------------------------------ screens
    def show_screen(self, cls, **kw):
        if self.screen is not None:
            self.screen.setParent(None)
            self.screen.deleteLater()
        self.screen = cls(self, **kw)
        self.screen.setGeometry(0, 0, self.screen_box.width(), self.screen_box.height())
        self.screen.show()
        self.screen.raise_()
        self._slide_in(self.screen)

    def transition(self, cls, **kw):
        if self.screen is None:
            self.show_screen(cls, **kw)
            return
        old = self.screen
        g = old.geometry()
        fx.tween(lambda v: old.setGeometry(g.x(), int(g.y() - v), g.width(), g.height()),
                 0.0, 18.0, 170, QEasingCurve.InCubic,
                 on_finish=lambda: self.show_screen(cls, **kw))

    def _slide_in(self, widget, dist=22):
        g = widget.geometry()
        fx.tween(lambda v: widget.setGeometry(g.x(), int(g.y() + dist - v), g.width(), g.height()),
                 float(dist), 0.0, 320, QEasingCurve.OutCubic)

    # ------------------------------------------------------------- modals
    def open_modal(self, content):
        if self.modal is not None:
            self.close_modal()
        self.modal = content
        self.modal_host.open(content)
        if hasattr(content, "focus_first"):
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(0, content.focus_first)

    def close_modal(self):
        if self.modal is not None:
            self.modal = None
            self.modal_host.close()

    # -------------------------------------------------------------- toast
    def toast(self, message, kind="success"):
        if self._toast is not None:
            try:
                self._toast.deleteLater()
            except RuntimeError:
                pass
            self._toast = None
        t = Toast(self, message, kind)
        t.animate_in()
        self._toast = t

        def cleanup():
            try:
                t.deleteLater()
            except RuntimeError:
                pass
            if self._toast is t:
                self._toast = None

        QTimer.singleShot(2400, cleanup)

    def copy(self, text, label="Copied to clipboard"):
        QApplication.clipboard().setText(text)
        self.toast(label, "success")
