# Game and UI driver for ultimate tic-tac-toe

# imports for Board class:
from ultimate_utils import PLAYERS, disp, disp_mini, valid_move, check_won

# imports for game driver in main():
from UserPlayer import UserPlayer
from RandomPlayer import RandomPlayer
from MinimaxPlayer import MinimaxPlayer
from StrategyPlayer import StrategyPlayer

class Board():
	def __init__(self, player1, player2, displaying=False, user_turn=0):
		self.board = [[' '] * 9 for i in range(9)] # in each position: ' ', 'x', 'o'
		self.mini = [0] * 9 # in each position: 0 for unfinished, 1 for x, 2 for o, 3 for draw
		self.game_over = 0 # 0 for unfinished, 1 for x, 2 for o, 3 for draw
		self.turn = 1 # 1 for x, 2 for o
		self.prev_move = (-1, -1) # overall (row, col) format

		self.players = [player1, player2]
		
		# if we have exactly one user playing: 1 if they're x, 2 if they're o
		self.user_turn = user_turn

		self.displaying = displaying
	
	def reset(self):
		# reset internal variables for a new game
		self.board = [[' '] * 9 for i in range(9)]
		self.mini = [0] * 9
		self.game_over = 0
		self.turn = 1
		self.prev_move = (-1, -1)
	
	def update_mini(self, mini, board):
		# update overall board (`mini`) given new board state
		# no need to return anything, just modifying mini in place
		for bigsq, mini_val in enumerate(mini):
			if mini_val != 0: continue # that big square is already done
			# check if corresponding big square is won
			# square is (bigsq // 3 * 3, bigsq % 3 * 3) .. (" + 2, " + 2) in board
			midsq = ((bigsq // 3) * 3 + 1, (bigsq % 3) * 3 + 1)
			if board[midsq[0]-1][midsq[1]-1] + board[midsq[0]-1][midsq[1]] + board[midsq[0]-1][midsq[1]+1] == 'xxx' or \
				board[midsq[0]][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]][midsq[1]+1] == 'xxx' or \
				board[midsq[0]+1][midsq[1]-1] + board[midsq[0]+1][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'xxx' or \
				board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]-1] + board[midsq[0]+1][midsq[1]-1] == 'xxx' or \
				board[midsq[0]-1][midsq[1]] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]] == 'xxx' or \
				board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]+1] + board[midsq[0]+1][midsq[1]+1] == 'xxx' or \
				board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'xxx' or \
				board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]-1] == 'xxx':
				mini[bigsq] = 1 # x won in this square
			elif board[midsq[0]-1][midsq[1]-1] + board[midsq[0]-1][midsq[1]] + board[midsq[0]-1][midsq[1]+1] == 'ooo' or \
				board[midsq[0]][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]][midsq[1]+1] == 'ooo' or \
				board[midsq[0]+1][midsq[1]-1] + board[midsq[0]+1][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'ooo' or \
				board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]-1] + board[midsq[0]+1][midsq[1]-1] == 'ooo' or \
				board[midsq[0]-1][midsq[1]] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]] == 'ooo' or \
				board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]+1] + board[midsq[0]+1][midsq[1]+1] == 'ooo' or \
				board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'ooo' or \
				board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]-1] == 'ooo':
				mini[bigsq] = 2 # o won in this square
			elif ' ' not in board[midsq[0]-1][midsq[1]-1] + board[midsq[0]-1][midsq[1]] + board[midsq[0]-1][midsq[1]+1] + \
				board[midsq[0]][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]][midsq[1]+1] + \
				board[midsq[0]+1][midsq[1]-1] + board[midsq[0]+1][midsq[1]] + board[midsq[0]+1][midsq[1]+1]:
				mini[bigsq] = 3 # there are no empty spaces left (and no one's won), so it's a tie
			else:
				# print(board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]-1] + board[midsq[0]+1][midsq[1]-1])
				mini[bigsq] = 0 # nobody's won here yet
	
	def run_game(self):
		# returns final state of game_over (1 for x win, 2 for o win, 3 for draw)

		# initialize players (e.g. load model into RL player. NOTE: may not be necessary.)
		self.players[0].initialize()
		self.players[1].initialize()

		# display initial game state, if necessary
		if self.displaying:
			disp(self.board)
			disp_mini(self.mini)

		# game loop
		while not self.game_over:
			cur_move = self.players[self.turn - 1].get_move(self.board, self.mini, self.prev_move, self.turn)

			# invalid move => automatic loss
			if not valid_move(cur_move, self.board, self.mini, self.prev_move):
				print(f"Player {self.turn} played invalid move {cur_move}, which is an automatic loss.")
				game_over = 3 - self.turn # current player loses
				break
			
			# update board with move
			self.board[cur_move[0]][cur_move[1]] = PLAYERS[self.turn - 1]
		
			# update mini based on board changes
			self.update_mini(self.mini, self.board) # no reassignment bc modifying list

			# display game state, if necessary
			if self.displaying:
				print(f"Player {self.turn}'s move: ({(cur_move[0] // 3) * 3 + (cur_move[1] // 3) + 1}, {(cur_move[0] % 3) * 3 + (cur_move[1] % 3) + 1})")
				disp(self.board)
				disp_mini(self.mini)
			
			# check if anyone has won
			self.game_over = check_won(self.mini) 
			# = 0 if not yet, 1 if player 1 (x), 2 if player 2 (o), 3 if draw

			# change turns
			self.prev_move = cur_move
			self.turn = 3 - self.turn

		# end the game
		if self.displaying:
			if self.game_over == 3:
				print("Game over, it was a draw!")
			elif self.players[0].get_type() == 'user' and self.players[1].get_type() != 'user':
				if self.game_over == 1: print("Congratulations, you won!")
				else: print("Sorry, AI has won. Better luck next time!")
			elif self.players[0].get_type() != 'user' and self.players[1].get_type() == 'user':
				if self.game_over == 2: print("Congratulations, you won!")
				else: print("Sorry, AI has won. Better luck next time!")
			else:
				print(f"Player {self.game_over} has won!")
		
		return self.game_over


def get_input(prompt, options):
	# wait for the user to respond to the prompt with one of the given option strings,
	# and return that string
	answer = "default"
	while answer not in options:
		try:
			answer = input(prompt).strip().lower()
		except:
			continue
	return answer

def main():
	# intro + rules out of the way
	print("Welcome to ultimate tic-tac-toe!")
	print("This is a game of nested tic-tac-toe, where the goal is to win tic-tac-toe in the larger grid, and you must play \n \
		in the square in the larger grid corresponding to where your opponent just played in the smaller grid.")
	print("For example, if X just played in the top-right corner of the center grid, then O must play somewhere in the top-right grid.")
	print("In order to enter a move, type \"x y\" where x is the location in the large grid, \n and y is the location in the small grid.")
	print("x and y are numbered like a telephone keypad.")
	print("For example, \"1 1\" is the upper-leftmost square in the game, \"5 5\" is the centermost square, and \"8 4\" is \n \
	   the middle-left square in the bottom-middle grid.")
	_ = get_input("Type 'y' when you understand: ", ('y', 'yes'))

	# get number of players
	num_players = int(get_input("How many players are playing, 0, 1 or 2? ", ('0', '1', '2')))
	
	# if one player, need to find whether user is x or o
	player_turn = 0
	if num_players == 1:
		player_turn = int(get_input("Would you like to be player 1 or 2 (type 1 or 2)? ", ('1', '2')))
	
	# initialize players
	players = [None, None]
	if num_players == 2:
		# if two-player, play two-player tic-tac-toe
		players = [UserPlayer(), UserPlayer()]
	elif num_players == 1:
		players[player_turn - 1] = UserPlayer()
		players[2 - player_turn] = MinimaxPlayer()
	else: # num_players == 0
		# if zero players, run an experiment of some AIs against each other
		players = [StrategyPlayer(), MinimaxPlayer()]
	
	# initialize board and run game
	user_involved = players[0].get_type() == 'user' or players[1].get_type() == 'user' # display game if there's a user involved
	board = Board(players[0], players[1], displaying=user_involved, user_turn=player_turn)

	if user_involved:
		board.run_game()
	else:
		# run experiment for AIs against each other and display results
		print(f"1 = {players[0].get_type()} wins, 2 = {players[1].get_type()} wins, 3 = draw")
		num_games, wins = 50, [0, 0, 0]
		for i in range(num_games):
			end_state = board.run_game()
			board.reset()
			wins[end_state - 1] += 1
			print(end_state, end="", flush=True)
		print()
		print(f"Out of {num_games} games-- X (1) wins: {wins[0]}, O (2) wins: {wins[1]}, draws: {wins[2]}")

if __name__=='__main__':
	main()