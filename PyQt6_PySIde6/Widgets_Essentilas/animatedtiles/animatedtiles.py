# Copyright (C) 2010 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

import sys
import math

from PySide6.QtCore import (QEasingCurve, QObject, QParallelAnimationGroup,
                            QPointF, QPropertyAnimation, QRandomGenerator,
                            QRectF, QTimer, Qt, Property, Signal)
from PySide6.QtGui import (QBrush, QLinearGradient, QPainter,
                           QPainterPath, QPixmap, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                               QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                               QGraphicsWidget, QStyle)
from PySide6.QtStateMachine import QState, QStateMachine

import animatedtiles_rc  # noqa: F401


# Deriving from more than one wrapped class is not supported, so we use
# composition and delegate the property.
class Pixmap(QObject):
    def __init__(self, pix):
        super().__init__()

        self.pixmap_item = QGraphicsPixmapItem(pix)
        self.pixmap_item.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

    def set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    def get_pos(self):
        return self.pixmap_item.pos()

    pos = Property(QPointF, get_pos, set_pos)


class Button(QGraphicsWidget):
    pressed = Signal()

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)

        self._pix = pixmap

        self.setAcceptHoverEvents(True)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

    def boundingRect(self):
        return QRectF(-65, -65, 130, 130)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())

        return path

    def paint(self, painter, option, widget):
        down = option.state & QStyle.StateFlag.State_Sunken
        r = self.boundingRect()

        grad = QLinearGradient(r.topLeft(), r.bottomRight())
        if option.state & QStyle.StateFlag.State_MouseOver:
            color_0 = Qt.GlobalColor.white
        else:
            color_0 = Qt.GlobalColor.lightGray

        color_1 = Qt.GlobalColor.darkGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(Qt.GlobalColor.darkGray)
        painter.setBrush(grad)
        painter.drawEllipse(r)

        color_0 = Qt.GlobalColor.darkGray
        color_1 = Qt.GlobalColor.lightGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(grad)

        if down:
            painter.translate(2, 2)

        painter.drawEllipse(r.adjusted(5, 5, -5, -5))
        painter.drawPixmap(-self._pix.width() / 2, -self._pix.height() / 2,
                           self._pix)

    def mousePressEvent(self, ev):
        self.pressed.emit()
        self.update()

    def mouseReleaseEvent(self, ev):
        self.update()


class View(QGraphicsView):
    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    kinetic_pix = QPixmap(':/images/kinetic.png')
    bg_pix = QPixmap(':/images/Time-For-Lunch-2.jpg')

    scene = QGraphicsScene(-350, -350, 700, 700)

    items = []
    for i in range(64):
        item = Pixmap(kinetic_pix)
        item.pixmap_item.setOffset(-kinetic_pix.width() / 2,
                                   -kinetic_pix.height() / 2)
        item.pixmap_item.setZValue(i)
        items.append(item)
        scene.addItem(item.pixmap_item)

    # Buttons.
    button_parent = QGraphicsRectItem()
    ellipse_button = Button(QPixmap(':/images/ellipse.png'), button_parent)
    figure_8button = Button(QPixmap(':/images/figure8.png'), button_parent)
    random_button = Button(QPixmap(':/images/random.png'), button_parent)
    tiled_button = Button(QPixmap(':/images/tile.png'), button_parent)
    centered_button = Button(QPixmap(':/images/centered.png'), button_parent)

    ellipse_button.setPos(-100, -100)
    figure_8button.setPos(100, -100)
    random_button.setPos(0, 0)
    tiled_button.setPos(-100, 100)
    centered_button.setPos(100, 100)

    scene.addItem(button_parent)
    button_parent.setTransform(QTransform().scale(0.75, 0.75))
    button_parent.setPos(200, 200)
    button_parent.setZValue(65)

    # States.
    root_state = QState()
    ellipse_state = QState(root_state)
    figure_8state = QState(root_state)
    random_state = QState(root_state)
    tiled_state = QState(root_state)
    centered_state = QState(root_state)

    # Values.
    generator = QRandomGenerator.global_()

    for i, item in enumerate(items):
        # Ellipse.
        ellipse_state.assignProperty(item, 'pos',
                                     QPointF(math.cos((i / 63.0) * 6.28) * 250,
                                             math.sin((i / 63.0) * 6.28) * 250))

        # Figure 8.
        figure_8state.assignProperty(item, 'pos',
                                     QPointF(math.sin((i / 63.0) * 6.28) * 250,
                                             math.sin(((i * 2) / 63.0) * 6.28) * 250))

        # Random.
        random_state.assignProperty(item, 'pos',
                                    QPointF(-250 + generator.bounded(0, 500),
                                            -250 + generator.bounded(0, 500)))

        # Tiled.
        width = kinetic_pix.width()
        height = kinetic_pix.height()
        tiled_state.assignProperty(item, 'pos',
                                   QPointF(((i % 8) - 4) * width + width / 2,
                                           ((i // 8) - 4) * height + height / 2))

        # Centered.
        centered_state.assignProperty(item, 'pos', QPointF())

    # Ui.
    view = View(scene)
    view.setWindowTitle("Animated Tiles")
    view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
    view.setBackgroundBrush(QBrush(bg_pix))
    view.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
    view.setRenderHints(QPainter.RenderHint.Antialiasing
                        | QPainter.RenderHint.SmoothPixmapTransform)
    view.show()

    states = QStateMachine()
    states.addState(root_state)
    states.setInitialState(root_state)
    root_state.setInitialState(centered_state)

    group = QParallelAnimationGroup()
    for i, item in enumerate(items):
        anim = QPropertyAnimation(item, b'pos')
        anim.setDuration(750 + i * 25)
        anim.setEasingCurve(QEasingCurve.Type.InOutBack)
        group.addAnimation(anim)

    trans = root_state.addTransition(ellipse_button.pressed, ellipse_state)
    trans.addAnimation(group)

    trans = root_state.addTransition(figure_8button.pressed, figure_8state)
    trans.addAnimation(group)

    trans = root_state.addTransition(random_button.pressed, random_state)
    trans.addAnimation(group)

    trans = root_state.addTransition(tiled_button.pressed, tiled_state)
    trans.addAnimation(group)

    trans = root_state.addTransition(centered_button.pressed, centered_state)
    trans.addAnimation(group)

    timer = QTimer()
    timer.start(125)
    timer.setSingleShot(True)
    trans = root_state.addTransition(timer.timeout, ellipse_state)
    trans.addAnimation(group)

    states.start()

    sys.exit(app.exec())
