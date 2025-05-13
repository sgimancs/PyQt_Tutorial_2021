# coding=utf-8
# **********************************************************
# lesson_34
# Spinbox
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

#----------------------------------------------------------
# Spinbox:
#
# Методы
#   setReadOnly(bool), isReadOnly()
#   setAlignment(Qt.Alignment)
#   setWrapping(bool)
#   text(), clear(), selectAll()
#   stetUp(), stepDown()
#
# Сигналы
#   editingFinished()
#----------------------------------------------------------
# QSpinBox, QDoubleSpinBox:
#
# Методы:
#   setMinimum(int), setMaximum(int), setRange(min, max)
#   setSingleStep(int)
#   setPrefix(str), setSuffix(str)
#   setValue(int), value()
#
# Сигналы:
#   textChanged(str)
#   valueChanged(int)
#
# QDoubleSpinBox идентичен, но для работы со значениями double
#   setDecimals(int) - кол-во цифр после запятой
#----------------------------------------------------------

import sys
from PyQt5.QtWidgets import *  # imports section
from PyQt5.QtGui import *
from PyQt5.QtCore import *


#==================================
# CLASS
#==================================
class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 200)

        # QSpinBox
        self.spbInt = QSpinBox(self)
        self.spbInt.move(50, 50)
        self.spbInt.setWrapping(True)           # циклично
        self.spbInt.setRange(0, 1000) # диапазон
        self.spbInt.setSingleStep(100)          # шаг
        self.spbInt.setValue(100)               # начальное значение
        self.spbInt.valueChanged.connect(self.evt_spb_int_value_changed)        # подключить к обработчику событий
        self.spbInt.editingFinished.connect(self.evt_spb_int_editing_finished)  # подключить к обработчику событий завершения

        # QDoubleSpinBox
        self.spbDbl = QDoubleSpinBox(self)
        self.spbDbl.move(50, 80)                        # позиция
        self.spbDbl.setDecimals(2)                      # округление до 2-х знаков
        self.spbDbl.setSingleStep(0.01)                 # шаг
        self.spbDbl.setPrefix('Height ')                # префикс (до)
        self.spbDbl.setSuffix(' meters')                # суффикс (после)
        self.spbDbl.setRange(0.40, 3.00)        # диапазон
        self.spbDbl.valueChanged.connect(self.evt_spb_dbl_value_changed) # изменить значение

    # Вывод на консоль
    def evt_spb_dbl_value_changed(self, val):
        print(self.spbDbl.text())
        print(self.spbDbl.value())

    # Контроль значений кратных 100
    def evt_spb_int_value_changed(self, val):
        print(val, val % 100)
        if(val % 100):
            self.spbInt.setStyleSheet('color: red')
        else:
            self.spbInt.setStyleSheet('color: black')

    # Предупреждение об некорректном вводе
    def evt_spb_int_editing_finished(self):
        if (self.spbInt.value() % 100):
            QMessageBox.critical(self, 'Invalid Number', 'Invalid value was entered '
                                                         '\n\nMust be divisible by 100')
            self.spbInt.setFocus()  # перевести фокус на ошибочный INT


#------------------------------------
# START
#------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
