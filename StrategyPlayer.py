# ultimate tic-tac-toe player that uses a couple of very simple, defensive heuristics to move (should all be captured by minimax with depth >1)

import random
from BasePlayer import BasePlayer
from ultimate_utils import find_moves, check_won, make_board_move, make_board_move, make_mini_move

class StrategyPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
    
    def get_type(self):
        # return string for what kind of player we are: "random", "strategy", "minimax", "rl", "user"
        return "strategy"
    
    def about_to_win(self, board_exc, cur_player):
        # return true if cur_player (1 for x, 2 for o) is about to win the square
        # given a 3x3 sub-array representing the board squares (so 'x', 'o', and ' ' as values) we're checking
        us = 'xo'[cur_player - 1]
        bf = ''.join(''.join(r) for r in board_exc) # bf for board_flat, flattened string version of board_exc

        def row_almost(s): 
            # does the current player have 2 spots in the 3-character string representation of a given row and is the last spot available
            return s.count(us) == 2 and s.count(' ') == 1

        return row_almost(bf[0:3]) or row_almost(bf[3:6]) or row_almost(bf[6:9]) or \
            row_almost(bf[0:7:3]) or row_almost(bf[1:8:3]) or row_almost(bf[2:9:3]) or \
            row_almost(bf[0:9:4]) or row_almost(bf[2:7:2])

    def good_move(self, board, mini, prev_move, ai_player, options):
        # return a good move (single row-col tuple) given options
        # ai_player is 1 if x, 2 if o, options is a list of row-col tuples

        ops = [(mv, newb := make_board_move(board, mv, ai_player), make_mini_move(mini, newb)) for mv in options] # [((move row, move col), new board, new mini), ...]
        # big square, small square corresponding to each option (each 0-8)
        op_bigsq = [(op[0][0] // 3) * 3 + op[0][1] // 3 for op in ops]
        op_smallsq = [(op[0][0] % 3) * 3 + op[0][1] % 3 for op in ops]
        unsafe_ops = [] # don't play these if we can avoid them

        # Win the game
        for i in range(len(ops)):
            if check_won(ops[i][2]) == ai_player: # we won the game
                return ops[i][0]

        # Block them from winning the game
        safe_ops = []
        for i in range(len(ops)):
            # if they are about to win the square they're directed to and that would win them the game, don't play here
            if self.about_to_win(board[op_smallsq[i] // 3 : op_smallsq[i] // 3 + 3][op_smallsq[i] % 3 : op_smallsq[i] % 3 + 3], 3 - ai_player):
                # if they're about to win the square (^), check if that move would also make them win the game
                new_mini = ops[i][2][:]
                new_mini[op_smallsq[i]] = 3 - ai_player
                if check_won(new_mini) == 3 - ai_player:
                    unsafe_ops.append(ops[i])
                    continue
            safe_ops.append(ops[i])
        ops = safe_ops
        
        # Win the square
        for i in range(len(ops)):
            if mini[op_bigsq[i]] == ai_player: # we've won the square
                return ops[i][0] # TODO: test - i think it's working but mb not
        
        # Don't direct to a full square
        safe_ops = []
        for i in range(len(ops)):
            if mini[op_smallsq[i]] == 0: # we're not directing to a full square
                safe_ops.append(ops[i])
            else: unsafe_ops.append(ops[i])
        ops = safe_ops
        
        # TODO: Block them in this square

        # Don't direct to a square they're about to win
        safe_ops = []
        for i in range(len(ops)):
            # if they are about to win the square they're directed to and that would win them the game, don't play here
            if not self.about_to_win(board[op_smallsq[i] // 3 : op_smallsq[i] // 3 + 3][op_smallsq[i] % 3 : op_smallsq[i] % 3 + 3], 3 - ai_player):
                safe_ops.append(ops[i])
            else: unsafe_ops.append(ops[i])
        ops = safe_ops

        if ops != []: return random.choice(ops)[0]
        return random.choice(unsafe_ops)[0]

    def get_move(self, board, mini, prev_move, cur_player):
		# board: 9x9 array representation of board, each position is ' ', 'x', or 'o'
		# mini: 1x9 list representation of overall board, each position is 0 for unfinished, 1 for x, 2 for o, 3 for draw
		# prev_move: tuple (row, col) of previous move
		# cur_player: 1 for x, 2 for o

        return self.good_move(board, mini, prev_move, cur_player, find_moves(board, mini, prev_move))