import random
import math


class Puzzle:
    def __init__(self, dim_size, num_of_nums):
        self.board_dim = dim_size
        self.num_of_nums = num_of_nums
        self.puzzle = self.make_puzzle()

    def print_puzzle(self):
        for row in self.puzzle:
            print(row)

    def print_all_nonets(self):
        # just a debugging tool
        print("all nonets")
        for i in range(0, self.board_dim-2, 3):
            for j in range(0, self.board_dim-2, 3):
                nonet = [*self.puzzle[i][j:j+3], *self.puzzle[i+1][j:j+3], *self.puzzle[i+2][j:j+3]]
                print(nonet)
                print("")

    @staticmethod
    def get_col(puzzle, col):
        return [row[col] for row in puzzle]

    @staticmethod
    def get_nonet(puzzle, row_idx, col_idx, ret_idx=False):
        # returns a nonet (3x3) in which the passed
        # coordinates are located in
        row_idx = math.floor(row_idx / 3) * 3
        col_idx = math.floor(col_idx / 3) * 3
        if ret_idx:
            return row_idx + col_idx//3

        return [*puzzle[row_idx][col_idx:col_idx + 3], *puzzle[row_idx + 1][col_idx:col_idx + 3], *puzzle[row_idx + 2][col_idx:col_idx + 3]]

    @staticmethod
    def get_row(puzzle, row_idx):
        return puzzle[row_idx]

    def make_puzzle(self):
        # this method creates a random valid sudoku puzzle board
        puzzle = [[0 for _ in range(self.board_dim)] for _ in range(self.board_dim)]
        placed = 0

        while placed < self.num_of_nums:
            rand_row, rand_col = (random.randint(0, self.board_dim-1) for _ in range(2))
            # print(f"row: {rand_row} and col: {rand_col}")
            if puzzle[rand_row][rand_col] == 0:
                # if the random spot is available get random integer
                val = random.randint(1, self.board_dim)
                if val in puzzle[rand_row] or val in [row[rand_col] for row in puzzle] or val in self.get_nonet(puzzle, rand_row, rand_col):
                    # if a value equal to the new random one is already in the row
                    # or column or nonet (3x3) go back
                    continue

                # if we are here it means that the random spot is available and valid
                # so we place a number there
                # print(f"VAL: {val}")
                # print(f"ROW: {puzzle[rand_row]}")
                # print(f"COL: {[row[rand_col] for row in puzzle]}")
                # print(f"NONET: {self.get_nonet(puzzle, rand_row, rand_col)}")
                puzzle[rand_row][rand_col] = val
                placed += 1

        # print("PUZZLE:")
        # for row in puzzle:
        #     print(row)
        return puzzle

    def check_if_valid(self):
        pass


