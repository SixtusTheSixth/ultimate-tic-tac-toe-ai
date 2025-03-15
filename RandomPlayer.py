# ultimate tic-tac-toe player that plays random valid mvoes

import random
from BasePlayer import BasePlayer
from ultimate_utils import valid_move

class RandomPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
    
    def get_type(self):
        # return string for what kind of player we are: "random", "strategy", "minimax", "rl", "user"
        return "random"
    
    def random_move(self, board, mini, prev_move, ai_player):
        # get a random valid move (in row-col format)
        # ai_player = 1 if x and 2 if o
        # move until we get a valid move
        valid = False
        move = (-1, -1)
        while not valid:
            move = (random.randint(0, 9), random.randint(0, 9))
            valid = valid_move(move, board, mini, prev_move)
        return move
    
    def get_move(self, board, mini, prev_move, cur_player):
		# board: 9x9 array representation of board, each position is ' ', 'x', or 'o'
		# mini: 1x9 list representation of overall board, each position is 0 for unfinished, 1 for x, 2 for o, 3 for draw
		# prev_move: tuple (row, col) of previous move
		# cur_player: 1 for x, 2 for o

        return self.random_move(board, mini, prev_move, cur_player)