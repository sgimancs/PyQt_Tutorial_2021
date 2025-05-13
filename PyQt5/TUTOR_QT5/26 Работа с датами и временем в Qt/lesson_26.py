# coding=utf-8
# **********************************************************
# lesson_26
# Qt Date & Time
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
from PyQt5.QtCore import *

#========================================================
# CLASS
#========================================================
class DlgMain(QDialog):

    def __init__(self):
        super().__init__()
        self.resize(200, 200)
        self.btn = QPushButton('Dates', self)   # QPushButton
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)


    def evt_btn_clicked(self):

        # QDate.currentDate
        print('-' * 80)
        dt = QDate.currentDate()
        print(dt.toString())
        print(dt.toJulianDay())
        print(dt.dayOfWeek())
        print(dt.dayOfYear())
        print(dt.addDays(21).toString())
        print('-' * 80)

        # QTime
        tm1 = QTime(13, 20)
        tm2 = QTime(15, 20)
        tm = tm2.addSecs(60)
        print(tm1.toString())
        print(tm.toString())
        print(tm1.msec())
        print(tm1.secsTo(tm2))
        print('-' * 80)

        # QDateTime.currentDateTime
        dtm = QDateTime.currentDateTime()
        print(dtm.toString())
        print('-' * 80)


#------------------------------
# START
#------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
