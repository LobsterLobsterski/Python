class Shape:
    def __init__(self, type):
        self.type = type  # dictates the shape
        self.shape = []
        self.colour = ()
        # setting starting coords
        self.x = 4*30
        self.y = 0
        # just like with rect object
        self.top = 0
        self.right = 0
        self.down = 0
        self.left = 0
        # used for rotation
        self.grid_coords = []
        self.rotation = 0

    def set_trdl(self):
        # sets up the top, right, left and down attributes (same as in rect object of pygame)
        self.top = min([coord[1] for coord in self.shape])
        self.right = max([coord[0] for coord in self.shape])
        self.down = max([coord[1] for coord in self.shape])
        self.left = min([coord[0] for coord in self.shape])

    def get_grid_coords(self):
        # setting up the points occupied by the shape from the point of view of the board

        point_x, point_y = self.left // 30, self.top // 30
        if self.type == 'I':
            self.grid_coords = [
                [[point_x, point_y], [point_x, point_y + 1], [point_x, point_y + 2], [point_x, point_y + 3]],
                [[point_x, point_y], [point_x + 1, point_y], [point_x + 2, point_y], [point_x + 3, point_y]]
            ]
        elif self.type == 'J':
            self.grid_coords = [
                [[point_x, point_y], [point_x + 1, point_y], [point_x + 2, point_y], [point_x + 2, point_y + 1]],
                [[point_x + 1, point_y], [point_x + 1, point_y + 1], [point_x + 1, point_y + 2],
                 [point_x, point_y + 2]],
                [[point_x, point_y], [point_x, point_y + 1], [point_x + 1, point_y + 1], [point_x + 2, point_y + 1]],
                [[point_x, point_y], [point_x + 1, point_y], [point_x, point_y + 1], [point_x, point_y + 2]]
            ]
            # as a not the 3rd one if offset to the right by one
        elif self.type == 'L':
            self.grid_coords = [
                [[point_x + 2, point_y], [point_x + 2, point_y + 1], [point_x + 1, point_y + 1],
                 [point_x, point_y + 1]],
                [[point_x, point_y], [point_x, point_y + 1], [point_x, point_y + 2], [point_x + 1, point_y + 2]],
                [[point_x, point_y + 1], [point_x, point_y], [point_x + 1, point_y], [point_x + 2, point_y]],
                [[point_x, point_y], [point_x + 1, point_y], [point_x + 1, point_y + 1], [point_x + 1, point_y + 2]]
            ]
        elif self.type == 'O':
            self.grid_coords = [
                [[point_x, point_y], [point_x + 1, point_y], [point_x + 1, point_y + 1], [point_x, point_y + 1]]
            ]
        elif self.type == 'S':
            self.grid_coords = [
                [[point_x, point_y], [point_x, point_y + 1], [point_x + 1, point_y + 1], [point_x + 1, point_y + 2]],
                [[point_x + 1, point_y], [point_x + 2, point_y], [point_x + 1, point_y + 1], [point_x, point_y + 1]]
            ]
        elif self.type == 'T':
            self.grid_coords = [
                [[point_x + 1, point_y], [point_x + 1, point_y + 1], [point_x, point_y + 1],
                 [point_x + 2, point_y + 1]],
                [[point_x, point_y], [point_x, point_y + 1], [point_x, point_y + 2], [point_x + 1, point_y + 1]],
                [[point_x, point_y], [point_x + 1, point_y], [point_x + 2, point_y], [point_x + 1, point_y + 1]],
                [[point_x + 1, point_y], [point_x + 1, point_y + 1], [point_x, point_y + 1], [point_x + 1, point_y + 2]]
            ]
        elif self.type == 'Z':
            self.grid_coords = [
                [[point_x + 1, point_y], [point_x + 1, point_y + 1], [point_x, point_y + 1], [point_x, point_y + 2]],
                [[point_x, point_y], [point_x + 1, point_y], [point_x + 1, point_y + 1], [point_x + 2, point_y + 1]]
            ]

    def make_shape(self, dx, dy):
        # this function creates a polygon object depending on the type and coordinates
        self.x += dx
        self.y += dy

        # if not initialised yet set the values
        if not self.shape:
            list_of_points = []  # the list fo points needed to draw the polygon
            colour = 0, 0, 0  # the colour values for a shape

            # self.type = 'I'  # for testing

            if self.type == 'I':
                # the 1 by 4
                colour = 240, 248, 255
                list_of_points = [[self.x, self.y], [self.x+30, self.y], [self.x+30, self.y+120], [self.x, self.y+120]]
            elif self.type == 'J':
                # the other-way-around L
                colour = 3, 37, 126
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+60, self.y), (self.x+90, self.y),
                                  (self.x+90, self.y+30), (self.x+90, self.y+60), (self.x+60, self.y+60),
                                  (self.x+60, self.y+30), (self.x+30, self.y+30), (self.x, self.y+30)]
            elif self.type == 'L':
                # the L
                colour = 255, 165, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+30, self.y+60),
                                  (self.x, self.y+60), (self.x-30, self.y+60), (self.x-60, self.y+60),
                                  (self.x-60, self.y+30),(self.x-30, self.y+30), (self.x, self.y+30)]
            elif self.type == 'O':
                # the square
                colour = 255, 255, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+60, self.y), (self.x+60, self.y+30),
                                  (self.x+60, self.y+60), (self.x+30, self.y+60), (self.x, self.y+60),
                                  (self.x, self.y+30)]
            elif self.type == 'S':
                # the square with the left side 1 block lower
                colour = 0, 255, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+60, self.y+30),
                                  (self.x+60, self.y+60), (self.x+60, self.y+90), (self.x+30, self.y+90),
                                  (self.x+30, self.y+60), (self.x, self.y+60), (self.x, self.y+30)]
            elif self.type == 'T':
                # the T
                colour = 221, 160, 221
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+60, self.y+30),
                                  (self.x+60, self.y+60), (self.x+30, self.y+60), (self.x, self.y+60),
                                  (self.x-30, self.y+60), (self.x-30, self.y+30), (self.x, self.y+30)]
            elif self.type == 'Z':
                # the square with the right side 1 block lower
                colour = 255, 0, 0
                list_of_points = [(self.x, self.y), (self.x+30, self.y), (self.x+30, self.y+30), (self.x+30, self.y+60),
                                  (self.x, self.y+60), (self.x, self.y+90), (self.x-30, self.y+90),
                                  (self.x-30, self.y+60), (self.x-30, self.y+30), (self.x, self.y+30)]

            self.shape = list_of_points
            self.colour = colour

        # otherwise we can't set out shape but operate and mutate it
        else:
            new = []
            for point in self.shape:
                temp = point[0]+dx, point[1]+dy
                new.append(temp)

            self.shape = new

        # at the end we set helpful attributes
        self.get_grid_coords()
        self.set_trdl()

    def rotate(self, grid_array):
        self.rotation += 1
        origin = self.shape[0]
        rotated = []
        for point in self.shape:
            # setting up the point around which we will rotate
            temp = point[0] - origin[0], point[1] - origin[1]
            # simplified rotation by 90 degrees
            temp = -temp[1], temp[0]
            # same as temp = int(round(temp[0]*math.cos(angle) - temp[1]*math.sin(angle), -1)),\
            #     int(round(temp[0]*math.sin(angle) + temp[1]*math.cos(angle), -1))
            # with angle of 90 degrees it does the exact same thing
            rotated.append([temp[0]+origin[0], temp[1]+origin[1]])

        prev = self.shape  # needed to possibly revert the change
        self.shape = rotated
        self.set_trdl()
        self.get_grid_coords()
        self.x, self.y = self.shape[0]

        # makes sure we don't rotate outside the screen
        if self.left < 0:
            for idx, point in enumerate(self.shape):
                self.shape[idx][0] += -self.left
        if self.right > 300:
            for idx, point in enumerate(self.shape):
                self.shape[idx][0] = self.shape[idx][0] + (300-self.right)
        if self.down > 600:
            for idx, point in enumerate(self.shape):
                self.shape[idx][1] = self.shape[idx][1] + (600-self.down)
        if self.top < 0:
            for idx, point in enumerate(self.shape):
                self.shape[idx][1] += -self.top

        self.set_trdl()
        self.get_grid_coords()
        self.x, self.y = self.shape[0]

        # makes sure we don't rotate into another shape
        tetrino_grid_coords = self.grid_coords[self.rotation % len(self.grid_coords)]
        for coord in tetrino_grid_coords:
            if grid_array[coord[1]][coord[0]] == (100, 100, 100):
                continue

            self.shape = prev
            self.set_trdl()
            self.get_grid_coords()
            self.x, self.y = self.shape[0]
            return
