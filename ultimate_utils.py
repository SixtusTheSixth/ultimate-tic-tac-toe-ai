# utility functions for ultimate tic-tac-toe

# representing state of board as two boards: one big 9x9 board for all the x's and o's (' ' for empty), and 'mini' for the 3x3 large board, who's won what (0, 1 = 'x', 2 = 'o', 3 = 'c').
# board is a 2d 9x9 array, mini is a 1d 1x9 array

global PLAYERS; PLAYERS = ('x', 'o') # imported in Board class, a reminder that x is first and o is second

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