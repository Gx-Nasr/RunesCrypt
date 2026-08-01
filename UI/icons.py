from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QBrush, QPolygonF


def _pen(color, width=2.0, cap=Qt.RoundCap, join=Qt.RoundJoin):
    p = QPen(color, width)
    p.setCapStyle(cap)
    p.setJoinStyle(join)
    return p


def _path_circle(cx, cy, r, color, painter, width=2.0, fill=None):
    painter.setPen(_pen(color, width))
    painter.setBrush(fill if fill is not None else Qt.NoBrush)
    painter.drawEllipse(QRectF(cx - r, cy - r, 2 * r, 2 * r))


def paint(painter, name, cx, cy, s, color):
    painter.save()
    painter.setRenderHint(QPainter.Antialiasing)
    painter.translate(cx, cy)
    painter.scale(s / 24.0, s / 24.0)
    painter.translate(-12, -12)
    if name == "lock":
        _lock(painter, color)
    elif name == "eye":
        _eye(painter, color, off=False)
    elif name == "eye_off":
        _eye(painter, color, off=True)
    elif name == "copy":
        _copy(painter, color)
    elif name == "edit":
        _edit(painter, color)
    elif name == "trash":
        _trash(painter, color)
    elif name == "plus":
        _plus(painter, color)
    elif name == "search":
        _search(painter, color)
    elif name == "key":
        _key(painter, color)
    elif name == "shield":
        _shield(painter, color)
    elif name == "logout":
        _logout(painter, color)
    elif name == "check":
        _check(painter, color)
    elif name == "x":
        _x(painter, color)
    elif name == "sparkle":
        _sparkle(painter, color)
    elif name == "clipboard":
        _clipboard(painter, color)
    elif name == "user":
        _user(painter, color)
    painter.restore()


def _lock(p, c):
    body = QRectF(5, 10, 14, 10)
    p.setPen(_pen(c, 2))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(body, 2.5, 2.5)
    p.setPen(_pen(c, 2.4))
    path = QPainterPath()
    path.moveTo(8, 10)
    path.arcTo(QRectF(7.5, 4.5, 9, 9), 180, 180)
    p.drawPath(path)
    p.setPen(_pen(c, 1.8))
    p.drawPoint(QPointF(12, 14))


def _eye(p, c, off):
    path = QPainterPath()
    path.moveTo(3, 12)
    path.quadTo(7.5, 6.5, 12, 12)
    path.quadTo(16.5, 17.5, 21, 12)
    path.quadTo(16.5, 6.5, 12, 12)
    path.quadTo(7.5, 17.5, 3, 12)
    p.setPen(_pen(c, 1.9))
    p.setBrush(Qt.NoBrush)
    p.drawPath(path)
    _path_circle(12, 12, 2.2, c, p, 1.8)
    if off:
        p.setPen(_pen(c, 1.9))
        p.drawLine(QPointF(4, 20), QPointF(20, 4))


def _copy(p, c):
    p.setPen(_pen(c, 1.9))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(9, 4, 11, 11), 2, 2)
    p.drawRoundedRect(QRectF(4, 9, 11, 11), 2, 2)


def _edit(p, c):
    p.setPen(_pen(c, 2))
    p.setBrush(Qt.NoBrush)
    p.drawLine(QPointF(5, 19), QPointF(7.5, 15.5))
    p.drawLine(QPointF(15, 5), QPointF(19.5, 9.5))
    p.drawLine(QPointF(9, 17), QPointF(19.5, 6.5))
    p.drawLine(QPointF(5, 19), QPointF(9, 17))
    p.drawLine(QPointF(15, 5), QPointF(19.5, 9.5))


def _trash(p, c):
    p.setPen(_pen(c, 1.9))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(5, 7, 14, 13), 2, 2)
    p.drawLine(QPointF(4, 5), QPointF(20, 5))
    p.drawLine(QPointF(9, 5), QPointF(9, 3))
    p.drawLine(QPointF(15, 5), QPointF(15, 3))
    p.drawLine(QPointF(9, 10), QPointF(9, 17))
    p.drawLine(QPointF(13, 10), QPointF(13, 17))
    p.drawLine(QPointF(17, 10), QPointF(17, 17))


def _plus(p, c):
    p.setPen(_pen(c, 2.4))
    p.drawLine(QPointF(12, 6), QPointF(12, 18))
    p.drawLine(QPointF(6, 12), QPointF(18, 12))


def _search(p, c):
    _path_circle(10.5, 10.5, 5.5, c, p, 2)
    p.setPen(_pen(c, 2.4))
    p.drawLine(QPointF(14.8, 14.8), QPointF(20, 20))


def _key(p, c):
    _path_circle(9, 11, 4.5, c, p, 2)
    p.setPen(_pen(c, 2))
    p.drawLine(QPointF(13, 15), QPointF(18, 20))
    p.drawLine(QPointF(17, 17), QPointF(19.5, 17))
    p.drawLine(QPointF(15.5, 19), QPointF(18, 19))


def _shield(p, c):
    path = QPainterPath()
    path.moveTo(12, 3)
    path.lineTo(20, 6)
    path.lineTo(20, 11.5)
    path.quadTo(20, 17, 12, 21)
    path.quadTo(4, 17, 4, 11.5)
    path.lineTo(4, 6)
    path.closeSubpath()
    p.setPen(_pen(c, 1.8))
    p.setBrush(Qt.NoBrush)
    p.drawPath(path)
    p.setPen(_pen(c, 2.2))
    p.drawLine(QPointF(8, 12), QPointF(11, 15))
    p.drawLine(QPointF(11, 15), QPointF(16.5, 9))


def _logout(p, c):
    p.setPen(_pen(c, 1.9))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(3, 5, 10, 14), 2, 2)
    p.setPen(_pen(c, 2.2))
    p.drawLine(QPointF(13, 12), QPointF(20, 12))
    p.drawLine(QPointF(17, 8), QPointF(20, 12))
    p.drawLine(QPointF(17, 16), QPointF(20, 12))


def _check(p, c):
    p.setPen(_pen(c, 2.6))
    p.drawLine(QPointF(5, 12.5), QPointF(10, 17.5))
    p.drawLine(QPointF(10, 17.5), QPointF(19, 6.5))


def _x(p, c):
    p.setPen(_pen(c, 2.2))
    p.drawLine(QPointF(6, 6), QPointF(18, 18))
    p.drawLine(QPointF(18, 6), QPointF(6, 18))


def _sparkle(p, c):
    p.setPen(_pen(c, 2))
    p.drawLine(QPointF(12, 4), QPointF(12, 9))
    p.drawLine(QPointF(12, 15), QPointF(12, 20))
    p.drawLine(QPointF(4, 12), QPointF(9, 12))
    p.drawLine(QPointF(15, 12), QPointF(20, 12))
    p.drawLine(QPointF(6.5, 6.5), QPointF(9.5, 9.5))
    p.drawLine(QPointF(14.5, 14.5), QPointF(17.5, 17.5))
    p.drawLine(QPointF(6.5, 17.5), QPointF(9.5, 14.5))
    p.drawLine(QPointF(14.5, 9.5), QPointF(17.5, 6.5))


def _clipboard(p, c):
    p.setPen(_pen(c, 1.9))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(QRectF(5, 4, 14, 17), 2, 2)
    p.drawRoundedRect(QRectF(9, 2.5, 6, 3), 1.5, 1.5)
    p.drawLine(QPointF(9, 10), QPointF(15, 10))
    p.drawLine(QPointF(9, 13.5), QPointF(15, 13.5))
    p.drawLine(QPointF(9, 17), QPointF(13, 17))


def _user(p, c):
    _path_circle(12, 8.5, 3.8, c, p, 1.9)
    p.setPen(_pen(c, 1.9))
    p.setBrush(Qt.NoBrush)
    path = QPainterPath()
    path.moveTo(5, 19.5)
    path.quadTo(6.5, 13.5, 12, 13.5)
    path.quadTo(17.5, 13.5, 19, 19.5)
    p.drawPath(path)
