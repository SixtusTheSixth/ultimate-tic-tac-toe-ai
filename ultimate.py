# one-player and two-player tic-tac-toe

# representing state of board as two boards: one big 9x9 board for all the x's and o's (' ' for empty), and 'mini' for the 3x3 large board, who's won what (0, 1 = 'x', 2 = 'o', 3 = 'c').
# board is a 2d 9x9 array, mini is a 1d 1x9 array

# TODO: DO CACHING it'll help so much bc when squares are filled it won't have to check the position twice
# TODO: add midgame alpha-beta and a position heuristic (e.g. how many squares you've won minus how many squares the opponent has won, and how many you're about to win, not directing to a full sq, etc)
# TODO: check Othello later steps to see if can include caching w globals, symmetry, etc.
# TODO: add RL AI

import re
import random

global PLAYERS; PLAYERS = ('x', 'o')
global N_AB; N_AB = 6
global N_AB_SQAURES; N_AB_SQUARES = 4 # after how many are left should we think to the end
global N_AB_MIDGAME; N_AB_MIDGAME = 4
global AI_TYPE; AI_TYPE = 1 # 0 for random, 1 for minimax, 2 for RL

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

def disp(board):
	# print a string representing the state of the board, in human-readable format
	d = ""
	for vert in range(3):
		d += " | ".join("|".join(board[vert*3][3*i : 3*i + 3]) for i in range(3))
		d += "\n" + " | ".join(["-+-+-"] * 3) + "\n"
		d += " | ".join("|".join(board[vert*3+1][3*i : 3*i + 3]) for i in range(3))
		d += "\n" + " | ".join(["-+-+-"] * 3) + "\n"
		d += " | ".join("|".join(board[vert*3+2][3*i : 3*i + 3]) for i in range(3))
		if vert < 2: d += "\n" + "-" * 6 + "+" + "-" * 7 + "+" + "-" * 6 + "\n"
	d += "\n"
	# return d
	print(d)

def disp_mini(mini):
	# return a string representing the state of the mini board, in human-readable format
	m = [' xoc'[c] for c in mini]
	d = ""
	d += "\n-+-+-\n".join("|".join(m[i] for i in range(3*j,3*j+3)) for j in range(3))
	d += "\n"
	# return d
	print(d)

def find_moves(board, mini, prev_move):
	# return a list of tuples in row-col format of valid moves from this position
	moves = []
	for i in range(9):
		for j in range(9):
			if valid_move((i, j), board, mini, prev_move):
				moves.append((i, j))
	return moves

def valid_move(move, board, mini, prev_move):
	# check whether a given move (in row-col format) is valid, considering the board state and previous move
	# don't need to deep-copy board since not modifying it
	# move and prev_move are tuples of integers in 0..8
	if move[0] not in list(range(0, 9)) or move[1] not in list(range(0, 9)): return False # check that move is within bounds (just in case, shouldn't need)
	move_bigsq, _ = (move[0] // 3) * 3 + (move[1] // 3), (move[0] % 3) * 3 + (move[1] % 3)
	_, prev_smallsq = (prev_move[0] // 3) * 3 + (prev_move[1] // 3), (prev_move[0] % 3) * 3 + (prev_move[1] % 3)
	if board[move[0]][move[1]] != ' ': return False # if you played in a spot that already has been played in, it's wrong
	if mini[move_bigsq] != 0: return False # if you played in a big square that is already completed, it's wrong
	if prev_move == (-1, -1): return True # if it's the first move, you can go anywhere
	if mini[prev_smallsq] != 0: return True # if you were directed to a full square, you can go anywhere
	if move_bigsq != prev_smallsq: return False # if you didn't play in the square you were directed to, it's wrong
	return True

def update_mini(mini, board):
	# update big board given new board state
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

def check_won(mini):
	# checks whether the game is over based on the mini board
	# returns 0 if not over, 1 if player 1 (x) won, 2 if player 2 (o), 3 if draw
	if 0 not in mini: return 3
	elif mini[0:3] == [1] * 3 or mini[3:6] == [1] * 3 or mini[6:9] == [1] * 3 or \
		mini[0:7:3] == [1] * 3 or mini[1:8:3] == [1] * 3 or mini[2:9:3] == [1] * 3 or \
		mini[0:9:4] == [1] * 3 or mini[2:8:2] == [1] * 3:
		return 1 # x won in this square
	elif mini[0:3] == [2] * 3 or mini[3:6] == [2] * 3 or mini[6:9] == [2] * 3 or \
		mini[0:7:3] == [2] * 3 or mini[1:8:3] == [2] * 3 or mini[2:9:3] == [2] * 3 or \
		mini[0:9:4] == [2] * 3 or mini[2:8:2] == [2] * 3:
		return 2 # o won in this square
	else:
		return 0 # nobody's won here yet

def random_move(board, mini, prev_move, ai_player):
	# get a random valid move (in row-col format)
	# ai_player = 1 if x and 2 if o
	# move until we get a valid move
	valid = False
	move = (-1, -1)
	while not valid:
		move = (random.randint(0, 9), random.randint(0, 9))
		valid = valid_move(move, board, mini, prev_move)
	return move

def make_mini_move(mini, board):
	# same as update_mini but return a copy of mini instead of modifying in place, for ai purposes
	ret_mini = mini[:] # copy to modify + return
	for bigsq, mini_val in enumerate(mini):
		if mini_val != 0: continue # that big square is already done
		# check if corresponding big square is won
		# square is (bigsq // 3 * 3, bigsq % 3 * 3) .. (" + 2, " + 2) in board
		midsq = ((bigsq // 3) * 3 + 1, (bigsq % 3) * 3 + 1)
		if ' ' not in board[midsq[0]-1][midsq[1]-1] + board[midsq[0]-1][midsq[1]] + board[midsq[0]-1][midsq[1]+1] + \
			board[midsq[0]][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]][midsq[1]+1] + \
			board[midsq[0]+1][midsq[1]-1] + board[midsq[0]+1][midsq[1]] + board[midsq[0]+1][midsq[1]+1]:
			ret_mini[bigsq] = 3 # there are no empty spaces left, so it's a tie
		elif board[midsq[0]-1][midsq[1]-1] + board[midsq[0]-1][midsq[1]] + board[midsq[0]-1][midsq[1]+1] == 'xxx' or \
			board[midsq[0]][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]][midsq[1]+1] == 'xxx' or \
			board[midsq[0]+1][midsq[1]-1] + board[midsq[0]+1][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'xxx' or \
			board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]-1] + board[midsq[0]+1][midsq[1]-1] == 'xxx' or \
			board[midsq[0]-1][midsq[1]] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]] == 'xxx' or \
			board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]+1] + board[midsq[0]+1][midsq[1]+1] == 'xxx' or \
			board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'xxx' or \
			board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]-1] == 'xxx':
			ret_mini[bigsq] = 1 # x won in this square
		elif board[midsq[0]-1][midsq[1]-1] + board[midsq[0]-1][midsq[1]] + board[midsq[0]-1][midsq[1]+1] == 'ooo' or \
			board[midsq[0]][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]][midsq[1]+1] == 'ooo' or \
			board[midsq[0]+1][midsq[1]-1] + board[midsq[0]+1][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'ooo' or \
			board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]-1] + board[midsq[0]+1][midsq[1]-1] == 'ooo' or \
			board[midsq[0]-1][midsq[1]] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]] == 'ooo' or \
			board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]+1] + board[midsq[0]+1][midsq[1]+1] == 'ooo' or \
			board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]+1] == 'ooo' or \
			board[midsq[0]-1][midsq[1]+1] + board[midsq[0]][midsq[1]] + board[midsq[0]+1][midsq[1]-1] == 'ooo':
			ret_mini[bigsq] = 2 # o won in this square
		else:
			# print(board[midsq[0]-1][midsq[1]-1] + board[midsq[0]][midsq[1]-1] + board[midsq[0]+1][midsq[1]-1])
			ret_mini[bigsq] = 0 # nobody's won here yet
	return ret_mini

def make_board_move(board, move, player):
	# just update board (not mini!) based on given move (in row/col format)
	# and return a copy of board, for ai purposes
	# player = 1 if x, 2 if o
	new_board = [i[:] for i in board]
	new_board[move[0]][move[1]] = 'xo'[player - 1]
	return new_board

def max_moves_left(board, mini):
	# return the number of empty squares in the board squares that correspond to unfinished mini squares
	ans = 0
	for s in mini:
		midsq = ((s // 3) * 3, (s % 3) * 3)
		ans += sum(board[midsq[0] + i][midsq[1] + j] == ' ' for i in range(3) for j in range(3))
	return ans

def about_to_win(board_exc, cur_player):
	# return true if cur_player (1 for x, 2 for o) is about to win the square
	# given a 3x3 sub-array representing the board squares (so 'x', 'o', and ' ' as values) we're checking
	us = 'xo'[cur_player - 1]
	bf = ''.join(''.join(r) for r in board_exc) # bf for board_flat, flattened string version of board_exc
	if bf[0:2] == us * 2 and bf[2] == ' ' or bf[0] + bf []

def good_move(board, mini, prev_move, ai_player, options):
	# return a good move (single row-col tuple) given options
	# ai_player is 1 if x, 2 if o, options is a list of row-col tuples

	full_options = [(mv, newb := make_board_move(board, mv, ai_player), make_mini_move(mini, newb)) for mv in options]
	for op in full_options:
		if check_won(op[2]) == ai_player: # we won the game
			return op[0]
	mv_sqs = ((op[0][0] // 3) * 3 + op[0][1] // 3, (op[0][0] % 3) * 3 + op[0][1] % 3)
	for op in full_options:
		# block them from directly winning
		# if they are about to win the square they're directed to and that would win them the game, don't play here

	for op in full_options:
		if mini[mv_sqs[0]] == ai_player: # we've won the square
			return op[0]
	# TODO: block people in this square
	for op in full_options:
		if mini[mv_sqs[1]] == 0: # we're not directing to a full square # TODO: this is not working
			return op[0]
	""" # TODO
	for op in full_options:
		# if can not direct to a square they're about to win, do that
		midsq = mv_sqs[1] + 
	"""
	return random.choice(full_options)[0]

def board_evaluation(board, mini, prev_move, ai_player, options):
	# given board and mini states, ai_player (1 if x, 2 if o), and options as list of row-col tuples, 
	# return a heuristic value representing how good this position is for ai_player
	heuristic = 0
	heuristic += sum(5 if i == ai_player else 0 for i in mini) # add 2 for every mini we have
	heuristic -= sum(5 if i == 3 - ai_player else 0 for i in mini) # minus 2 for every mini they have
	# TODO: +/- 2 for squares about to win
	return heuristic / 45 # scale to +/- 9

def mmx_ab(board, mini, prev_move, cur_player, lowerBound = -9, upperBound = 9):
	# get minimax + alpha/beta pruning next move given a previous move and the board and mini states
	# cur_player = 1 if x and 2 if o
	# return [score, ... moves in row-col format in reverse order]
	next_player = 3 - cur_player
	myOptions = find_moves(board, mini, prev_move)
	
	# if game is over, return appropriate score
	game_over = check_won(mini)
	if game_over: # i.e. game_over != 0
		if game_over != cur_player:
			return [-10] # we lost
		elif game_over == 3:
			return [-5] # we drew
		else:
			return [10] # we won
	
	# negamax recursion
	bestSoFar = [lowerBound - 1]
	for mv in myOptions:
		new_board = make_board_move(board, mv, cur_player)
		new_mini = make_mini_move(mini, new_board)
		ab = mmx_ab(new_board, new_mini, mv, next_player, -upperBound, -lowerBound)
		score = -ab[0]

		if score < lowerBound: continue
		if score > upperBound: return [score]
		if score > bestSoFar[0]:
			bestSoFar = [score] + ab[1:] + [mv] # compile moves in reverse order, 0th element is min score

		lowerBound = score + 1
	
	if len(bestSoFar) > 1 and bestSoFar[-1] not in myOptions: # shouldn't trigger?
		print('you played a prev played move')
		print(f'{bestSoFar} {board} {mini} {cur_player} options: {myOptions}')
		exit()

	return bestSoFar

def mmx_move(board, mini, prev_move, cur_player):
	return mmx_ab(board, mini, prev_move, cur_player)[-1]

def midgame_ab(board, mini, prev_move, cur_player, lowerBound = -9, upperBound = 9, depth=0):
	# get minimax + alpha/beta pruning next move given a previous move and the board and mini states
	# cur_player = 1 if x and 2 if o
	# return [score, ... moves in row-col format in reverse order]
	myOptions = find_moves(board, mini, prev_move)
	next_player = 3 - cur_player

	if depth == N_AB_MIDGAME:
		score = board_evaluation(board, mini, prev_move, cur_player, myOptions)
		return [score]
	
	game_over = check_won(mini)
	if game_over: # i.e. game_over != 0
		if game_over != cur_player:
			return [-10] # we lost
		elif game_over == 3:
			return [-5] # we drew
		else:
			return [10] # we won
	
	if len(myOptions) == 1:
		mv = [*myOptions][0] # idk why not just myOptions[0]
		new_board = make_board_move(board, mv, cur_player)
		new_mini = make_mini_move(mini, new_board)
		ab = midgame_ab(new_board, new_mini, mv, next_player, -upperBound, -lowerBound, depth+1)
		return [-ab[0]] + ab[1:] + [mv]
	
	bestSoFar = [lowerBound - 1]
	for mv in myOptions:
		new_board = make_board_move(board, mv, cur_player)
		new_mini = make_mini_move(mini, new_board)
		ab = midgame_ab(new_board, new_mini, mv, next_player, -upperBound, -lowerBound, depth+1)
		score = -ab[0]
		if score < lowerBound: continue # not good enough
		if score > upperBound: return [score] # too good, caller will not choose
		if score > bestSoFar[0]:
			bestSoFar = [score] + ab[1:] + [mv] # compile moves in reverse order, 0th element is min score
		lowerBound = score + 1 # max(lowerBound, score + 1) # should be equivalent

	return bestSoFar

def one_player_loop(player_turn):
	# run a one-player game vs ai, where player_turn is whether the player wants to go 1st or 2nd
	board = [[' '] * 9 for i in range(9)]
	mini = [0] * 9
	game_over = 0
	turn = 0
	prev_move = (-1, -1)
	disp(board)

	# game loop
	while not game_over:
		# get next move from player or ai
		if turn == player_turn - 1: # b/c player_turn is 1 or 2
			cur_move = -1
			while cur_move == -1:
				# get the move from input
				move_str = re.findall(r'.*?([1-9]).*?([1-9]).*', input(f"Player {turn + 1}'s move: ").strip().lower())
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
		else: # ai's turn
			if AI_TYPE == 0: # random
				cur_move = random_move(board, mini, prev_move, turn + 1) # ai_player is 2 if player_turn is 1 and vice versa
			elif AI_TYPE == 1: # alpha-beta
				if (mini.count(0) < N_AB_SQUARES or max_moves_left(board, mini) < N_AB): # only use negamax when close to end of game
					negamax = mmx_ab(board, mini, prev_move, turn + 1)
					if -0.5 <= negamax[0] <= 10:
						print(f"negamax with score of {negamax[0]}")
						cur_move = negamax[-1]
					else:
						print(f"negamax not good enough: {negamax[0]} so good move")
						cur_move = good_move(board, mini, prev_move, turn + 1, find_moves(board, mini, prev_move))
				else:
					ab = midgame_ab(board, mini, prev_move, turn + 1)
					if -0.5 <=ab[0]<= 10:
						print(f"midgame a/b with score {ab[0]}")
						cur_move = ab[-1]
					else:
						print(f"midgame a/b not good enough: {ab[0]} so good move")
						cur_move = good_move(board, mini, prev_move, turn + 1, find_moves(board, mini, prev_move))
					# random_move(board, mini, prev_move, turn + 1)
			else: # == 2: RL
				cur_move = random_move(board, mini, prev_move, turn + 1) # TODO
			print(f"AI's move: ({(cur_move[0] // 3) * 3 + (cur_move[1] // 3) + 1}, {(cur_move[0] % 3) * 3 + (cur_move[1] % 3) + 1})")
		
		# update board with move
		board[cur_move[0]][cur_move[1]] = PLAYERS[turn]
		
		# update mini based on board changes
		update_mini(mini, board) # no reassignment bc modifying list

		# display board
		disp(board)
		disp_mini(mini) # may want to remove if change disp(board) to also show big square wins
		# but maybe not, bc that would take away info

		# check if anyone has won
		game_over = check_won(mini) 
		# = 0 if not yet, 1 if player 1 (x), 2 if player 2 (o), 3 if draw

		# change turns
		prev_move = cur_move
		turn = 1 - turn
	
	# end the game
	if game_over == player_turn:
		print(f"Congratulations, you won!")
	elif game_over < 3:
		print(f"Sorry, AI has won. Better luck next time!")
	else:
		print("Game over, it was a draw!")

def two_player_loop():
	# run a two-player game, player 1 vs player 2
	# remember, possible square states are 'x', 'o', ' ', 'c' (for large squares only)

	# set up variables
	board = [[' '] * 9 for i in range(9)]
	mini = [0] * 9
	game_over = 0
	turn = 0
	prev_move = (-1, -1)
	disp(board)

	# game loop
	while not game_over:
		# get next move
		cur_move = -1
		while cur_move == -1:
			# get the move from input
			move_str = re.findall(r'.*?([1-9]).*?([1-9]).*', input(f"Player {turn + 1}'s move: ").strip().lower())
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
		
		# update board with move
		board[cur_move[0]][cur_move[1]] = PLAYERS[turn]
		
		# update mini based on board changes
		update_mini(mini, board) # no reassignment bc modifying list

		# display board
		disp(board)
		disp_mini(mini) # may want to remove if change disp(board) to also show big square wins
		# but maybe not, bc that would take away info

		# check if anyone has won
		game_over = check_won(mini) 
		# = 0 if not yet, 1 if player 1 (x), 2 if player 2 (o), 3 if draw

		# change turns
		prev_move = cur_move
		turn = 1 - turn
	
	# end the game
	if game_over < 3:
		print(f"Congratulations, player {game_over} has won!")
	else:
		print("Game over, it was a draw!")

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
	num_players = int(get_input("How many players are playing, 1 or 2? ", ('1', '2')))
	
	# if one-player, play one-player tic-tac-toe
	if num_players == 1:
		player_turn = int(get_input("Would you like to be player 1 or 2 (type 1 or 2)? ", ('1', '2')))
		one_player_loop(player_turn)
	else:
		# if two-player, play two-player tic-tac-toe
		two_player_loop()

if __name__=='__main__':
	main()

# useful testing code:
# board = [['x', ' ', ' '] + [' ']*6, [' ', 'x', ' '] + [' ']*6, [' ', ' ', 'x'] + [' ']*6] + [[' ']*9 for i in range(6)]
# print('\n'.join(str(board[i]) for i in range(9))
