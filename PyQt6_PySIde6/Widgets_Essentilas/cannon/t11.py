# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

# PySide6 tutorial 11


import sys
import math

from PySide6.QtCore import QPoint, QRect, QTimer, Qt, Signal, Slot, qWarning
from PySide6.QtGui import QColor, QFont, QPainter, QPainterStateGuard, QPalette, QRegion
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout,
                               QLCDNumber, QPushButton, QSlider,
                               QVBoxLayout, QWidget)


class LCDRange(QWidget):

    value_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        lcd = QLCDNumber(2)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)

        self.slider.valueChanged.connect(lcd.display)
        self.slider.valueChanged.connect(self.value_changed)

        layout = QVBoxLayout(self)
        layout.addWidget(lcd)
        layout.addWidget(self.slider)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    @Slot(int)
    def set_value(self, value):
        self.slider.setValue(value)

    def set_range(self, minValue, maxValue):
        if minValue < 0 or maxValue > 99 or minValue > maxValue:
            qWarning(f"LCDRange::setRange({minValue}, {maxValue})\n"
                     "\tRange must be 0..99\n"
                     "\tand minValue must not be greater than maxValue")
            return

        self.slider.setRange(minValue, maxValue)


class CannonField(QWidget):

    angle_changed = Signal(int)
    force_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current_angle = 45
        self._current_force = 0
        self._timer_count = 0
        self._auto_shoot_timer = QTimer(self)
        self._auto_shoot_timer.timeout.connect(self.move_shot)
        self._shoot_angle = 0
        self._shoot_force = 0
        self.setPalette(QPalette(QColor(250, 250, 200)))
        self.setAutoFillBackground(True)

    def angle(self):
        return self._current_angle

    @Slot(int)
    def set_angle(self, angle):
        if angle < 5:
            angle = 5
        if angle > 70:
            angle = 70
        if self._current_angle == angle:
            return
        self._current_angle = angle
        self.update()
        self.angle_changed.emit(self._current_angle)

    def force(self):
        return self._current_force

    @Slot(int)
    def set_force(self, force):
        if force < 0:
            force = 0
        if self._current_force == force:
            return
        self._current_force = force
        self.force_changed.emit(self._current_force)

    @Slot()
    def shoot(self):
        if self._auto_shoot_timer.isActive():
            return
        self._timer_count = 0
        self._shoot_angle = self._current_angle
        self._shoot_force = self._current_force
        self._auto_shoot_timer.start(5)

    @Slot()
    def move_shot(self):
        region = QRegion(self.shot_rect())
        self._timer_count += 1

        shot_r = self.shot_rect()

        if shot_r.x() > self.width() or shot_r.y() > self.height():
            self._auto_shoot_timer.stop()
        else:
            region = region.united(QRegion(shot_r))

        self.update(region)

    def paintEvent(self, event):
        with QPainter(self) as painter:
            self.paint_cannon(painter)
            if self._auto_shoot_timer.isActive():
                self.paint_shot(painter)

    def paint_shot(self, painter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawRect(self.shot_rect())

    barrel_rect = QRect(33, -4, 15, 8)

    def paint_cannon(self, painter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.GlobalColor.blue)

        with QPainterStateGuard(painter):
            painter.translate(0, self.height())
            painter.drawPie(QRect(-35, -35, 70, 70), 0, 90 * 16)
            painter.rotate(-self._current_angle)
            painter.drawRect(CannonField.barrel_rect)

    def cannon_rect(self):
        result = QRect(0, 0, 50, 50)
        result.moveBottomLeft(self.rect().bottomLect())
        return result

    def shot_rect(self):
        gravity = 4.0

        time = self._timer_count / 40.0
        velocity = self._shoot_force
        radians = self._shoot_angle * math.pi / 180

        velx = velocity * math.cos(radians)
        vely = velocity * math.sin(radians)
        x0 = (CannonField.barrel_rect.right() + 5) * math.cos(radians)
        y0 = (CannonField.barrel_rect.right() + 5) * math.sin(radians)
        x = x0 + velx * time
        y = y0 + vely * time - 0.5 * gravity * time * time

        result = QRect(0, 0, 6, 6)
        result.moveCenter(QPoint(round(x), self.height() - 1 - round(y)))
        return result


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        quit = QPushButton("&Quit")
        quit.setFont(QFont("Times", 18, QFont.Weight.Bold))

        quit.clicked.connect(qApp.quit)  # noqa: F821

        angle = LCDRange()
        angle.set_range(5, 70)

        force = LCDRange()
        force.set_range(10, 50)

        cannon_field = CannonField()

        angle.value_changed.connect(cannon_field.set_angle)
        cannon_field.angle_changed.connect(angle.set_value)

        force.value_changed.connect(cannon_field.set_force)
        cannon_field.force_changed.connect(force.set_value)

        shoot = QPushButton("&Shoot")
        shoot.setFont(QFont("Times", 18, QFont.Weight.Bold))

        shoot.clicked.connect(cannon_field.shoot)

        top_layout = QHBoxLayout()
        top_layout.addWidget(shoot)
        top_layout.addStretch(1)

        left_layout = QVBoxLayout()
        left_layout.addWidget(angle)
        left_layout.addWidget(force)

        grid_layout = QGridLayout(self)
        grid_layout.addWidget(quit, 0, 0)
        grid_layout.addLayout(top_layout, 0, 1)
        grid_layout.addLayout(left_layout, 1, 0)
        grid_layout.addWidget(cannon_field, 1, 1, 2, 1)
        grid_layout.setColumnStretch(1, 10)

        angle.set_value(60)
        force.set_value(25)
        angle.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setGeometry(100, 100, 500, 355)
    widget.show()
    sys.exit(app.exec())
