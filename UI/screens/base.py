from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QSizePolicy, QWidget

from .. import theme as th
from .. import fx


class Screen(QWidget):
    def __init__(self, app, **kw):
        super().__init__(app.screen_box)
        self.app = app
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.build(**kw)

    def build(self, **kw):
        pass

    def rebuild(self):
        pass


class GlassCard(QWidget):
    def __init__(self, parent, min_w, max_w, min_h, max_h):
        super().__init__(parent)
        self.setMinimumSize(min_w, min_h)
        self.setMaximumSize(max_w, max_h)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, e):
        w, h = self.width(), self.height()
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = fx.rounded_path(w, h, 26)
        p.fillPath(path, QColor(0, 0, 0, 0))
        p.setPen(QPen(th.BORDER, 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)
        hi = QColor(th.ACCENT_L)
        hi.setAlphaF(0.12)
        p.setPen(QPen(hi, 1.2))
        top = QRectF(2, 2, w - 4, 1)
        p.drawLine(top.topLeft(), top.topRight())
