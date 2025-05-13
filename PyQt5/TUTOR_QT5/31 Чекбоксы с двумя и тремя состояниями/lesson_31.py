# coding=utf-8
# **********************************************************
# lesson_31
# Qt Check Boxes
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
# QCheckBox
#-----------------------------------------------------------
# Родителем является QAbstractButton:
#   Методы:
#       isChecked()
#       setChecked(bool)
#   Сигналы:
#       clicked(bool)
#       toggle(bool)
#
# QCheckBox(str, parent):
#   Методы:
#       isTristate(), setTristate(bool) - для 3-х состояний (get)
#       checkState(), setCheckState(Qt.CheckState) - для 3-х состояний (set)
#   Сигналы:
#       stateChanged(int)
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

        # Checkbox для 2-х состояний
        self.chk_enabled = QCheckBox('Enabled', self)
        self.chk_enabled.move(50, 50)
        self.chk_enabled.setChecked(True)
        self.chk_enabled.toggled.connect(self.evt_chk_enabled_toggled)

        # Checkbox для 3-х состояний
        self.chk_3_states = QCheckBox('3 state checkbox', self)
        self.chk_3_states.move(50, 70)
        self.chk_3_states.setTristate(True)
        self.chk_3_states.stateChanged.connect(self.evt_chk_3_states_changed)

        # метка
        self.lbl = QLabel('Label Text', self)
        self.lbl.move(60, 100)
        self.lbl.resize(320, 176)
        font = QFont('Times New Roman', 24, 75, True)
        self.lbl.setFont(font)

    # События для 2-х состояний
    def evt_chk_enabled_toggled(self, is_checked):
        if is_checked:
            self.lbl.setEnabled(True)
        else:
            self.lbl.setDisabled(True)

    # События для 3-х состояний
    def evt_chk_3_states_changed(self, state):
        if state == 0:
            QMessageBox.information(self, 'State', 'Unchecked')
        elif state == 1:
            QMessageBox.information(self, 'State', 'Partially checked')
        else:
            QMessageBox.information(self, 'State', 'Checked')


#------------------------------
# START
#------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application

