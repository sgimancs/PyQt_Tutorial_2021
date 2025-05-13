# coding=utf-8
# **********************************************************
# lesson_22
# QInputDialog
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


#--------------------------
# CLASS
#--------------------------
class DlgMain(QDialog):

    # Конструктор
    def __init__(self):
        super().__init__()
        self.resize(200, 200)
        self.btn = QPushButton('Show Input', self)  # QPushButton
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)

    # Обработчик событий
    def evt_btn_clicked(self):
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

        # QInputDialog
        s_color, b_ok = QInputDialog.getItem(self, 'Title',
                                             'Enter your favorite color: ', colors)

        if b_ok:
            QMessageBox.information(self, 'Color', 'Your favorite color is ' + s_color)
        else:
            QMessageBox.critical(self, 'Canceled', 'User have clicked "Cancel"')

#----------------------------
# START
#----------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application

