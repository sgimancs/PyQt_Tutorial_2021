# coding=utf-8
# **********************************************************
# lesson_25
# QFontDialog
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

import sys
from PyQt5.QtWidgets import *  # imports section
from PyQt5.QtGui import *

#========================================================
# CLASS
#========================================================
class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)
        self.btn = QPushButton('Choose Font', self)     # QPushButton
        self.btn.move(35, 50)
        font = QFont('Arial', 14, 75, True)
        self.btn.setFont(font)
        self.btn.clicked.connect(self.evt_btn_clicked)

    def evt_btn_clicked(self):
        # QFontDialog
        font, b_ok = QFontDialog.getFont()  # распаковка кортежа в переменные
        print(font, b_ok)

        if b_ok:
            print(font.family())
            print(font.italic())
            print(font.bold())
            print(font.weight())
            print(font.pointSize())
            print('-' * 80)
            self.btn.setFont(font)


#------------------------------
# START
#------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
