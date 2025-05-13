##########################################
# point.py
# CLASSES
##########################################
#
# self - ссылка на объект
# x,у - аргументы (свойства)
#
class Point:    # camel-case name of class
    # CONSTRUCTOR (начальная инициализация)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # distance_to() - METHOD
    def distance_to(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

    # Override - переопределить внутренний метод str()
    def __str__(self):
        str_repr = 'Point({0:.5f}, {1:.5f})'.format(self.x, self.y)
        return str_repr
