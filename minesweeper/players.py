class Player:
    def __init__(self):
        pass

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_move(self, game):
        val = None
        while True:
            game.print_display()
            spot = input(f"Choose your move? (0-49)")
            try:
                val = int(spot)
                if val not in game.available_moves():
                    raise ValueError
                break
            except ValueError:
                print("try again")

        return val


class ComputerPlayer(Player):
    pass
