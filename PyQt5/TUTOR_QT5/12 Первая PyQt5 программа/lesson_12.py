# coding=utf-8
# **********************************************************
# lesson_12
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
# ПОЦЕДУРНЫЙ ПОДХОД (ПАРАДИГМА)
#------------------------------------------------------
import sys
from PyQt5.QtWidgets import *       # imports section

app = QApplication(sys.argv)        # create application (главное окно)

# W I N D O W
# dlgMain = QWidget()             # create main GUI window (standard windows variant)
dlgMain = QDialog()               # create main GUI window (рекомендуется - QT variant)
# dlgMain = QMainWindow()         # для меню и панелей в сложных app

dlgMain.setWindowTitle('First GUI') # свойства - title (setter)

dlgMain.show()                      # show the GUI

#app.exec_()                        # execute the app (main loop)
sys.exit(app.exec_())               # выполнение с возвратом кода ошибки
