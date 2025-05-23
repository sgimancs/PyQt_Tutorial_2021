# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the widgets/painting/basicdrawing example from Qt v5.x, originating from PyQt"""

from PySide6.QtCore import QPoint, QRect, QSize, Qt, qVersion
from PySide6.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
                           QPainterStateGuard, QPainterPath, QPalette, QPen,
                           QPixmap, QPolygon, QRadialGradient)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QLabel, QSpinBox, QWidget)

import basicdrawing_rc  # noqa: F401


class RenderArea(QWidget):
    points = QPolygon([
        QPoint(10, 80),
        QPoint(20, 10),
        QPoint(80, 30),
        QPoint(90, 70)
    ])

    (Line, Points, Polyline, Polygon, Rect, RoundedRect, Ellipse,
     Arc, Chord, Pie, Path, Text, Pixmap) = range(13)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()
        self.pixmap = QPixmap()

        self.shape = RenderArea.Polygon
        self.antialiased = False
        self.transformed = False
        self.pixmap.load(':/images/qt-logo.png')

        self.setBackgroundRole(QPalette.ColorRole.Base)
        self.setAutoFillBackground(True)

    def minimumSizeHint(self):
        return QSize(100, 100)

    def sizeHint(self):
        return QSize(400, 200)

    def set_shape(self, shape):
        self.shape = shape
        self.update()

    def set_pen(self, pen):
        self.pen = pen
        self.update()

    def set_brush(self, brush):
        self.brush = brush
        self.update()

    def set_antialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()

    def set_transformed(self, transformed):
        self.transformed = transformed
        self.update()

    def paintEvent(self, event):
        rect = QRect(10, 20, 80, 60)

        path = QPainterPath()
        path.moveTo(20, 80)
        path.lineTo(20, 30)
        path.cubicTo(80, 0, 50, 50, 80, 80)

        start_angle = 30 * 16
        arc_length = 120 * 16

        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            if self.antialiased:
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            for x in range(0, self.width(), 100):
                for y in range(0, self.height(), 100):
                    with QPainterStateGuard(painter):
                        painter.translate(x, y)
                        if self.transformed:
                            painter.translate(50, 50)
                            painter.rotate(60.0)
                            painter.scale(0.6, 0.9)
                            painter.translate(-50, -50)

                        if self.shape == RenderArea.Line:
                            painter.drawLine(rect.bottomLeft(), rect.topRight())
                        elif self.shape == RenderArea.Points:
                            painter.drawPoints(RenderArea.points)
                        elif self.shape == RenderArea.Polyline:
                            painter.drawPolyline(RenderArea.points)
                        elif self.shape == RenderArea.Polygon:
                            painter.drawPolygon(RenderArea.points)
                        elif self.shape == RenderArea.Rect:
                            painter.drawRect(rect)
                        elif self.shape == RenderArea.RoundedRect:
                            painter.drawRoundedRect(rect, 25, 25, Qt.SizeMode.RelativeSize)
                        elif self.shape == RenderArea.Ellipse:
                            painter.drawEllipse(rect)
                        elif self.shape == RenderArea.Arc:
                            painter.drawArc(rect, start_angle, arc_length)
                        elif self.shape == RenderArea.Chord:
                            painter.drawChord(rect, start_angle, arc_length)
                        elif self.shape == RenderArea.Pie:
                            painter.drawPie(rect, start_angle, arc_length)
                        elif self.shape == RenderArea.Path:
                            painter.drawPath(path)
                        elif self.shape == RenderArea.Text:
                            qv = qVersion()
                            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter,
                                             f"PySide 6\nQt {qv}")
                        elif self.shape == RenderArea.Pixmap:
                            painter.drawPixmap(10, 10, self.pixmap)

            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))


id_role = Qt.ItemDataRole.UserRole


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self._render_area = RenderArea()

        self._shape_combo_box = QComboBox()
        self._shape_combo_box.addItem("Polygon", RenderArea.Polygon)
        self._shape_combo_box.addItem("Rectangle", RenderArea.Rect)
        self._shape_combo_box.addItem("Rounded Rectangle", RenderArea.RoundedRect)
        self._shape_combo_box.addItem("Ellipse", RenderArea.Ellipse)
        self._shape_combo_box.addItem("Pie", RenderArea.Pie)
        self._shape_combo_box.addItem("Chord", RenderArea.Chord)
        self._shape_combo_box.addItem("Path", RenderArea.Path)
        self._shape_combo_box.addItem("Line", RenderArea.Line)
        self._shape_combo_box.addItem("Polyline", RenderArea.Polyline)
        self._shape_combo_box.addItem("Arc", RenderArea.Arc)
        self._shape_combo_box.addItem("Points", RenderArea.Points)
        self._shape_combo_box.addItem("Text", RenderArea.Text)
        self._shape_combo_box.addItem("Pixmap", RenderArea.Pixmap)

        shape_label = QLabel("&Shape:")
        shape_label.setBuddy(self._shape_combo_box)

        self._pen_width_spin_box = QSpinBox()
        self._pen_width_spin_box.setRange(0, 20)
        self._pen_width_spin_box.setSpecialValueText("0 (cosmetic pen)")

        pen_width_label = QLabel("Pen &Width:")
        pen_width_label.setBuddy(self._pen_width_spin_box)

        self._pen_style_combo_box = QComboBox()
        self._pen_style_combo_box.addItem("Solid", Qt.PenStyle.SolidLine)
        self._pen_style_combo_box.addItem("Dash", Qt.PenStyle.DashLine)
        self._pen_style_combo_box.addItem("Dot", Qt.PenStyle.DotLine)
        self._pen_style_combo_box.addItem("Dash Dot", Qt.PenStyle.DashDotLine)
        self._pen_style_combo_box.addItem("Dash Dot Dot", Qt.PenStyle.DashDotDotLine)
        self._pen_style_combo_box.addItem("None", Qt.PenStyle.NoPen)

        pen_style_label = QLabel("&Pen Style:")
        pen_style_label.setBuddy(self._pen_style_combo_box)

        self._pen_cap_combo_box = QComboBox()
        self._pen_cap_combo_box.addItem("Flat", Qt.PenCapStyle.FlatCap)
        self._pen_cap_combo_box.addItem("Square", Qt.PenCapStyle.SquareCap)
        self._pen_cap_combo_box.addItem("Round", Qt.PenCapStyle.RoundCap)

        pen_cap_label = QLabel("Pen &Cap:")
        pen_cap_label.setBuddy(self._pen_cap_combo_box)

        self._pen_join_combo_box = QComboBox()
        self._pen_join_combo_box.addItem("Miter", Qt.PenJoinStyle.MiterJoin)
        self._pen_join_combo_box.addItem("Bevel", Qt.PenJoinStyle.BevelJoin)
        self._pen_join_combo_box.addItem("Round", Qt.PenJoinStyle.RoundJoin)

        pen_join_label = QLabel("Pen &Join:")
        pen_join_label.setBuddy(self._pen_join_combo_box)

        self._brush_style_combo_box = QComboBox()
        self._brush_style_combo_box.addItem("Linear Gradient", Qt.BrushStyle.LinearGradientPattern)
        self._brush_style_combo_box.addItem("Radial Gradient", Qt.BrushStyle.RadialGradientPattern)
        self._brush_style_combo_box.addItem("Conical Gradient",
                                            Qt.BrushStyle.ConicalGradientPattern)
        self._brush_style_combo_box.addItem("Texture", Qt.BrushStyle.TexturePattern)
        self._brush_style_combo_box.addItem("Solid", Qt.BrushStyle.SolidPattern)
        self._brush_style_combo_box.addItem("Horizontal", Qt.BrushStyle.HorPattern)
        self._brush_style_combo_box.addItem("Vertical", Qt.BrushStyle.VerPattern)
        self._brush_style_combo_box.addItem("Cross", Qt.BrushStyle.CrossPattern)
        self._brush_style_combo_box.addItem("Backward Diagonal", Qt.BrushStyle.BDiagPattern)
        self._brush_style_combo_box.addItem("Forward Diagonal", Qt.BrushStyle.FDiagPattern)
        self._brush_style_combo_box.addItem("Diagonal Cross", Qt.BrushStyle.DiagCrossPattern)
        self._brush_style_combo_box.addItem("Dense 1", Qt.BrushStyle.Dense1Pattern)
        self._brush_style_combo_box.addItem("Dense 2", Qt.BrushStyle.Dense2Pattern)
        self._brush_style_combo_box.addItem("Dense 3", Qt.BrushStyle.Dense3Pattern)
        self._brush_style_combo_box.addItem("Dense 4", Qt.BrushStyle.Dense4Pattern)
        self._brush_style_combo_box.addItem("Dense 5", Qt.BrushStyle.Dense5Pattern)
        self._brush_style_combo_box.addItem("Dense 6", Qt.BrushStyle.Dense6Pattern)
        self._brush_style_combo_box.addItem("Dense 7", Qt.BrushStyle.Dense7Pattern)
        self._brush_style_combo_box.addItem("None", Qt.BrushStyle.NoBrush)

        brush_style_label = QLabel("&Brush Style:")
        brush_style_label.setBuddy(self._brush_style_combo_box)

        other_options_label = QLabel("Other Options:")
        self._antialiasing_check_box = QCheckBox("&Antialiasing")
        self._transformations_check_box = QCheckBox("&Transformations")

        self._shape_combo_box.activated.connect(self.shape_changed)
        self._pen_width_spin_box.valueChanged.connect(self.pen_changed)
        self._pen_style_combo_box.activated.connect(self.pen_changed)
        self._pen_cap_combo_box.activated.connect(self.pen_changed)
        self._pen_join_combo_box.activated.connect(self.pen_changed)
        self._brush_style_combo_box.activated.connect(self.brush_changed)
        self._antialiasing_check_box.toggled.connect(self._render_area.set_antialiased)
        self._transformations_check_box.toggled.connect(self._render_area.set_transformed)

        main_layout = QGridLayout()
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(3, 1)
        main_layout.addWidget(self._render_area, 0, 0, 1, 4)
        main_layout.setRowMinimumHeight(1, 6)
        main_layout.addWidget(shape_label, 2, 1, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self._shape_combo_box, 2, 2)
        main_layout.addWidget(pen_width_label, 3, 1, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self._pen_width_spin_box, 3, 2)
        main_layout.addWidget(pen_style_label, 4, 1, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self._pen_style_combo_box, 4, 2)
        main_layout.addWidget(pen_cap_label, 5, 1, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self._pen_cap_combo_box, 5, 2)
        main_layout.addWidget(pen_join_label, 6, 1, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self._pen_join_combo_box, 6, 2)
        main_layout.addWidget(brush_style_label, 7, 1, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self._brush_style_combo_box, 7, 2)
        main_layout.setRowMinimumHeight(8, 6)
        main_layout.addWidget(other_options_label, 9, 1, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self._antialiasing_check_box, 9, 2)
        main_layout.addWidget(self._transformations_check_box, 10, 2)
        self.setLayout(main_layout)

        self.shape_changed()
        self.pen_changed()
        self.brush_changed()
        self._antialiasing_check_box.setChecked(True)

        self.setWindowTitle("Basic Drawing")

    def shape_changed(self):
        shape = self._shape_combo_box.itemData(self._shape_combo_box.currentIndex(), id_role)
        self._render_area.set_shape(shape)

    def pen_changed(self):
        width = self._pen_width_spin_box.value()
        style = Qt.PenStyle(self._pen_style_combo_box.itemData(
            self._pen_style_combo_box.currentIndex(), id_role))
        cap = Qt.PenCapStyle(self._pen_cap_combo_box.itemData(
            self._pen_cap_combo_box.currentIndex(), id_role))
        join = Qt.PenJoinStyle(self._pen_join_combo_box.itemData(
            self._pen_join_combo_box.currentIndex(), id_role))

        self._render_area.set_pen(QPen(Qt.GlobalColor.blue, width, style, cap, join))

    def brush_changed(self):
        style = Qt.BrushStyle(self._brush_style_combo_box.itemData(
            self._brush_style_combo_box.currentIndex(), id_role))

        if style == Qt.BrushStyle.LinearGradientPattern:
            linear_gradient = QLinearGradient(0, 0, 100, 100)
            linear_gradient.setColorAt(0.0, Qt.GlobalColor.white)
            linear_gradient.setColorAt(0.2, Qt.GlobalColor.green)
            linear_gradient.setColorAt(1.0, Qt.GlobalColor.black)
            self._render_area.set_brush(QBrush(linear_gradient))
        elif style == Qt.BrushStyle.RadialGradientPattern:
            radial_gradient = QRadialGradient(50, 50, 50, 70, 70)
            radial_gradient.setColorAt(0.0, Qt.GlobalColor.white)
            radial_gradient.setColorAt(0.2, Qt.GlobalColor.green)
            radial_gradient.setColorAt(1.0, Qt.GlobalColor.black)
            self._render_area.set_brush(QBrush(radial_gradient))
        elif style == Qt.BrushStyle.ConicalGradientPattern:
            conical_gradient = QConicalGradient(50, 50, 150)
            conical_gradient.setColorAt(0.0, Qt.GlobalColor.white)
            conical_gradient.setColorAt(0.2, Qt.GlobalColor.green)
            conical_gradient.setColorAt(1.0, Qt.GlobalColor.black)
            self._render_area.set_brush(QBrush(conical_gradient))
        elif style == Qt.BrushStyle.TexturePattern:
            self._render_area.set_brush(QBrush(QPixmap(':/images/brick.png')))
        else:
            self._render_area.set_brush(QBrush(Qt.GlobalColor.green, style))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
