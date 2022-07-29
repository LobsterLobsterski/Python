##########################################################
# Code made by Tomasz Potoczko while learning how to use
# python.
# This file contains the Game class which contains
# all the methods needed for the game to function
# properly.
##########################################################

class Game:

    def __init__(self):
        self.gameSpace = [' ' for _ in range(9)]
        self.display = [str(x) for x in range(9)]
        self.winner = None

    def print_display(self):
        for row in (self.display[i*3:(i+1)*3] for i in range(3)):
            print("|" + "|".join(row) + "|")

    def print_game_space(self):
        for row in (self.gameSpace[i*3:(i+1)*3] for i in range(3)):
            print("|" + "|".join(row) + "|")

    def empty_spots(self):
        return ' ' in self.gameSpace

    def num_empty_spots(self):
        return self.gameSpace.count(' ')

    def check_for_available_spot(self, spot):
        return self.gameSpace[spot] == ' '

    def make_move(self, spot, letter):
        if self.check_for_available_spot(spot):
            self.gameSpace[spot] = letter
            if self.won(letter, spot):
                self.winner = letter

            return True
        return False

    def available_moves(self):
        return [i for i, spot in enumerate(self.gameSpace) if spot == ' ']

    def won(self, letter, spot):
        # check if three of the same symbol are in a line
        # !!CHECK WHICH ROW/COLUMN TO CHECK BY THE SPOT GIVEN AS ARG


        # if in a horizontal line
        for row in (self.gameSpace[i*3:(i+1)*3] for i in range(3)):
            # print(row)
            if all([spot == letter for spot in row]):
                # print("3 in horizontal line")
                return True

        # if in vertical line
        for col_idx in range(3):
            col = [self.gameSpace[col_idx+i*3] for i in range(3)]
            if all([spot == letter for spot in col]):
                # print("3 in a vertical line")
                return True

        # if in a diagnal, if idx%2 is true
        diagonal1 = [self.gameSpace[i] for i in [0, 4, 8]]
        if all([spot == letter for spot in diagonal1]):
            # print("3 in a left-to-right diagnal")
            return True
        diagonal2 = [self.gameSpace[i] for i in [2, 4, 6]]
        if all([spot == letter for spot in diagonal2]):
            # print("3 in a right-to-left diagonal")
            return True

        return False

