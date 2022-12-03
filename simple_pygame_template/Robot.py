# from main import square, rows, cols


class Robot:
    def __init__(self, x_pos, y_pos, square, rows, cols):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.square, self.rows, self.cols = square, rows, cols
        self.visible_squares = self.update_visible()

    def move(self, dx, dy):
        self.x_pos += dx
        self.y_pos += dy

        if self.x_pos < 0:
            self.x_pos += self.square[0]

        elif self.x_pos > (self.cols - 1) * self.square[0]:
            self.x_pos -= self.square[0]

        if self.y_pos < 0:
            self.y_pos += self.square[1]

        elif self.y_pos > (self.rows - 1) * self.square[1]:
            self.y_pos -= self.square[1]

        self.visible_squares = self.update_visible()

    def is_valid(self, new_pos):
        # checks if the position proposed is one that is within boundaries and is not and obstacle
        if new_pos[0] > self.cols * self.square[0] or new_pos[0] < 0 or new_pos[1] > self.rows * self.square[1] or new_pos[1] < 0:
            return False

        return True

    def update_visible(self):
        vis = []
        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            neighbour = self.x_pos + self.square[0] * direction[0], self.y_pos + self.square[1] * direction[1]
            if self.is_valid(neighbour):
                vis.append(neighbour)

        return vis
