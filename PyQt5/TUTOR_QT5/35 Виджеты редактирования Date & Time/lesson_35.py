# coding=utf-8
# **********************************************************
# lesson_35
# Edit Date & Time
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
# QDateTimeEdit:
# Родителем является QAbstractSpinBox
# QDateTimeEdit(QTime, parent), QTimeEdit(QDate, parent)
# QDateTimeEdit(QDateTime, parent), QDateTimeEdit(parent)
#
#   Методы:
#       setCalendarPopup(bool), setCalendarWidget(QCalendarWidget)
#       date(), time(), dateTime()
#       setDate(), setTime(), setDateTime()
#       setMinimumDate(QDate), setMaximum(QDate), setDateRange(QDate)
#       setDisplay(str)
#
#   Сигналы:
#       dateChanged(QDate), dateTimeChanged(QDateTime), timeChanged(QTime)
#
# QDateEdit(), QTimeEdit():
#-----------------------------------------------------------

import sys
from PyQt5.QtWidgets import *  # imports section
from PyQt5.QtGui import *
from PyQt5.QtCore import *


#===========================================================
# CLASS
#===========================================================
class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 200)

        # QDateTimeEdit
        self.dteDate = QDateTimeEdit(QDate().currentDate(), self)
        self.dteDate.move(50, 50)
        self.dteDate.setCalendarPopup(True)

        self.dteTime = QDateTimeEdit(QTime.currentTime(), self)
        self.dteTime.move(50, 80)

        self.dteDateTime = QDateTimeEdit(QDateTime().currentDateTime(), self)
        self.dteDateTime.move(50, 110)


#-------------------------------------
# START
#-------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
