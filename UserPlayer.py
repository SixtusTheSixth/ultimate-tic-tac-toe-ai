# ultimate tic-tac-toe player that gets moves from a user

import re
from BasePlayer import BasePlayer
from ultimate_utils import valid_move

class UserPlayer(BasePlayer):
	def __init__(self):
		super().__init__()
	
	def get_type(self):
		# return string for what kind of player we are: "random", "strategy", "minimax", "rl", "user"
		return "user"
	
	def get_move(self, board, mini, prev_move, cur_player):
		# board: 9x9 array representation of board, each position is ' ', 'x', or 'o'
		# mini: 1x9 list representation of overall board, each position is 0 for unfinished, 1 for x, 2 for o, 3 for draw
		# prev_move: tuple (row, col) of previous move
		# cur_player: 1 for x, 2 for o
		
		cur_move = -1
		while cur_move == -1:
			# get the move from input
			move_str = re.findall(r'.*?([1-9]).*?([1-9]).*', input(f"Player {cur_player}'s move: ").strip().lower())
			if not move_str:
				print("That's not a valid move, please try again.")
				continue
			a, b = tuple(int(x) for x in move_str[0])
			a, b = a-1, b-1
			cur_move = ((a // 3) * 3 + (b // 3), (a % 3)  * 3 + (b % 3)) # convert to indices in board
			
			# check that the move is valid, if not say so and ask again
			if not valid_move(cur_move, board, mini, prev_move):
				print("That's not a valid move, please try again.")
				cur_move = -1
		
		return cur_move