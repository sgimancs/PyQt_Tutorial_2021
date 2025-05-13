# coding=utf-8
# **********************************************************
# lesson_21
# QMessageBox
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
        self.btn = QPushButton('Show Message', self)    # кнопка (QPushButton)
        self.btn.move(35, 50)                           # размер
        self.btn.clicked.connect(self.evt_btn_clicked)         # подключение к обработчику событий

    # Обработчик событий
    def evt_btn_clicked(self):
        # res = QMessageBox.question(self, 'Disk Full', 'Your disk drive is almost full')
        # if res == QMessageBox.Yes:
        #     QMessageBox.information(self, '', "You've clicked 'Yes' button")
        # elif res == QMessageBox.No:
        #     QMessageBox.information(self, '', "You've clicked 'No' button")

        # QMessageBox
        msgDiskFull = QMessageBox()

        msgDiskFull.setText('Your hard drive is almostfull')
        msgDiskFull.setDetailedText('Please free up disk space')            # button - show detail
        msgDiskFull.setIcon(QMessageBox.Information)                        # icon
        msgDiskFull.setWindowTitle('Full Drive')                            # title
        msgDiskFull.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) # buttons
        msgDiskFull.exec_()     # выполнить


#----------------------------
# START
#----------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI
    sys.exit(app.exec_())           # execute the application
