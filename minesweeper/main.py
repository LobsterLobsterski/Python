##########################################################
# Code made by Tomasz Potoczko while learning how to use
# python.
# This code is a python implementation of Minesweeper
# and I feel very proud of it as it is my first OOP
# program which i wrote by myself
##########################################################

from game import Game
from players import HumanPlayer, ComputerPlayer


def play(game, player):
    while game.empty_spots():
        move = player.get_move(game)

        if not game.make_move(move):
            break

        print("")


g = Game()
p = HumanPlayer()
play(g, p)

