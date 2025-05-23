# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the qml/tutorials/extending-qml/chapter1-basics example from Qt v5.x"""

import os
from pathlib import Path
import sys

from PySide6.QtCore import Property, Signal, QUrl
from PySide6.QtGui import QGuiApplication, QPen, QPainter, QColor
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickPaintedItem, QQuickView

# Для использования в декораторе @QmlElement
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "Charts"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class PieChart (QQuickPaintedItem):

    nameChanged = Signal()

    def __init__(self, parent=None):
        QQuickPaintedItem.__init__(self, parent)
        self._name = u''
        self._color = QColor()

    def paint(self, painter):
        pen = QPen(self.color, 2)
        painter.setPen(pen)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing, True)
        painter.drawPie(self.boundingRect().adjusted(1, 1, -1, -1), 90 * 16, 290 * 16)

    @Property(QColor, final=True)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @Property(str, notify=nameChanged, final=True)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

#---------------------------------------
# START
#---------------------------------------
if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    view = QQuickView()
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    qml_file = os.fspath(Path(__file__).resolve().parent / 'app.qml')
    view.setSource(QUrl.fromLocalFile(qml_file))

    if view.status() == QQuickView.Status.Error:
        sys.exit(-1)

    view.show()
    res = app.exec()

    # Удаление представления до того, как оно выйдет из области действия, необходимо для того,
    # чтобы все дочерние экземпляры QML были уничтожены в правильном порядке.
    del view
    sys.exit(res)
