from PyQt5.QtGui import QColor, QFont, QFontMetrics, QLinearGradient
from PyQt5.QtWidgets import QApplication

APP_NAME = "RunesCrypt"

BG = QColor("#0b0f1f")
BG_SOFT = QColor("#10142a")
SURFACE = QColor("#151a34")
SURFACE_2 = QColor("#1c2244")
SURFACE_HI = QColor("#232a52")
BORDER = QColor("#2a3158")
BORDER_2 = QColor("#3a4378")

ACCENT = QColor("#7c6cf6")
ACCENT_L = QColor("#9487ff")
ACCENT_D = QColor("#6555e0")
ACCENT_2 = QColor("#b088ff")
TEAL = QColor("#4ee6c8")
TEAL_D = QColor("#2fb89d")

TEXT = QColor("#eef1ff")
MUTED = QColor("#9aa2cc")
FAINT = QColor("#5d6490")

SUCCESS = QColor("#3ddc97")
DANGER = QColor("#ff5c7a")
DANGER_BG = QColor("#3a1722")
WARNING = QColor("#ffb86b")

OVERLAY = QColor(5, 8, 18, 180)

_FAMILY = "Noto Sans"
_MONO_FAMILY = "Noto Sans Mono"


def font(size, weight="normal"):
    f = QFont(_FAMILY)
    f.setPointSize(int(size))
    w = {"normal": QFont.Normal, "medium": QFont.Medium,
         "bold": QFont.DemiBold, "heavy": QFont.Bold}[weight]
    f.setWeight(w)
    return f


def mono(size):
    f = QFont(_MONO_FAMILY)
    f.setPointSize(int(size))
    return f


def lerp(c1, c2, t):
    return QColor(
        int(c1.red() + (c2.red() - c1.red()) * t),
        int(c1.green() + (c2.green() - c1.green()) * t),
        int(c1.blue() + (c2.blue() - c1.blue()) * t),
        int(c1.alpha() + (c2.alpha() - c1.alpha()) * t),
    )


def with_alpha(color, alpha):
    c = QColor(color)
    c.setAlpha(int(alpha))
    return c


def text_width(text, size, weight="normal"):
    m = QFontMetrics(font(size, weight))
    return m.horizontalAdvance(text)


def ellipsize(text, size, weight, max_w):
    if max_w < 20:
        return ""
    m = QFontMetrics(font(size, weight))
    if m.horizontalAdvance(text) <= max_w:
        return text
    t = text
    while t and m.horizontalAdvance(t + "\u2026") > max_w:
        t = t[:-1]
    return t + "\u2026"


AVATAR_COLORS = [
    QColor("#7c6cf6"), QColor("#4ee6c8"), QColor("#ffb86b"),
    QColor("#ff5c7a"), QColor("#5ec4ff"), QColor("#b088ff"),
    QColor("#ff8fab"), QColor("#66d9a8"),
]


def avatar_color(name):
    if not name:
        return AVATAR_COLORS[0]
    return AVATAR_COLORS[sum(ord(c) for c in name) % len(AVATAR_COLORS)]


def accent_gradient(w=1.0):
    g = QLinearGradient(0, 0, float(w), 0)
    g.setColorAt(0.0, ACCENT)
    g.setColorAt(1.0, ACCENT_2)
    return g
