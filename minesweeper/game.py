import random


class Game:
    def __init__(self):
        self.gameSpace = ['-' for _ in range(50)]
        self.display = [str(x) for x in range(50)]
        self.mineField = ['-' for _ in range(50)]

    def print_display(self):
        for row in (self.display[i*10:(i+1)*10] for i in range(5)):
            print("|" + "|".join(row) + "|")

    def print_game_space(self):
        for row in (self.gameSpace[i*10:(i+1)*10] for i in range(5)):
            print("|" + "|".join(row) + "|")

    def print_mine_field(self):
        for row in (self.mineField[i*10:(i+1)*10] for i in range(5)):
            print("|" + "|".join(row) + "|")

    def empty_spots(self):
        return '-' in self.gameSpace

    def num_empty_spots(self):
        return self.gameSpace.count('-')

    def check_for_available_spot(self, spot):
        return self.gameSpace[spot] == '-'

    @staticmethod
    def outside(spot):
        # checks if a spot is outside the board
        return True if spot < 0 or spot > 49 else False

    def adjacent_spots(self, spot):
        # lets take spot = 23
        # we need to return:
        # 12(-11), 13(-10), 14(-9), 22(-1), 24(+1), 32(+9), 33(+10), 34(+11)
        adjacent = []
        for i in [-11, -10, -9, -1, 1, 9, 10, 11]:
            if not self.outside(spot+i):
                adjacent.append(spot+i)
        return adjacent

    def num_of_adjacent_mines(self, spot):
        # returns a number up to 8 indicating the number
        # of adjacent mines
        num = 0
        adjacent = self.adjacent_spots(spot)
        for i in adjacent:
            if self.mineField[i] == 'x':
                num += 1
        return str(num)

    def make_move(self, spot):

        if self.mineField[spot] == 'x':
            print("You've hit a mine")
            return False
        else:
            self.gameSpace[spot] = self.num_of_adjacent_mines(spot)

        # sets up the mines after the first move
        if 'x' not in self.mineField:
            self.fill_with_mines(10)
            self.gameSpace[spot] = self.num_of_adjacent_mines(spot)

        self.print_game_space()

        return True

    def available_moves(self):
        return [i for i, spot in enumerate(self.gameSpace) if spot == '-']

    def available_mine_spots(self):
        return [i for i, spot in enumerate(self.mineField) if spot == '-']

    def fill_with_mines(self, num):
        spot = random.randint(0, 49)
        for i in range(num):
            while spot not in self.available_mine_spots():
                spot = random.randint(0, 49)
            self.mineField[spot] = 'x'
