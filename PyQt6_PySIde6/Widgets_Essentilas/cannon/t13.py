# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

# PySide6 tutorial 13


import sys
import math
import random

from PySide6.QtCore import (QPoint, QRect, QTime, QTimer, Qt,
                            Signal, Slot, qWarning)
from PySide6.QtGui import QColor, QFont, QPainter, QPainterStateGuard, QPalette, QRegion
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
                               QLCDNumber, QPushButton, QSizePolicy, QSlider,
                               QVBoxLayout, QWidget)


class LCDRange(QWidget):

    value_changed = Signal(int)

    def __init__(self, text=None, parent=None):
        if isinstance(text, QWidget):
            parent = text
            text = None

        super().__init__(parent)

        self.init()

        if text:
            self.set_text(text)

    def init(self):
        lcd = QLCDNumber(2)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.slider.valueChanged.connect(lcd.display)
        self.slider.valueChanged.connect(self.value_changed)

        layout = QVBoxLayout(self)
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    @Slot(int)
    def set_value(self, value):
        self.slider.setValue(value)

    def text(self):
        return self.label.text()

    def set_range(self, minValue, maxValue):
        if minValue < 0 or maxValue > 99 or minValue > maxValue:
            qWarning(f"LCDRange::setRange({minValue}, {maxValue})\n"
                     "\tRange must be 0..99\n"
                     "\tand minValue must not be greater than maxValue")
            return

        self.slider.setRange(minValue, maxValue)

    def set_text(self, text):
        self.label.setText(text)


class CannonField(QWidget):

    angle_changed = Signal(int)
    force_changed = Signal(int)
    hit = Signal()
    missed = Signal()
    can_shoot = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current_angle = 45
        self._current_force = 0
        self._timer_count = 0
        self._auto_shoot_timer = QTimer(self)
        self._auto_shoot_timer.timeout.connect(self.move_shot)
        self._shoot_angle = 0
        self._shoot_force = 0
        self.target = QPoint(0, 0)
        self._game_ended = False
        self.setPalette(QPalette(QColor(250, 250, 200)))
        self.setAutoFillBackground(True)
        self.new_target()

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
        if self.is_shooting():
            return
        self._timer_count = 0
        self._shoot_angle = self._current_angle
        self._shoot_force = self._current_force
        self._auto_shoot_timer.start(5)
        self.can_shoot.emit(False)

    first_time = True

    def new_target(self):
        if CannonField.first_time:
            CannonField.first_time = False
            midnight = QTime(0, 0, 0)
            random.seed(midnight.secsTo(QTime.currentTime()))

        self.target = QPoint(200 + random.randint(0, 190 - 1), 10 + random.randint(0, 255 - 1))
        self.update()

    def set_game_over(self):
        if self._game_ended:
            return
        if self.is_shooting():
            self._auto_shoot_timer.stop()
        self._game_ended = True
        self.update()

    def restart_game(self):
        if self.is_shooting():
            self._auto_shoot_timer.stop()
        self._game_ended = False
        self.update()
        self.can_shoot.emit(True)

    @Slot()
    def move_shot(self):
        region = QRegion(self.shot_rect())
        self._timer_count += 1

        shot_r = self.shot_rect()

        if shot_r.intersects(self.target_rect()):
            self._auto_shoot_timer.stop()
            self.hit.emit()
            self.can_shoot.emit(True)
        elif shot_r.x() > self.width() or shot_r.y() > self.height():
            self._auto_shoot_timer.stop()
            self.missed.emit()
            self.can_shoot.emit(True)
        else:
            region = region.united(QRegion(shot_r))

        self.update(region)

    def paintEvent(self, event):
        with QPainter(self) as painter:
            if self._game_ended:
                painter.setPen(Qt.GlobalColor.black)
                painter.setFont(QFont("Courier", 48, QFont.Weight.Bold))
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Game Over")

            self.paint_cannon(painter)
            if self.is_shooting():
                self.paint_shot(painter)
            if not self._game_ended:
                self.paint_target(painter)

    def paint_shot(self, painter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawRect(self.shot_rect())

    def paint_target(self, painter):
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.red)
        painter.drawRect(self.target_rect())

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

    def target_rect(self):
        result = QRect(0, 0, 20, 10)
        result.moveCenter(QPoint(self.target.x(), self.height() - 1 - self.target.y()))
        return result

    def game_over(self):
        return self._game_ended

    def is_shooting(self):
        return self._auto_shoot_timer.isActive()


class GameBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        quit = QPushButton("&Quit")
        quit.setFont(QFont("Times", 18, QFont.Weight.Bold))

        quit.clicked.connect(qApp.quit)  # noqa: F821

        angle = LCDRange("ANGLE")
        angle.set_range(5, 70)

        force = LCDRange("FORCE")
        force.set_range(10, 50)

        self._cannon_field = CannonField()

        angle.value_changed.connect(self._cannon_field.set_angle)
        self._cannon_field.angle_changed.connect(angle.set_value)

        force.value_changed.connect(self._cannon_field.set_force)
        self._cannon_field.force_changed.connect(force.set_value)

        self._cannon_field.hit.connect(self.hit)
        self._cannon_field.missed.connect(self.missed)

        shoot = QPushButton("&Shoot")
        shoot.setFont(QFont("Times", 18, QFont.Weight.Bold))

        shoot.clicked.connect(self.fire)
        self._cannon_field.can_shoot.connect(shoot.setEnabled)

        restart = QPushButton("&New Game")
        restart.setFont(QFont("Times", 18, QFont.Weight.Bold))

        restart.clicked.connect(self.new_game)

        self.hits = QLCDNumber(2)
        self._shots_left = QLCDNumber(2)
        hits_label = QLabel("HITS")
        shots_left_label = QLabel("SHOTS LEFT")

        top_layout = QHBoxLayout()
        top_layout.addWidget(shoot)
        top_layout.addWidget(self.hits)
        top_layout.addWidget(hits_label)
        top_layout.addWidget(self._shots_left)
        top_layout.addWidget(shots_left_label)
        top_layout.addStretch(1)
        top_layout.addWidget(restart)

        left_layout = QVBoxLayout()
        left_layout.addWidget(angle)
        left_layout.addWidget(force)

        grid_layout = QGridLayout(self)
        grid_layout.addWidget(quit, 0, 0)
        grid_layout.addLayout(top_layout, 0, 1)
        grid_layout.addLayout(left_layout, 1, 0)
        grid_layout.addWidget(self._cannon_field, 1, 1, 2, 1)
        grid_layout.setColumnStretch(1, 10)

        angle.set_value(60)
        force.set_value(25)
        angle.setFocus()

        self.new_game()

    @Slot()
    def fire(self):
        if self._cannon_field.game_over() or self._cannon_field.is_shooting():
            return
        self._shots_left.display(self._shots_left.intValue() - 1)
        self._cannon_field.shoot()

    @Slot()
    def hit(self):
        self.hits.display(self.hits.intValue() + 1)
        if self._shots_left.intValue() == 0:
            self._cannon_field.set_game_over()
        else:
            self._cannon_field.new_target()

    @Slot()
    def missed(self):
        if self._shots_left.intValue() == 0:
            self._cannon_field.set_game_over()

    @Slot()
    def new_game(self):
        self._shots_left.display(15)
        self.hits.display(0)
        self._cannon_field.restart_game()
        self._cannon_field.new_target()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = GameBoard()
    board.setGeometry(100, 100, 500, 355)
    board.show()
    sys.exit(app.exec())
