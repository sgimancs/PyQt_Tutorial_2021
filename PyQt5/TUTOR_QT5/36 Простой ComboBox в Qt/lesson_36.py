# coding=utf-8
# **********************************************************
# lesson_36
# Qt ComboBox
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

#
# QComboBox(parent) - конструктор
#
#   Методы (idx - индекс элемента):
#       addItem(QIcon,txt,obj), insertItem(idx,QIcon,txt,obj), insertSeparator(idx)
#       addItems(list), insertItems(idx,list)
#       removeItem(idx), clear()
#       count(), currentIndex(), currentData(), currentText()
#       itemText(idx), itemData(idx), itemIcon(idx)
#       setItemText(idx,txt), setItemData(idx,obj), setItemIcon(idx,QIcon)
#       setMaxCount(int), setMaxVisibleItems(int), setPlaceHolder(str)
#       setCurrent(idx), setCurrentText(str)
#
#   Сигналы:
#       currentIndexChanged(idx), currentTextChanged(txt) - для программ
#       activated(idx), textActivated(txt) - для пользователя
#       highlighted(idx), textHighlighted(txt) - выделение
#

import sys
from PyQt5.QtWidgets import *  # imports section
from PyQt5.QtGui import *
from PyQt5.QtCore import *


#============================================================
# CLASS
#============================================================
class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 200)

        # QComboBox 1 (STATES) - (txt, idx)
        self.cmbState = QComboBox(self)
        self.cmbState.move(50, 50)
        # self.cmbState.addItems(['AL', 'AR', 'MA', 'MO', 'MI'])
        # кортежи с названиями штатов
        self.cmbState.addItem('Alabama', 'AL')
        self.cmbState.addItem('Alaska', 'AR')
        self.cmbState.addItem('Minnesota', 'MA')
        self.cmbState.addItem('Missouri', 'MO')
        self.cmbState.addItem('Michigan', 'MI')
        self.cmbState.currentIndexChanged.connect(self.evt_cmb_state_changed)
        self.cmbState.highlighted.connect(self.evt_cmb_state_highlighted)

        # QLabel
        self.lblAbbr = QLabel('State Abbreviation: AL', self)
        self.lblAbbr.resize(150, 30)
        self.lblAbbr.move(170, 50)

    #---------------------------------------------
    # ОБРАБОТЧИКИ СОБЫТИЙ (СЛОТЫ)
    #---------------------------------------------
    def evt_cmb_state_changed(self, idx):
        QMessageBox.information(self, 'ComboBox', 'You have selected {}'.format(self.cmbState.itemData(idx)))

    def evt_cmb_state_highlighted(self, idx):
        self.lblAbbr.setText('State Abbreviation: {}'.format(self.cmbState.itemData(idx)))


#----------------------------------
# START
#----------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
