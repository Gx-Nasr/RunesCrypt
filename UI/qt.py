try:
    from PySide6.QtCore import Signal as Signal, Qt as Qt
    from PySide6.QtGui import (QPainter as QPainter, QColor as QColor,
                               QFont as QFont, QFontMetrics as QFontMetrics,
                               QPainterPath as QPainterPath, QLinearGradient as QLinearGradient,
                               QRadialGradient as QRadialGradient, QBrush as QBrush,
                               QPen as QPen, QPolygonF as QPolygonF, QImage as QImage,
                               QPixmap as QPixmap, QPainterPathStroker as QPainterPathStroker)
    from PySide6.QtWidgets import (QWidget as QWidget, QMainWindow as QMainWindow,
                                   QApplication as QApplication, QVBoxLayout as QVBoxLayout,
                                   QHBoxLayout as QHBoxLayout, QGridLayout as QGridLayout,
                                   QStackedLayout as QStackedLayout, QLabel as QLabel,
                                   QLineEdit as QLineEdit, QPushButton as QPushButton,
                                   QFrame as QFrame, QGraphicsDropShadowEffect as QGraphicsDropShadowEffect,
                                   QGraphicsOpacityEffect as QGraphicsOpacityEffect,
                                   QScrollArea as QScrollArea, QScrollBar as QScrollBar,
                                   QSizePolicy as QSizePolicy, QDialog as QDialog,
                                   QAbstractScrollArea as QAbstractScrollArea)
    from PySide6.QtCore import QPropertyAnimation as QPropertyAnimation, QEasingCurve as QEasingCurve
    from PySide6.QtCore import QPoint as QPoint, QPointF as QPointF, QRect as QRect, QRectF as QRectF, QSize as QSize
    from PySide6.QtCore import QTimer as QTimer, QEvent as QEvent
    HAS_PYSIDE = True
except ImportError:
    from PyQt5.QtCore import pyqtSignal as Signal, Qt
    from PyQt5.QtGui import (QPainter, QColor, QFont, QFontMetrics, QPainterPath,
                             QLinearGradient, QRadialGradient, QBrush, QPen, QPolygonF,
                             QImage, QPixmap)
    from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QVBoxLayout,
                                 QHBoxLayout, QGridLayout, QStackedLayout, QLabel,
                                 QLineEdit, QPushButton, QFrame,
                                 QGraphicsDropShadowEffect, QGraphicsOpacityEffect,
                                 QScrollArea, QScrollBar, QSizePolicy, QDialog,
                                 QAbstractScrollArea)
    from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QPointF, QRect, QRectF, QSize
    from PyQt5.QtCore import QTimer, QEvent
    HAS_PYSIDE = False


def enum(qt_cls, name):
    if HAS_PYSIDE:
        return getattr(qt_cls, name)
    return getattr(qt_cls, name)


WA = Qt.WindowType.AlignCenter if HAS_PYSIDE else Qt.AlignCenter
WA_HCENTER = Qt.WindowType.AlignHCenter if HAS_PYSIDE else Qt.AlignHCenter
WA_VCENTER = Qt.WindowType.AlignVCenter if HAS_PYSIDE else Qt.AlignVCenter
WA_LEFT = Qt.WindowType.AlignLeft if HAS_PYSIDE else Qt.AlignLeft
WA_RIGHT = Qt.WindowType.AlignRight if HAS_PYSIDE else Qt.AlignRight
WA_TOP = Qt.WindowType.AlignTop if HAS_PYSIDE else Qt.AlignTop
WA_BOTTOM = Qt.WindowType.AlignBottom if HAS_PYSIDE else Qt.AlignBottom
WA_NOWRAP = Qt.TextFlag.TextWordWrap if HAS_PYSIDE else Qt.TextWordWrap
