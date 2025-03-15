class BasePlayer():
    def __init__(self):
        pass

    def initialize(self):
        pass

    def get_type(self):
        # return string for what kind of player we are: "random", "strategy", "minimax", "rl", "user"
        return "base"

    def get_move(self, board, mini, prev_move, cur_player):
        # board: 9x9 array representation of board, each position is ' ', 'x', or 'o'
        # mini: 1x9 list representation of overall board, each position is 0 for unfinished, 1 for x, 2 for o, 3 for draw
        # prev_move: tuple (row, col) of previous move
        # cur_player: 1 for x, 2 for o
        pass