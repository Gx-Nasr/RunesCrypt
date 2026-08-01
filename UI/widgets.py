import math

from PyQt5.QtCore import QEasingCurve, QRectF, Qt, QTimer, QEvent, QSize
from PyQt5.QtGui import QColor, QFontMetrics, QLinearGradient, QPainter, QPalette, QPen, QFont
from PyQt5.QtWidgets import (QGraphicsDropShadowEffect,
                             QHBoxLayout, QLabel, QLineEdit, QScrollArea, QScrollBar,
                             QSizePolicy, QVBoxLayout, QWidget)

from . import theme as th
from . import fx
from . import icons


def apply_shadow(widget, blur=40, dy=8, alpha=0.45, color=QColor(0, 0, 0)):
    eff = QGraphicsDropShadowEffect(widget)
    eff.setBlurRadius(int(blur))
    eff.setOffset(0, int(dy))
    c = QColor(color)
    c.setAlphaF(alpha)
    eff.setColor(c)
    widget.setGraphicsEffect(eff)
    return eff


def set_cursor(widget, hand=True):
    widget.setCursor(Qt.PointingHandCursor if hand else Qt.ArrowCursor)


# ---------------------------------------------------------------------------
# Rounded surface widget (base for cards / buttons / fields)
# ---------------------------------------------------------------------------

class Surface(QWidget):
    def __init__(self, parent=None, radius=16, bg=None, border=None, border_w=1):
        super().__init__(parent)
        self.radius = radius
        self.bg = QColor(bg) if bg else QColor(0, 0, 0, 0)
        self.border = QColor(border) if border else None
        self.border_w = border_w
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

    def set_bg(self, color):
        self.bg = QColor(color)
        self.update()

    def set_border(self, color, width=None):
        self.border = QColor(color) if color else None
        if width is not None:
            self.border_w = width
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = fx.rounded_path(self.width(), self.height(), self.radius)
        p.fillPath(path, self.bg)
        if self.border:
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(self.border, self.border_w))
            p.drawPath(path)


# ---------------------------------------------------------------------------
# Icon button
# ---------------------------------------------------------------------------

class IconButton(QWidget):
    clicked = None

    def __init__(self, parent, icon, on_click, size=30, radius=9, bg=QColor(0, 0, 0, 0),
                 color=th.MUTED, hover_color=None, hover_bg=None, tooltip=""):
        super().__init__(parent)
        self.icon = icon
        self.on_click = on_click
        self.size = size
        self.radius = radius
        self.bg = QColor(bg)
        self.color = QColor(color)
        self.hover_color = QColor(hover_color) if hover_color else QColor(th.TEXT)
        self.hover_bg = QColor(hover_bg) if hover_bg else th.with_alpha(th.TEXT, 26)
        self._t = 0.0
        self._pressed = False
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TranslucentBackground)
        set_cursor(self)
        self.setToolTip(tooltip)

    def enterEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_t", v) or self.update()), 0.0, 1.0, 140)
        super().enterEvent(e)

    def leaveEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_t", v) or self.update()), 1.0, 0.0, 180)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._pressed = True
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self._pressed = False
            self.update()
            if self.on_click:
                self.on_click()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        t = self._t
        fill = self.hover_bg if self._pressed else th.lerp(self.bg, self.hover_bg, t)
        path = fx.rounded_path(self.size, self.size, self.radius)
        p.fillPath(path, fill)
        col = th.lerp(self.color, self.hover_color, t)
        icons.paint(p, self.icon, self.size / 2, self.size / 2,
                    self.size * (0.84 if self._pressed else 0.9), col)


# ---------------------------------------------------------------------------
# Button
# ---------------------------------------------------------------------------

class Button(QWidget):
    def __init__(self, parent, text="", on_click=None, variant="primary", height=50,
                 radius=14, icon=None, font_size=14, width=None, bg=th.BG):
        super().__init__(parent)
        self.text = text
        self.on_click = on_click
        self.variant = variant
        self._height = height
        self.radius = radius
        self.icon = icon
        self.font_size = font_size
        self.bg_ref = QColor(bg)
        self._t = 0.0
        self._pressed = False
        self._loading = False
        self._spin = 0.0
        self._timer = None
        self.setFixedHeight(self._height)
        if width:
            self.setFixedWidth(width)
        self.setAttribute(Qt.WA_TranslucentBackground)
        set_cursor(self)
        self._colors()

    def sizeHint(self):
        fm = QFontMetrics(th.font(self.font_size, "bold"))
        w = fm.horizontalAdvance(self.text) + 40
        if self.icon:
            w += self.font_size + 8
        return QSize(int(w), self._height)

    def _colors(self):
        if self.variant == "primary":
            self.fill = th.accent_gradient(300)
            self.fg = QColor("#ffffff")
            self.hover = 0.08
            self.border = None
        elif self.variant == "secondary":
            self.fill = QColor(0, 0, 0, 0)
            self.fg = QColor(th.TEXT)
            self.hover = 0.0
            self.border = th.BORDER
        elif self.variant == "danger":
            self.fill = QColor(th.DANGER)
            self.fg = QColor("#ffffff")
            self.hover = 0.10
            self.border = None
        elif self.variant == "ghost":
            self.fill = QColor(0, 0, 0, 0)
            self.fg = QColor(th.MUTED)
            self.hover = 0.0
            self.border = None

    def set_loading(self, flag):
        self._loading = bool(flag)
        if flag:
            self._timer = QTimer(self)
            self._timer.timeout.connect(lambda: (setattr(self, "_spin", (self._spin + 0.25) % 6.283) or self.update()))
            self._timer.start(33)
        elif self._timer:
            self._timer.stop()
            self._timer = None
        self.setEnabled(not self._loading)
        self.update()

    def enterEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_t", v) or self.update()), 0.0, 1.0, 150)
        super().enterEvent(e)

    def leaveEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_t", v) or self.update()), 1.0, 0.0, 200)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and not self._loading:
            self._pressed = True
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._pressed = False
            self.update()
            if self.rect().contains(e.pos()) and not self._loading and self.on_click:
                self.on_click()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        path = fx.rounded_path(w, h, self.radius)
        t = self._t
        if self.variant == "primary":
            fill = QLinearGradient(0, 0, w, 0)
            c1 = th.lerp(th.ACCENT, th.ACCENT_L, t)
            c2 = th.lerp(th.ACCENT_2, th.ACCENT, t)
            fill.setColorAt(0, c1)
            fill.setColorAt(1, c2)
            if self._pressed:
                fill = QLinearGradient(0, 0, w, 0)
                fill.setColorAt(0, th.ACCENT_D)
                fill.setColorAt(1, th.lerp(th.ACCENT_2, th.ACCENT_D, 0.4))
            p.fillPath(path, fill)
        else:
            base = QColor(self.bg_ref) if self.variant == "ghost" else QColor(self.fill)
            if self.variant == "secondary":
                col = th.lerp(base, th.with_alpha(th.TEXT, 26), t)
            else:
                col = th.lerp(base, th.lerp(th.BG, th.TEXT, 0.08), t * 0.6)
            if self._pressed:
                col = th.lerp(col, th.BG, 0.3)
            p.fillPath(path, col)
            if self.border:
                p.setBrush(Qt.NoBrush)
                p.setPen(QPen(th.lerp(th.BORDER, th.BORDER_2, t), 1))
                p.drawPath(path)

        p.setPen(QPen(self.fg, 1))
        p.setFont(th.font(self.font_size, "bold"))
        metrics = p.fontMetrics()
        cw = self.width() / 2
        icon_w = 0
        if self.icon:
            icon_w = self.font_size + 2
            if self._loading:
                self._draw_spinner(p, cw - metrics.horizontalAdvance(self.text) / 2 - icon_w - 4,
                                   self.height() / 2)
            else:
                icons.paint(p, self.icon, cw - metrics.horizontalAdvance(self.text) / 2 - icon_w - 2,
                            self.height() / 2, self.font_size, self.fg)
        p.drawText(QRectF(0, 0, self.width(), self.height()),
                   Qt.AlignCenter, self.text if not self._loading else "Working\u2026")

    def _draw_spinner(self, p, cx, cy):
        r = self.font_size * 0.55
        p.save()
        p.translate(cx, cy)
        p.rotate(self._spin * 57.3)
        pen = QPen(self.fg, 2.4)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.drawArc(QRectF(-r, -r, 2 * r, 2 * r), 0, 260 * 16)
        p.restore()


# ---------------------------------------------------------------------------
# Field
# ---------------------------------------------------------------------------

class Field(QWidget):
    def __init__(self, parent, label, placeholder="", password=False, bg=QColor(0, 0, 0, 0),
                hint_color=th.DANGER, on_return=None, on_change=None,
                mono=False, placeholder_color="#6E6E6E"):
        super().__init__(parent)
        self.placeholder_color = placeholder_color
        self.label = label
        self.placeholder = placeholder
        self.password = password
        self.bg = QColor(bg)
        self._show = False
        self._focused = 0.0
        self._error = False
        self._border_t = 0.0
        self.mono = mono
        self._on_return = on_return
        self._on_change = on_change
        self.setAttribute(Qt.WA_TranslucentBackground)

        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)

        self.lbl = QLabel(label.upper(), self)
        self.label_color = th.lerp(th.TEXT, th.MUTED, 0.25)
        self.lbl.setStyleSheet(f"color: {self.label_color.name()};")
        self.lbl.setFont(th.font(9, "bold"))
        if not label:
            self.lbl.hide()
        v.addWidget(self.lbl)

        self.box = _FieldBox(self, self, self.bg)
        v.addWidget(self.box)

        self.hint = QLabel("", self)
        self.hint.setStyleSheet(f"color: {th.DANGER.name()};")
        self.hint.setFont(th.font(11))
        self.hint.setVisible(False)
        v.addWidget(self.hint)

    # --- public api -------------------------------------------------------
    @property
    def value(self):
        return self.box.entry.text()

    def set_value(self, text):
        self.box.entry.setText(text)
        if self._on_change:
            self._on_change(None)

    def clear(self):
        self.set_value("")

    def set_error(self, flag):
        self._error = bool(flag)
        self.box.set_error(flag)
        if not flag:
            self.hint.setVisible(False)

    def set_hint(self, msg):
        if msg:
            self.hint.setText(msg)
            self.hint.setVisible(True)
            self.set_error(True)
        else:
            self.hint.setVisible(False)

    def focus(self):
        self.box.entry.setFocus()

    def set_placeholder(self, text):
        self.placeholder = text
        self.box.entry.setPlaceholderText(text)


class _FieldBox(QWidget):
    def __init__(self, parent, owner, bg):
        super().__init__(parent)
        self.owner = owner
        self.bg = QColor(bg)
        self._t = 0.0
        self._error = False
        self._box_h = 54
        self.setFixedHeight(54)
        self.setAttribute(Qt.WA_TranslucentBackground)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 0, 10, 0)
        lay.setSpacing(8)

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText(owner.placeholder)
        self.entry.setFont(th.mono(13) if owner.mono else th.font(13))
        self.entry.setStyleSheet(f"""
        QLineEdit {{
            background: transparent;
            border: none;
            selection-background-color: {th.ACCENT_D.name()};
            selection-color: #ffffff;
        }}
        """)
        pal = self.entry.palette()
        pal.setColor(QPalette.Text, th.TEXT)
        pal.setColor(QPalette.PlaceholderText, QColor("#9A9A9A"))
        self.entry.setPalette(pal)

        if owner.password:
            self.entry.setEchoMode(QLineEdit.Password)
        lay.addWidget(self.entry)

        if owner.password:
            self.eye = IconButton(self, "eye", self._toggle_eye, size=30,
                                  bg=bg, color=th.FAINT, hover_color=th.TEXT,
                                  hover_bg=th.with_alpha(th.TEXT, 22))
            lay.addWidget(self.eye)
        elif owner.label == "Search":
            pass

        self.entry.installEventFilter(self)
        self.entry.textChanged.connect(lambda t: self.owner._on_change and self.owner._on_change(t))

    def _toggle_eye(self):
        self.owner._show = not self.owner._show
        self.entry.setEchoMode(QLineEdit.Normal if self.owner._show else QLineEdit.Password)
        self.eye.icon = "eye_off" if self.owner._show else "eye"
        self.eye.update()

    def eventFilter(self, obj, ev):
        if obj is self.entry and ev.type() == QEvent.FocusIn:
            fx.tween(lambda v: (setattr(self, "_t", v), setattr(self.owner, "_focused", v), self.update()),
                     0.0, 1.0, 170)
            self.owner.lbl.setStyleSheet(f"color: {th.ACCENT_L.name()};")
        elif obj is self.entry and ev.type() == QEvent.FocusOut:
            fx.tween(lambda v: (setattr(self, "_t", v), setattr(self.owner, "_focused", v), self.update()),
                     1.0, 0.0, 220)
            self.owner.lbl.setStyleSheet(f"color: {self.owner.label_color.name()};")
        elif obj is self.entry and ev.type() == QEvent.KeyPress and ev.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.owner._on_return:
                self.owner._on_return()
                return True
        return super().eventFilter(obj, ev)

    def set_error(self, flag):
        self._error = bool(flag)
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        t = self._t
        if self._error:
            outline = th.DANGER
        else:
            outline = th.lerp(th.BORDER, th.ACCENT, t)
        fill = th.lerp(self.bg, th.with_alpha(th.TEXT, 26), t * 0.5) if not self._error else th.lerp(self.bg, th.DANGER_BG, 0.5)
        path = fx.rounded_path(w, h, 14)
        p.fillPath(path, fill)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(outline, 1.8 if t > 0.05 or self._error else 1.0))
        p.drawPath(path)


# ---------------------------------------------------------------------------
# Strength meter
# ---------------------------------------------------------------------------

def score_password(pw):
    if not pw:
        return 0, 0
    score = 0
    if len(pw) >= 8:
        score += 1
    if len(pw) >= 12:
        score += 1
    classes = 0
    for ch in pw:
        if ch.islower():
            classes |= 1
        elif ch.isupper():
            classes |= 2
        elif ch.isdigit():
            classes |= 4
        else:
            classes |= 8
    if classes & 1:
        score += 1
    if classes & 2:
        score += 1
    if classes & 4:
        score += 1
    if classes & 8:
        score += 1
    return min(4, max(0, score // 2)), score


class StrengthMeter(QWidget):
    LABELS = ["", "Weak", "Fair", "Good", "Strong"]

    def __init__(self, parent, bg=QColor(0, 0, 0, 0)):
        super().__init__(parent)
        self.bg = QColor(bg)
        self._level = 0
        self._target = 0
        self.setFixedHeight(18)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_password(self, pw):
        lvl, _ = score_password(pw)
        self._target = lvl
        fx.tween(lambda v: (setattr(self, "_level", v), self.update()), self._level, float(lvl), 260)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        seg_w = (w - 3 * 6) / 4.0
        colors = [th.DANGER, th.WARNING, th.ACCENT, th.SUCCESS]
        for i in range(4):
            x = i * (seg_w + 6)
            r = QRectF(x, 3, seg_w, 8)
            filled = self._level > i + 0.01
            col = colors[i] if filled else th.BORDER
            p.setPen(Qt.NoPen)
            p.setBrush(col)
            p.drawRoundedRect(r, 4, 4)
        if self._target:
            lbl = self.LABELS[min(4, int(round(self._level)))]
            idx = max(0, min(3, int(round(self._level)) - 1))
            p.setPen(colors[idx])
            p.setFont(th.font(9, "bold"))
            p.drawText(QRectF(0, 12, w, 14), Qt.AlignRight, lbl)


# ---------------------------------------------------------------------------
# Stat card
# ---------------------------------------------------------------------------

class StatCard(QWidget):
    def __init__(self, parent, icon, value, caption, color, bg=th.BG):
        super().__init__(parent)
        self.icon = icon
        self.value = value
        self.caption = caption
        self.color = QColor(color)
        self.bg = QColor(bg)
        self.setFixedHeight(92)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(140)

    def set_value(self, text):
        self.value = text
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        path = fx.rounded_path(w, h, 18)
        p.fillPath(path, QColor(0, 0, 0, 0))
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(th.BORDER, 1))
        p.drawPath(path)

        iw = 44
        g = QLinearGradient(0, 0, iw, iw)
        g.setColorAt(0, th.lerp(self.color, th.BG, 0.35))
        g.setColorAt(1, th.lerp(self.color, th.BG, 0.55))
        p.setPen(Qt.NoPen)
        p.setBrush(g)
        p.drawRoundedRect(QRectF(16, (h - iw) / 2, iw, iw), 13, 13)
        icons.paint(p, self.icon, 16 + iw / 2, h / 2, 20, self.color)

        tx = 16 + iw + 16
        p.setFont(th.font(19, "heavy"))
        p.setPen(th.TEXT)
        p.drawText(QRectF(tx, 16, w - tx - 12, 28), Qt.AlignLeft | Qt.AlignVCenter, str(self.value))
        p.setFont(th.font(11))
        p.setPen(th.MUTED)
        p.drawText(QRectF(tx, 48, w - tx - 12, 24), Qt.AlignLeft | Qt.AlignVCenter, self.caption)


# ---------------------------------------------------------------------------
# Scroll area
# ---------------------------------------------------------------------------

SCROLLBAR_CSS = """
QScrollBar:vertical {
    background: transparent; width: 10px; margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: #2a3158; border-radius: 4px; min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #3a4378; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
QScrollBar:horizontal { height: 0px; }
"""


class ScrollArea(QScrollArea):
    def __init__(self, parent=None, bg=th.BG):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet(
            f"QScrollArea {{ background: transparent; border: none; }}"
            f"QScrollArea > QWidget > QWidget {{ background: transparent; }}"
            + SCROLLBAR_CSS)
        self.viewport().setStyleSheet("background: transparent;")
        self.container = QWidget()
        self.container.setAttribute(Qt.WA_TranslucentBackground)
        self.vbox = QVBoxLayout(self.container)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.setWidget(self.container)

    def clear(self):
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.scrollTop()

    def scrollTop(self):
        QTimer.singleShot(0, lambda: self.verticalScrollBar().setValue(0))


# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------

class EmptyState(QWidget):
    def __init__(self, parent, icon="key", title="", subtitle="", action_text=None,
                 on_action=None, bg=th.BG):
        super().__init__(parent)
        self.bg = QColor(bg)
        self.setAttribute(Qt.WA_TranslucentBackground)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 10, 0, 10)
        lay.addStretch(1)

        icon_c = QWidget()
        icon_c.setFixedSize(92, 92)
        lay.addWidget(icon_c, 0, Qt.AlignHCenter)
        self._icon = icon

        t = QLabel(title, self)
        t.setFont(th.font(18, "heavy"))
        t.setStyleSheet(f"color: {th.TEXT.name()};")
        t.setAlignment(Qt.AlignCenter)
        lay.addWidget(t)

        if subtitle:
            s = QLabel(subtitle, self)
            s.setFont(th.font(13))
            s.setStyleSheet(f"color: {th.MUTED.name()};")
            s.setAlignment(Qt.AlignCenter)
            lay.addWidget(s)

        if action_text and on_action:
            b = Button(self, action_text, on_action, variant="primary", height=46,
                       radius=14, icon="plus", font_size=14, bg=bg)
            b.setFixedWidth(230)
            lay.addWidget(b, 0, Qt.AlignHCenter)

        lay.addStretch(2)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        if self._icon:
            icons.paint(p, self._icon, self.width() / 2, 74, 46, th.BORDER_2)
            icons.paint(p, self._icon, self.width() / 2, 74, 30, th.ACCENT)


# ---------------------------------------------------------------------------
# Entry card
# ---------------------------------------------------------------------------

class EntryCard(QWidget):
    HEIGHT = 108

    def __init__(self, parent, *, platform, email, password, index, color,
                 on_copy_email, on_copy_password, on_edit, on_delete, bg=th.BG):
        super().__init__(parent)
        self.platform = platform
        self.email = email
        self.password = password
        self.index = index
        self.color = QColor(color)
        self.bg = QColor(bg)
        self._revealed = False
        self._hover = 0.0
        self.on_copy_email = on_copy_email
        self.on_copy_password = on_copy_password
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.setFixedHeight(self.HEIGHT)
        self.setAttribute(Qt.WA_TranslucentBackground)
        set_cursor(self)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(18, 0, 12, 0)
        lay.setSpacing(12)

        self.avatar = AvatarWidget(self, self)
        lay.addWidget(self.avatar)

        mid = QVBoxLayout()
        mid.setSpacing(2)
        self.lbl_platform = QLabel(self.platform, self)
        self.lbl_platform.setFont(th.font(15, "bold"))
        self.lbl_platform.setStyleSheet(f"color: {th.TEXT.name()};")
        self.lbl_email = QLabel(self.email, self)
        self.lbl_email.setFont(th.font(12))
        self.lbl_email.setStyleSheet(f"color: {th.MUTED.name()};")
        self.lbl_pw = QLabel("\u2022" * min(len(self.password), 22), self)
        self.lbl_pw.setFont(th.mono(13))
        self.lbl_pw.setStyleSheet(f"color: {th.FAINT.name()};")
        mid.addWidget(self.lbl_platform)
        mid.addWidget(self.lbl_email)
        mid.addWidget(self.lbl_pw)
        lay.addLayout(mid, 1)

        btns = QHBoxLayout()
        btns.setSpacing(4)
        self._btn_eye = IconButton(self, "eye", self._toggle_reveal, size=34, radius=10,
                                   color=th.MUTED, tooltip="Show / hide")
        self._btn_copy_email = IconButton(self, "copy", self._copy_email, size=34, radius=10,
                                          color=th.MUTED, tooltip="Copy login")
        self._btn_copy_pw = IconButton(self, "clipboard", self._copy_pw, size=34, radius=10,
                                       color=th.MUTED, tooltip="Copy password")
        self._btn_edit = IconButton(self, "edit", self._edit, size=34, radius=10,
                                    color=th.MUTED, tooltip="Edit")
        self._btn_del = IconButton(self, "trash", self._delete, size=34, radius=10,
                                   color=th.MUTED, hover_color=th.DANGER,
                                   hover_bg=th.DANGER_BG, tooltip="Delete")
        for b in (self._btn_eye, self._btn_copy_email, self._btn_copy_pw,
                  self._btn_edit, self._btn_del):
            btns.addWidget(b)
        lay.addLayout(btns)

    # --- actions ----------------------------------------------------------
    def _toggle_reveal(self):
        self._revealed = not self._revealed
        self.lbl_pw.setText(self.password if self._revealed else "\u2022" * min(len(self.password), 22))
        self.lbl_pw.setStyleSheet(
            f"color: {th.TEXT.name() if self._revealed else th.FAINT.name()};")
        self.lbl_pw.setFont(th.mono(13) if self._revealed else th.font(13))
        self._btn_eye.icon = "eye_off" if self._revealed else "eye"
        self._btn_eye.update()

    def _copy_email(self):
        if self.on_copy_email:
            self.on_copy_email(self)

    def _copy_pw(self):
        if self.on_copy_password:
            self.on_copy_password(self)

    def _edit(self):
        if self.on_edit:
            self.on_edit(self)

    def _delete(self):
        if self.on_delete:
            self.on_delete(self)

    def enterEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_hover", v), self.update()), 0.0, 1.0, 160)
        super().enterEvent(e)

    def leaveEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_hover", v), self.update()), 1.0, 0.0, 200)
        super().leaveEvent(e)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        t = self._hover
        path = fx.rounded_path(w, h, 18)
        fill = th.lerp(QColor(0, 0, 0, 0), th.with_alpha(th.TEXT, 14), t)
        p.fillPath(path, fill)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(th.lerp(th.BORDER, self.color, t * 0.6), 1))
        p.drawPath(path)

    def paint_avatar(self, p):
        r = 52
        g = QLinearGradient(0, 0, r, r)
        g.setColorAt(0, th.lerp(self.color, QColor("#ffffff"), 0.12))
        g.setColorAt(1, th.lerp(self.color, th.BG, 0.25))
        p.setPen(Qt.NoPen)
        p.setBrush(g)
        p.drawRoundedRect(QRectF(0, 0, r, r), 16, 16)
        initials = self.platform[:2].upper() if self.platform else "??"
        p.setFont(th.font(15, "heavy"))
        p.setPen(QColor("#ffffff"))
        p.drawText(QRectF(0, 0, r, r), Qt.AlignCenter, initials)


class AvatarWidget(QWidget):
    def __init__(self, parent, card):
        super().__init__(parent)
        self.card = card
        self.setFixedSize(52, 52)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        self.card.paint_avatar(p)


# ---------------------------------------------------------------------------
# Link button
# ---------------------------------------------------------------------------

class LinkButton(QWidget):
    def __init__(self, parent, text, on_click, color=th.MUTED, hover=th.ACCENT_L, font_size=13):
        super().__init__(parent)
        self.text = text
        self.on_click = on_click
        self.color = QColor(color)
        self.hover = QColor(hover)
        self.font_size = font_size
        self._t = 0.0
        self.setAttribute(Qt.WA_TranslucentBackground)
        set_cursor(self)
        self.setMinimumHeight(30)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

    def sizeHint(self):
        m = self.fontMetrics()
        mf = th.font(self.font_size)
        return QSize(m.horizontalAdvance(self.text) + 8, 30)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        col = th.lerp(self.color, self.hover, self._t)
        p.setFont(th.font(13))
        p.setPen(col)
        p.drawText(QRectF(0, 0, self.width(), self.height()), Qt.AlignCenter, self.text)
        y = int(self.height() - 7)
        w = th.text_width(self.text, 13)
        p.setPen(th.lerp(self.color, self.hover, self._t))
        p.drawLine(int((self.width() - w) / 2), y, int((self.width() + w) / 2), y)

    def enterEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_t", v), self.update()), 0.0, 1.0, 140)
        super().enterEvent(e)

    def leaveEvent(self, e):
        fx.tween(lambda v: (setattr(self, "_t", v), self.update()), 1.0, 0.0, 180)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()) and self.on_click:
            self.on_click()


# ---------------------------------------------------------------------------
# Toast
# ---------------------------------------------------------------------------

class Toast(QWidget):
    def __init__(self, window, message, kind="success"):
        super().__init__(window)
        self.window = window
        self.kind = kind
        self.setAttribute(Qt.WA_TranslucentBackground)
        color = th.SUCCESS if kind == "success" else (th.DANGER if kind == "error" else th.ACCENT)
        self._color = QColor(color)
        self._icon = "check" if kind == "success" else ("x" if kind == "error" else "lock")

        h = QHBoxLayout(self)
        h.setContentsMargins(46, 0, 18, 0)
        h.setSpacing(10)
        self.setFixedHeight(48)

        self.lbl = QLabel(message, self)
        self.lbl.setFont(th.font(13))
        self.lbl.setStyleSheet(f"color: {th.TEXT.name()};")
        h.addWidget(self.lbl)

    def animate_in(self):
        self.adjustSize()
        self.setFixedHeight(48)
        self.move(self.window.width() - self.width() - 24, -48)
        self.show()
        self.raise_()
        fx.tween(lambda v: self.move(self.window.width() - self.width() - 24, int(v)),
                 -48.0, 18.0, 420, QEasingCurve.OutBack)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        path = fx.rounded_path(w, h, 16)
        g = QLinearGradient(0, 0, w, 0)
        g.setColorAt(0, QColor(0, 0, 0, 0))
        g.setColorAt(1, th.lerp(QColor(0, 0, 0, 0), self._color, 0.12))
        p.fillPath(path, g)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(th.lerp(th.BORDER, self._color, 0.5), 1))
        p.drawPath(path)
        p.setPen(Qt.NoPen)
        p.setBrush(self._color)
        p.drawEllipse(QRectF(12, (h - 22) / 2, 22, 22))
        icons.paint(p, self._icon, 23, h / 2, 12, QColor("#ffffff"))
