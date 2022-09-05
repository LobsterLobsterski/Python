import math


class Shape:
    def __init__(self, type):
        self.type = type  # dictates the shape
        self.shape = []
        self.colour = ()
        self.height = 0
        # setting starting coords
        self.x = 4*30
        self.y = 0
        #  just like with rect object
        self.top = 0
        self.right = 0
        self.down = 0
        self.left = 0

    def init_trdl(self):
        # initialises the top, right, down and left values based on the shape
        pass

    def make_shape(self, dx, dy):
        self.x += dx
        self.y += dy
        # this function creates a polygon object depending on the type

        # if not initialised yet set the values
        if not self.shape:
            list_of_points = []  # the list fo points needed to draw the polygon
            colour = 0, 0, 0  # the colour values for a shape

            self.type = 'I'  # for testing

            if self.type == 'I':
                # the 1 by 4
                colour = 240, 248, 255
                list_of_points = [[self.x, self.y], [self.x+30, self.y], [self.x+30, self.y+120], [self.x, self.y+120]]
                self.height = 4*30
            elif self.type == 'J':
                # the other-way-around L
                colour = 3, 37, 126
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+60, self.y), (self.x+90, self.y), (self.x+90, self.y+30), (self.x+90, self.y+60), (self.x+60, self.y+60), (self.x+60, self.y+30), (self.x+30, self.y+30), (self.x, self.y+30)]
                self.height = 2*30
            elif self.type == 'L':
                # the L
                colour = 255, 165, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+30, self.y+60), (self.x, self.y+60), (self.x-30, self.y+60), (self.x-60, self.y+60), (self.x-60, self.y+30),(self.x-30, self.y+30), (self.x, self.y+30)]
                self.height = 2*30
            elif self.type == 'O':
                # the square
                colour = 255, 255, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+60, self.y), (self.x+60, self.y+30), (self.x+60, self.y+60), (self.x+30, self.y+60), (self.x, self.y+60), (self.x, self.y+30)]
                self.height = 2*30
            elif self.type == 'S':
                # the square with the left side 1 block lower
                colour = 0, 255, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+60, self.y+30), (self.x+60, self.y+60), (self.x+60, self.y+90), (self.x+30, self.y+90), (self.x+30, self.y+60), (self.x, self.y+60), (self.x, self.y+30)]
                self.height = 3*30
            elif self.type == 'T':
                # the T
                colour = 221, 160, 221
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+60, self.y+30), (self.x+60, self.y+60), (self.x+30, self.y+60), (self.x, self.y+60), (self.x-30, self.y+60), (self.x-30, self.y+30), (self.x, self.y+30)]
            elif self.type == 'Z':
                # the square with the right side 1 block lower
                colour = 255, 0, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+30, self.y+60), (self.x, self.y+60), (self.x, self.y+90), (self.x-30, self.y+90), (self.x-30, self.y+60), (self.x-30, self.y+30), (self.x, self.y+30)]
                self.height = 3*30

            self.shape = list_of_points
            self.init_trdl()
            self.colour = colour

        # otherwise we can't set out shape but operate and mutate it
        else:
            new = []
            for point in self.shape:
                temp = point[0]+dx, point[1]+dy
                new.append(temp)

            self.shape = new

    def rotate(self, angle):
        # fix the elongation effect
        angle = math.radians(angle)
        for _ in range(2):
            origin = self.shape[0]
            print(origin)
            rotated = []
            for point in self.shape:
                temp = point[0] - origin[0], point[1] - origin[1]
                # print(f"temp0: {temp[0]} temp1: {temp[1]}")
                temp = int(round(temp[0]*math.cos(angle) - temp[1]*math.sin(angle), -1)),\
                    int(round(temp[0]*math.sin(angle) + temp[1]*math.cos(angle), -1))

                # print(temp)
                rotated.append((point[0]+temp[0], point[1]+temp[1]))

            self.shape = rotated


if __name__ == '__main__':
    obj = Shape('I')
    obj.make_shape(0, 0)
    print(f"before rotation cls.shape: \n{obj.shape}")
    obj.rotate(90)
    print(f"after rotation cls.shape: \n{obj.shape}")



