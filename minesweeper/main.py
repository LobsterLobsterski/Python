from game import Game
from players import HumanPlayer, ComputerPlayer


def play(game, player):
    while game.empty_spots():
        move = player.get_move(game)

        if not game.make_move(move):
            break

        print("")

# game is functional now
# add a function which will plot the mine field
# onto the game space AND find the fucking None
# print


g = Game()
p = HumanPlayer()
play(g, p)

