from PyQt5.QtCore import QRectF, Qt, QTimer
from PyQt5.QtGui import QColor, QLinearGradient, QPainter, QPen
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .. import theme as th
from .. import icons
from .. import fx
from ..widgets import Button, Field
from .base import GlassCard, Screen


class Brand(QWidget):
    def __init__(self, parent, size=56):
        super().__init__(parent)
        self.size = size
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        s = self.size
        g = QLinearGradient(0, 0, s, s)
        g.setColorAt(0, th.ACCENT)
        g.setColorAt(1, th.ACCENT_2)
        p.setPen(Qt.NoPen)
        p.setBrush(g)
        p.drawRoundedRect(QRectF(0, 0, s, s), 18, 18)
        p.setPen(QPen(QColor(255, 255, 255, 40), 2))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(1.5, 1.5, s - 3, s - 3), 17, 17)
        icons.paint(p, "lock", s / 2, s / 2, 28, QColor("#ffffff"))


class AuthScreen(Screen):
    card_min_w = 380
    card_max_w = 860
    card_min_h = 500
    card_max_h = 700

    def build(self):
        self.card = GlassCard(self, self.card_min_w, self.card_max_w,
                              self.card_min_h, self.card_max_h)
        self._center_card()
        self._build_card()

    def resizeEvent(self, e):
        if hasattr(self, "card"):
            self._center_card()
        super().resizeEvent(e)

    def _center_card(self):
        m = 24
        w = min(self.card_max_w, max(self.card_min_w, int(self.width() * 0.62)))
        h = min(self.card_max_h, max(self.card_min_h, self.height() - 2 * m))
        self.card.resize(w, h)
        self.card.move(max(0, (self.width() - w) // 2),
                       max(0, (self.height() - h) // 2))

    def _build_card(self):
        raise NotImplementedError

    def _brand_block(self):
        lay = QVBoxLayout()
        lay.setSpacing(8)
        lay.addWidget(Brand(self.card, 54), 0, Qt.AlignHCenter)
        return lay

    def _shake(self):
        x0 = self.card.x()

        def go(step):
            if step > 6:
                self.card.move(x0, self.card.y())
                return
            dx = int(10 * (1 - step / 7.0))
            self.card.move(x0 + (dx if step % 2 == 0 else -dx), self.card.y())
            QTimer.singleShot(40, lambda: go(step + 1))

        go(0)
