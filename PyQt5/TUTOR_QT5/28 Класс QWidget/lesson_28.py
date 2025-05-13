# coding=utf-8
# **********************************************************
# lesson_28
# QWidget
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
# QWidget
#----------------------------------------------------------
# Текущее состояние:
#   isEnabled(), isWindow(), isVisible(), isModal() итд
#
# Позиционирование:
#   move(x,y), pos(), resize(w,h), size(), setGeometry(x,y,w,h)
#
# Стилизация:
#   setFont(QFont), setStyleSheet(string) - CSS
#
# Tips (подсказки):
#   serStatus(strings), setToolTip(string) - status bar (panel)
#
# Видимость:
#   show(), hide(), setEnabled(boolean)
#
#