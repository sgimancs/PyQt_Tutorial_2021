##########################################
# point.py
# CLASSES
##########################################
#
# self - ссылка на объект
# x,у - аргументы (свойства)
#

#--------------------------------------------------
# БАЗОВЫЙ КЛАСС
#--------------------------------------------------
class Point:    # camel-case name of class

    # CONSTRUCTOR (начальная инициализация)
    def __init__(self, x, y, units):
        self.x = x
        self.y = y
        self.__units = units    # приватное свойство

    # GETTER for "units" (private-protected)
    def get_units(self):
        return self.__units

    # SETTER for "units" (private-protected)
    def set_units(self, units):
        self.__units = units

    # distance_to() - METHOD для Point3D
    def distance_to(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

    # Override - переопределить внутренний метод str() для класса Point
    def __str__(self):
        str_repr = 'Point({0:.5f}, {1:.5f})'.format(self.x, self.y)
        return str_repr

    # Метод для 2D
    def hello(self):
        return 'Hello! My coords are: {0:.5f}, {1:.5f}. Nice to meet you!'.format(self.x, self.y)


#--------------------------------------------------
# КЛАСС С НАССЛЕДОВАНИЕМ
#--------------------------------------------------
class Point3D(Point):

    # CONSTRUCTOR
    def __init__(self, x, y, z, units):
        Point.__init__(self, x, y, units)  # инициализировать класс родителя (Point)
        self.z = z                         # доп. свойство (z)

    # Override - переопределить внутренний метод str() для класса Point3D
    def __str__(self):
        str_repr = 'Point({0:.5f}, {1:.5f}, {2:.5f})'.format(self.x, self.y, self.z)
        return str_repr

    # distance3D_to() - METHOD для Point3D
    def distance3d_to(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2) ** 0.5

    # Метод переопределён для 3D
    def hello(self):
        return 'Hello! My coords are: {0:.5f}, {1:.5f}, {2:.5f}. Nice to meet you!'\
            .format(self.x, self.y, self.z)
