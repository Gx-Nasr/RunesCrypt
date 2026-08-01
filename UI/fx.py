from PyQt5.QtCore import QEasingCurve, QTimer, QVariantAnimation
from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QRectF


def rounded_path(w, h, r):
    r = min(r, w / 2.0, h / 2.0)
    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, float(w), float(h)), r, r)
    return path


_active = []


def tween(on_update, start, end, duration=160, easing=QEasingCurve.OutCubic, on_finish=None):
    anim = QVariantAnimation()
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setDuration(int(duration))
    anim.setEasingCurve(easing)

    def _update(v):
        try:
            on_update(v)
        except RuntimeError:
            pass

    anim.valueChanged.connect(_update)

    def _finish():
        if anim in _active:
            _active.remove(anim)
        if on_finish:
            on_finish()

    anim.finished.connect(_finish)
    _active.append(anim)
    anim.start()
    return anim
