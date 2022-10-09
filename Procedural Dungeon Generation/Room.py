"""
File holding different room classes to creating various room shapes
by various I mean two :)
"""
import math


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{type(self).__name__}'

    def __hash__(self):
        return hash(self.x, self.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def get_trdl(self):
        top = min(self.points, key=lambda val: val[1])[1]
        right = max(self.points, key=lambda val: val[0])[0]
        down = max(self.points, key=lambda val: val[1])[1]
        left = min(self.points, key=lambda val: val[0])[0]

        return top, right, down, left

    def get_points(self, ):
        ...

    def centre(self, square):
        ...


class Rect(Room):
    def __init__(self, x, y, width, height, size_mod):
        super(Rect, self).__init__(x, y)
        self.x2 = x + height*size_mod
        self.y2 = y + width*size_mod
        self.points = self.get_points()
        self.top, self.right, self.down, self.left = super(Rect, self).get_trdl()

    def __str__(self):
        return super(Rect, self).__str__() + f"(x= {self.x}, y= {self.y}, x2= {self.x2}, y2= {self.y2})"

    def __repr__(self):
        return super(Rect, self).__str__() + f"(x= {self.x}, y= {self.y}, x2= {self.x2}, y2= {self.y2})"

    def get_points(self):
        list_of_points = set()
        for row_idx in range(self.y, self.y2):
            for col_idx in range(self.x, self.x2):
                val = (row_idx, col_idx)
                list_of_points.add(val)

        return list(list_of_points)

    def centre(self, square):
        return ((self.x+self.x2)//2)*square[0], ((self.y+self.y2)//2)*square[1]


class Circle(Room):
    def __init__(self, start, radius, size_mod):
        super(Circle, self).__init__(start[0], start[1])
        self.radius = radius*size_mod
        self.points = self.get_points()
        self.top, self.right, self.down, self.left = super(Circle, self).get_trdl()

    def __str__(self):
        return super(Circle, self).__str__() + f'(start: {(self.x, self.y)}, radius: {self.radius})'

    def __repr__(self):
        return super(Circle, self).__str__() + f'(start: {(self.x, self.y)}, radius: {self.radius})'

    def get_points(self):
        list_of_points = set()
        for ray in range(180):
            angle = math.radians(ray*2)
            for pos in range(0, int((self.radius+1)*10), 1):
                pos /= 10
                x = int(math.cos(angle)*pos + self.x)
                y = int(math.sin(angle)*pos + self.y)
                val = (y, x)
                list_of_points.add(val)

        return list(list_of_points)

    def centre(self, square):
        return self.x*square[0], self.y*square[1]


