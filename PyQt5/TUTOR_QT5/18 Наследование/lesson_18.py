# coding=utf-8
# **********************************************************
# lesson_18
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
# Объект - это структура данных,
# cодержащая: данные-свойства и функции-методы
#
# Класс - это шаблон для создания объектов этого класса
#

#import sys
#from PyQt5.QtWidgets import *       # imports section

###############################################
# point_main.py
###############################################
# from point import Point
import point as pt  # рекомендуется

#=============================================
# FOR 2D POINT (x,y)
#=============================================
# (..) - вызывается конструктор для начальной инициализации (__init__(...))
p1 = pt.Point(1,33)     # p1 =  1 33
p2 = pt.Point(4,-9)        # p2 =  4 -9

# Values
print('p1 = ', p1.x, p1.y)  # p1 =  1 33
print('p2 = ', p2.x, p2.y)  # p2 =  4 -9

# Equal distance
print('DIST2 = ', p1.distance_to(p2))   # DIST2 =  42.1070065428546
print('DIST1 = ', p2.distance_to(p1))   # DIST1 =  42.1070065428546

# Null distance
print('DIST (p1) = ', p1.distance_to(p1))   # DIST (p1) =  0.0

# Type object
print(type(p1)) # <class 'point.Point'>

# Address object (с переопределением вывода str())
print('str(): ', p1)       # <point.Point object at 0x00000212CAA16510> --> Point(1.00000, 33.00000)

print('-' * 80)

#=============================================
# FOR 3D POINT (x,y,z)
#=============================================
point3D_1 = pt.Point3D(2,4, 9)
point3D_2 = pt.Point3D(5,14, -29)

print(point3D_1.distance_to(point3D_2))     # с методом родителя - distance_to() - 10.44030650891055
print(point3D_1.distance3d_to(point3D_2))   # с новым методом - distance3D_to - 39.408120990476064

print(point3D_1)
print('2D: ', p1.hello())
print('3D:', point3D_1.hello())
