# coding=utf-8
# **********************************************************
# lesson_13
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
#------------------------------------------------------
# ООП ПОДХОД (ПАРАДИГМА)
#------------------------------------------------------
import sys
from PyQt5.QtWidgets import *       # imports section

# Н А С Л Е Д О В А Н И Е (CLASS)
class DlgMain(QDialog):                     # наследуется от QDialog()

    # К О Н С Т Р У К Т О Р
    def __init__(self):                     # init object properties
        super().__init__()                  # init base class
        self.setWindowTitle('Second GUI')   # add widgets, set properties
        self.resize(300,200)

        self.ledText = QLineEdit('Default Text', self)
        self.ledText.move(85,50)

        self.btnUpdate = QPushButton('Update Window Title', self)
        self.btnUpdate.move(95,90)
        self.btnUpdate.clicked.connect(self.evt_btn_update_clicked)  # подключить обработчик событий

    # ОБРАБОТЧИК СОБЫТИЙ
    def evt_btn_update_clicked(self):
        self.setWindowTitle(self.ledText.text())    # текст заголовка окна



# В Ы П О Л Н Е Н И Е
if __name__ == '__main__':          # если модуль не импортирован в другую программу
    app = QApplication(sys.argv)    # create application
    dlgMain = DlgMain()             # create main GUI window
    dlgMain.show()                  # show GUI (унаследовано)
    sys.exit(app.exec_())           # execute the application
