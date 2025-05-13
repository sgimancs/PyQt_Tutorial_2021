# coding=utf-8
# **********************************************************
# lesson_29
# QLabel
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
# QLabel(str, parent):
#   setText(str)
#   setNum(int | double)
#   setPixmap(QPixmap)
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
        self.btn = QPushButton('Change Label', self)    # QPushButton
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)

        # QLabel
        self.lbl = QLabel('Label Text', self)
        self.lbl.move(60, 100)
        self.lbl.resize(320, 176)
        font = QFont('Arial', 24, 75, True)
        self.lbl.setFont(font)


    def evt_btn_clicked(self):
        rich_text = """
        <h1>Fruits</h1>
        <ul>
            <li>Apple</li>
            <li>Orange</li>
        </ul>
        """
        self.lbl.setText(rich_text)
        pxm = QPixmap('pictures/orange.jpg').scaled(320, 176)
        self.lbl.setPixmap(pxm)


#------------------------------
# START
#------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
