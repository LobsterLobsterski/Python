import math
import random


class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        val = None
        while True:
            game.print_display()
            spot = input(f"Where does {self.letter} go? (0-9)")

            try:
                val = int(spot)
                if val not in game.available_moves():
                    raise ValueError
                break
            except ValueError:
                print("try again")

        return val


class ComputerPlayer(Player):
    # if go first, pick a corner, then another and you win
    # if second go for a tie
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            spot = random.choice(game.available_moves())
        else:
            # minimax algorythm for decision making
            spot = self.minimax(game, self.letter)['position']

        return spot

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'o' if player == 'x' else 'x'

        # first we want to check if the previous move is a winner
        if state.winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_spots() + 1) if other_player == max_player else -1 * (state.num_empty_spots() + 1)}
        elif not state.num_empty_spots():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        for possible_move in state.available_moves():
            # step 1 make a move, try that spot
            state.make_move(possible_move, player)
            # step 2 recurse minimax to simulate the game after that move
            sim_score = self.minimax(state, other_player)  # simulate a game after making that move

            # step 3 undo the move and its consequences
            state.gameSpace[possible_move] = ' '
            state.winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            # step 4 update the dict when score from that move beats the best move we
            # have so far then we need to update it
            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best






