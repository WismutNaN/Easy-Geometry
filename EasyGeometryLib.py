import math

class Point:
    ''' Точка имеет координаты в трехмерном пространстве '''
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotated(self,center,azimuth):
        ''' Поворот точки в плане вокруг другой точки на заданный азимут'''
        x_a, y_a, z_a = self.x, self.y, self.z
        x_c, y_c = center.x, center.y
        length_с_а = math.sqrt((x_c-x_a)**2+(y_c-y_a)**2)
        print(length_с_а)
        x_b = length_с_а*math.cos(math.radians(azimuth))
        y_b = length_с_а*math.sin(math.radians(azimuth))

        return Point(x_b, y_b,z_a)


    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Point(self.x-other.x,self.y-other.y, self.z-other.z)

    def __str__(self):
        return '{:.3f}\t{:.3f}\t{:.3f}'.format(self.x, self.y, self.z)

class Vector:
    '''
    Вектор имеет координаты в трехмерном пространстве
    Умеет задаваться двумя способами, как две точки в пространстве и координатами вектора
    Может высчитать свою длину, угол и азимут, а так же менять свое направление на противоположенное
    Реализовано умножение векторов
    '''
    def __init__(self, *args):
        if len(args) == 2:
            point1 = args[0]
            point2 = args[1]
            self.x = point2.x-point1.x
            self.y = point2.y-point1.y
            self.z = point2.z-point1.z
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        else:
            print('проблема с входными данными')

    def multiply_minus(self):
        '''
        Изменение направления вектора на противоположенное
        '''
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def edge2face(self):
        '''
        Поворот вектора на 90 градусов
        '''

        azimuth = self.azimuth()

        x = self.x
        y = self.y
        z = self.z

        self.z = - math.sqrt(x**2+y**2)
        self.x = z*math.sin(math.radians(azimuth))
        self.y = z*math.cos(math.radians(azimuth))

    def length(self):
        '''
        Длина вектора
        '''
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def azimuth(self):
        '''
        Направление падения вектора в поскости X0Y
        '''
        if self.z < 0:
            self.multiply_minus()
        try:
            azimuth_sub = math.degrees(math.atan(self.x / self.y))
        except: # pylint: disable=bare-except
            azimuth_sub = 0
        if self.x > 0 and self.y > 0:
            azimuth = azimuth_sub
        elif self.x < 0 < self.y:
            azimuth = 360 + azimuth_sub
        else:
            azimuth = 180 + azimuth_sub
        return azimuth

    def dip(self):
        '''
        Угол падения вектора
        '''
        return math.degrees(math.atan(math.sqrt(self.y**2+self.x**2)/self.z))

    def degrees_with(self,other):
        return math.degrees(math.acos((self.x*other.x+self.y* other.y+self.z*other.z)/(math.sqrt(self.x**2+self.y**2+self.z**2)*math.sqrt(other.x**2+other.y**2+other.z**2))))

    def __mul__(self, other):
        return Vector(self.y * other.z - other.y * self.z,
                         -(self.x * other.z - other.x * self.z),
                         self.x * other.y - other.x * self.y)

    def __str__(self):
        return '{:.3f}\t{:.3f}\t{:.3f}'.format(self.x, self.y, self.z)

class Face:
    '''
    Плоскость задается тремя точками
    Представляется одим вектором
    Кроме свойств вектра имеет площадь
    '''
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.center = self.calculate_center()
        self.ab = self.ab_vector()
        self.azimuth = self.ab.azimuth()
        self.dip = self.ab.dip()
        self.area = self.calculate_area()
        self.rotated_azimuth = 0
        self.degree = self.calculate_degree()

    def calculate_center(self):
        x = (self.point1.x+self.point2.x+self.point3.x)/3
        y = (self.point1.y+self.point2.y+self.point3.y)/3
        z = (self.point1.z+self.point2.z+self.point3.z)/3
        return Point(x, y, z)

    def ab_vector(self):
        a = Vector(self.point2, self.point1)
        b = Vector(self.point3, self.point1)
        return a*b

    def calculate_degree(self):
        a = Vector(self.point2, self.point1)
        b = Vector(self.point2, self.point3)
        return a.degrees_with(b)


    def calculate_area(self):
        area = math.sqrt(self.ab.x * self.ab.x + self.ab.y *
                         self.ab.y + self.ab.z * self.ab.z)/2
        return area

    def __str__(self):
        return '{}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.4f}\t{:.1f}'.format(self.center,
                                                                   self.azimuth,
                                                                   self.dip,
                                                                   self.rotated_azimuth,
                                                                   self.area,
                                                                   self.degree)

class Edge:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.center = self.calculate_center()
        self.a = Vector(point1, point2)
        self.length = self.a.length()
        self.azimuth = self.a.azimuth()
        self.dip = self.a.dip()
        self.a.edge2face()
        self.edge_azimuth = self.a.azimuth()
        self.edge_dip = self.a.dip()
        self.rotated_azimuth = 0

    def calculate_center(self):
        x = (self.point1.x+self.point2.x)/2
        y = (self.point1.y+self.point2.y)/2
        z = (self.point1.z+self.point2.z)/2
        return Point(x, y, z)

    def __str__(self):
        return '{}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.4f}'.format(self.center,
                                                                           self.azimuth,
                                                                           self.dip,
                                                                           self.edge_azimuth,
                                                                           self.edge_dip,
                                                                           self.rotated_azimuth,
                                                                           self.length)
