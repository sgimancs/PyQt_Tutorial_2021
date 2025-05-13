# coding=utf-8
# **********************************************************
# lesson_30
# QPushButton
# ----------------------------------------------------------
# Master of Code (2021)
# 2021_Разработка GUI приложений на Python 3 и PyQt5
# ----------------------------------------------------------
# Python 3.13.3
# jetBrain PyCharm 2024.2.3
# Designer 5.14 (Qt)
# ----------------------------------------------------------
# pip install pyqt5
# pip install pyqt5-tools
# pyuic5 -x app.ui -o app.py
# ----------------------------------------------------------
# PyQt — это свободное программное обеспечение,
# разработанное британской фирмой Riverbank Computing.
# https://riverbankcomputing.com/
# **********************************************************
# Writing sgiman, 2025
#

#-----------------------------------------------------------
# QPushButton:
# Родителем является QAbstractButton
# Абстрактные классы не используются для создания объектов.
# Абстрактные классы используются для общих свойств и методов.
#
# Методы:
#   setIcon(QIcon)
#   setText(str)
#   setAutoRepeat(bool), setAutoRepeatDelay(msec), setAutoRepeatInterval(msec)
#
# Сигналы:
#   clicked
#
# QPushButton(str, parent)
#   setFlat(bool), setDefault(bool)
#-----------------------------------------------------------

import sys
from PyQt5.QtWidgets import *  # imports section
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#========================================================
# CLASS
#========================================================
class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.btn = QPushButton('Disable Label', self)               # QPushButton
        self.btn.setIcon(QIcon(QPixmap('pictures/banana.png')))
        self.btn.setFlat(False)
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)              # btn.clicked.connect

        # QLabel
        self.lbl = QLabel('Label Text', self)                       # lbl - object
        self.lbl.move(60, 100)
        self.lbl.resize(320, 176)
        font = QFont('Times New Roman', 24, 75, True)
        self.lbl.setFont(font)

    def evt_btn_clicked(self):
        if self.lbl.isEnabled():
            self.lbl.setDisabled(True)
            self.btn.setText('Enable Label')
        else:
            self.lbl.setEnabled(True)
            self.btn.setText('Disable Label')


#------------------------------
# START
#------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
