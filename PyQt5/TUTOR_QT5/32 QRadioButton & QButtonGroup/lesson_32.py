# coding=utf-8
# **********************************************************
# lesson_32
# QRadioButton & QButtonGroup
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
# QRadioButton:
#-----------------------------------------------------------
# Родителем является QAbstractButton:
# QRadioButton(str, parent)
#
# По умолчанию Radio Buttons автоматически исключительные:
#   только одна Radio Button в одном и том же родителе может быть выбрана
#   выбор одной Radio Button автоматически снимает выбор с других
#
# Для двух групп Radio Button:
#   два отдельных родительских виджета
#-----------------------------------------------------------
# QButtonGroup:
#-----------------------------------------------------------
#   addButton(QAbstractButton, id)
#   checkButton()
#   checkId()
#
# В QButtonGroup чекбоксы могут быть исключительные
# и QRadioButton могут быть не исключительными
#   setExclusive(bool) - не рекомендуется
#-----------------------------------------------------------

import sys
from PyQt5.QtWidgets import *  # imports section
from PyQt5.QtGui import *
from PyQt5.QtCore import *


#==============================================
# CLASS
#==============================================
class DlgMain(QDialog):

    # КОНСТРУКТОР
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 200)
        self.lbl = QLabel('Label Text', self)           # QLabel
        self.lbl.setStyleSheet('color:red; font-size: 10px')
        self.lbl.move(50, 20)
        self.lbl.resize(100, 30)

        # Color Button Group
        self.btgColor = QButtonGroup()

        # QRadioButton ("red")
        self.rbtRed = QRadioButton('Red', self)
        self.rbtRed.move(50, 70)                          # position
        self.rbtRed.setChecked(True)
        self.rbtRed.clicked.connect(self.evt_rbt_clicked) # подключить к clicked
        self.btgColor.addButton(self.rbtRed)              # добавить в группу

        # QRadioButton ("green")
        self.rbtGreen = QRadioButton('Green', self)
        self.rbtGreen.move(50, 100)                         # position
        self.rbtGreen.clicked.connect(self.evt_rbt_clicked) # подключить к clicked
        self.btgColor.addButton(self.rbtGreen)              # добавить в группу

        # QRadioButton ("blue")
        self.rbtBlue = QRadioButton('Blue', self)
        self.rbtBlue.move(50, 130)                          # position
        self.rbtBlue.clicked.connect(self.evt_rbt_clicked)  # подключить к clicked
        self.btgColor.addButton(self.rbtBlue)               # добавить в группу

        # Text Size Button Group
        self.btgTextSize = QButtonGroup()

        # checked 1
        self.rbtSmall = QRadioButton('Small Text', self)
        self.rbtSmall.move(150, 70)                         # position
        self.rbtSmall.setChecked(True)
        self.rbtSmall.clicked.connect(self.evt_rbt_clicked) # подключить к clicked
        self.btgTextSize.addButton(self.rbtSmall, 10)    # добавить в группу

        # checked 2
        self.rbtMedium = QRadioButton('Medium Text', self)
        self.rbtMedium.move(150, 100)                        # position
        self.rbtMedium.clicked.connect(self.evt_rbt_clicked) # подключить к clicked
        self.btgTextSize.addButton(self.rbtMedium, 15)    # добавить в группу

        # checked 3
        self.rbtLarge = QRadioButton('Large Text', self)
        self.rbtLarge.move(150, 130)                        # position
        self.rbtLarge.clicked.connect(self.evt_rbt_clicked) # подключить к clicked
        self.btgTextSize.addButton(self.rbtLarge, 20)    # добавить в группу


    # ОБРАБОТЧИК СОБЫТИЙ
    def evt_rbt_clicked(self):
        checked_btg_color_rbt = self.btgColor.checkedButton()
        checked_btg_text_size_rbt_id = self.btgTextSize.checkedId()
        str_style_sheet = 'color:' + checked_btg_color_rbt.text() + '; font-size:' \
                          + str(checked_btg_text_size_rbt_id) + 'px'
        print(str_style_sheet)
        self.lbl.setStyleSheet(str_style_sheet)


#------------------------------
# START
#------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
