# coding=utf-8
# **********************************************************
# lesson_33
# QLineEdit
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
# QLineEdit(parent),QLineEdit(str, parent):
#
# Методы:
#   tex(), setTex(str), clear()
#   setPlaceHolderText(str)
#   setReadOnly(bool)
#   setEchoMode(QLineEdit.Password)
#   setAlignment(Qt.Alignment)
#   setMaxLength(int)
#
# Сигналы:
#   textChanged(str)
#   textEdited(str)
#   editingFinished()
#-----------------------------------------------------------

import sys
from PyQt5.QtWidgets import *  # imports section
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#==============================================
# CLASS
#==============================================
class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 200)

        # QLineEdit
        self.ledTitle = QLineEdit(self.windowTitle(), self)             # извлечь title
        self.ledTitle.setPlaceholderText('Enter a new window title')    # placeholder
        self.ledTitle.setEchoMode(QLineEdit.Password)                   # echo password
        self.ledTitle.setAlignment(Qt.AlignCenter)                      # align center
        self.ledTitle.move(50, 50)                                      # position
        self.btnUpdate = QPushButton('Update Title', self)              # update
        self.btnUpdate.move(150, 100)                                   # position
        self.btnUpdate.clicked.connect(self.evt_btn_update_clicked)     # event update
        self.ledTitle.textChanged.connect(self.evt_led_title_text_changed)  # event change text


    def evt_led_title_text_changed(self, title):
        self.setWindowTitle(title)


    def evt_btn_update_clicked(self):
        res = QMessageBox.question(self, 'Title Editing', 'Do you want to change the title to "'
                                   + self.ledTitle.text() + '"?')
        if res == QMessageBox.Yes:
            self.setWindowTitle(self.ledTitle.text())


#---------------------------------
# START
#---------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
