from game import Game
from players import HumanPlayer, ComputerPlayer


def play(game, player1, player2):

    letter = "x"
    while game.empty_spots():

        # getting the move of the player depending on who's turn it is
        if letter == "x":
            spot = player1.get_move(game)
        else:
            spot = player2.get_move(game)

        if game.make_move(spot, letter):
            game.print_game_space()
            print("")

        # checking if the variable changed to a value e.g. is someone won
        if game.winner:
            print(f"{letter} wins!")

            return letter

        # swapping the player
        letter = 'o' if letter == 'x' else 'x'
        # game.print_game_space()

    print("It's a tie")


player1 = ComputerPlayer("x")
player2 = HumanPlayer("o")
g = Game()

play(g, player1, player2)
