# ultimate tic-tac-toe player that looks a few moves ahead using negamax with alpha/beta pruning

import random
from BasePlayer import BasePlayer
from ultimate_utils import find_moves, check_won, disp, disp_mini, make_board_move, make_mini_move

class MinimaxPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.N_AB = 6 # how many individual moves left available for us to think to the end
        self.N_AB_SQUARES = 4 # how many big squares left unfinished for us to think to the end
        self.N_AB_MIDGAME = 3 # how many moves ahead to count for midgame minimax
    
    def get_type(self):
        # return string for what kind of player we are: "random", "strategy", "minimax", "rl", "user"
        return "minimax"
    
    def max_moves_left(self, board, mini):
        # return the number of empty squares in the board squares that correspond to unfinished mini squares
        ans = 0
        for s in mini:
            midsq = ((s // 3) * 3, (s % 3) * 3)
            ans += sum(board[midsq[0] + i][midsq[1] + j] == ' ' for i in range(3) for j in range(3))
        return ans
    
    def board_evaluation(self, board, mini, prev_move, ai_player, options):
        # given board and mini states, ai_player (1 if x, 2 if o), and options as list of row-col tuples, 
        # return a heuristic value representing how good this position is for ai_player
        heuristic = 0
        heuristic += sum(5 if i == ai_player else 0 for i in mini) # add 2 for every mini we have
        heuristic -= sum(5 if i == 3 - ai_player else 0 for i in mini) # minus 2 for every mini they have
        # TODO: +/- 2 for squares about to win
        return heuristic / 45 # scale to +/- 9

    def mmx_ab(self, board, mini, prev_move, cur_player, lowerBound = -9, upperBound = 9):
        # get negamax + alpha/beta pruning next move given a previous move and the board and mini states
        # cur_player = 1 if x and 2 if o
        # Returns a tuple (score, move_sequence), where move_sequence is a list (in reverse order) of moves each in row-col format.
        next_player = 3 - cur_player
        myOptions = find_moves(board, mini, prev_move)
        
        # if game is over, return appropriate score
        game_over = check_won(mini)
        if game_over: # i.e. game_over != 0
            if game_over != cur_player:
                return (-10, [])  # we lost
            elif game_over == 3:
                return (-5, [])   # we drew
            else:
                return (10, [])   # we won
        
        # Set initial best score and move sequence.
        bestScore = lowerBound - 2
        bestMoves = []  # Will store the best move sequence (in reverse order)

        if not myOptions:
            disp(board)
            disp_mini(mini)
            print(f"no options for player {'xo'[cur_player - 1]} in above position")
            exit()
        
        for mv in myOptions:
            new_board = make_board_move(board, mv, cur_player)
            new_mini = make_mini_move(mini, new_board)
            childScore, childMoves = self.mmx_ab(new_board, new_mini, mv, next_player, -upperBound, -lowerBound)
            score = -childScore # Negamax: invert child score

            if score < lowerBound: continue
            if score > upperBound: # If we exceed the upper bound, do an immediate cutoff with the complete move sequence.
                return (score, [mv] if childMoves == [] else childMoves + [mv])
                # return (score, childMoves + [mv])
            if score > bestScore: # Update the best score and corresponding move sequence if we found a better option.
                bestScore = score
                bestMoves = childMoves + [mv]

            lowerBound = max(lowerBound, score)

        if bestMoves and bestMoves[-1] not in myOptions:
            print(f"Invalid move detected: {bestMoves[-1]} not in {myOptions}")
            exit()

        return (bestScore, bestMoves)

    def mmx_move(self, board, mini, prev_move, cur_player):
        # mmx_ab returns a tuple; we extract the move sequence.
        score, moves = self.mmx_ab(board, mini, prev_move, cur_player)
        # If moves is not empty, return the first move in the sequence (the last appended move).
        # (The moves are stored in reverse order.)
        if moves:
            return moves[-1] # moves[0]?
        else:
            # In a terminal position, there may be no move.
            # return None # Somehow, this is broken... I guess it's possible to reach immediate terminal states or smth
            return random.choice(find_moves(board, mini, prev_move))

    def midgame_ab(self, board, mini, prev_move, cur_player, lowerBound = -9, upperBound = 9, depth=0):
        # get minimax + alpha/beta pruning next move given a previous move and the board and mini states
        # cur_player = 1 if x and 2 if o
        # Return tuple (score, moves) rather than a flat list.
        # moves is a list of moves in forward order (first move is the move to play now).
        myOptions = find_moves(board, mini, prev_move)
        next_player = 3 - cur_player

        if depth == self.N_AB_MIDGAME:
            score = self.board_evaluation(board, mini, prev_move, cur_player, myOptions)
            return (score, [])
        
        game_over = check_won(mini)
        if game_over: # i.e. game_over != 0
            if game_over != cur_player:
                return (-10, []) # we lost
            elif game_over == 3:
                return (-5, []) # we drew
            else:
                return (10, []) # we won
        
        # If there is only one legal move, just follow it.
        if len(myOptions) == 1:
            mv = list(myOptions)[0]  # Modification: converting to list for clarity.
            new_board = make_board_move(board, mv, cur_player)
            new_mini = make_mini_move(mini, new_board)
            child_score, child_moves = self.midgame_ab(new_board, new_mini, mv, next_player, -upperBound, -lowerBound, depth + 1)
            score = -child_score  # Negamax inversion.
            return (score, child_moves + [mv])
        
        # Initialize best score and move sequence.
        bestSoFar = (lowerBound - 1, [])

        for mv in myOptions:
            new_board = make_board_move(board, mv, cur_player)
            new_mini = make_mini_move(mini, new_board)
            child_score, child_moves = self.midgame_ab(new_board, new_mini, mv, next_player, -upperBound, -lowerBound, depth + 1)
            score = -child_score  # Negamax inversion

            if score < lowerBound: continue # not good enough
            if score > upperBound: return (score, child_moves + [mv]) # + ab[1:] + [mv]??
            if score > bestSoFar[0]:
                bestSoFar = (score, child_moves + [mv]) # compile moves in reverse order, 0th element is min score
            lowerBound = max(lowerBound, score)

        # If no branch produced a move sequence at the root, choose a random legal move.
        if bestSoFar[1] == [] and depth == 0:  # every move loses, so fallback
            # print("this happened") # NOTE: this does actually happen sometimes
            return (bestSoFar[0], [random.choice(list(myOptions))])

        return bestSoFar

    def get_move(self, board, mini, prev_move, cur_player):
        # board: 9x9 array representation of board, each position is ' ', 'x', or 'o'
        # mini: 1x9 list representation of overall board, each position is 0 for unfinished, 1 for x, 2 for o, 3 for draw
        # prev_move: tuple (row, col) of previous move
        # cur_player: 1 for x, 2 for o
        
        use_negamax = (mini.count(0) < self.N_AB_SQUARES or self.max_moves_left(board, mini) < self.N_AB) # only use negamax when close to end of game

        cur_move = -1
        if use_negamax:
            negamax = self.mmx_move(board, mini, prev_move, cur_player)
            #-- print("negamax, looking to end of game")
            if not negamax:
                print(f"Error - endgame: no moves for player {cur_player} of type negamax in position with prev move {prev_move}")
                disp(board)
                disp_mini(mini)
                exit()
            cur_move = negamax
        else:
            score, moves = self.midgame_ab(board, mini, prev_move, cur_player)
            #-- print(f"midgame a/b with score {score:.2f}")
            if moves:
                cur_move = moves[-1]
            else:
                print(f"Error - midgame: no moves for player {cur_player} of type minimax in position with prev move {prev_move}")
                disp(board)
                disp_mini(mini)
                exit()
    
            if type(cur_move) != tuple:
                print(f"Error - {cur_move} is not a tuple, using {'nega' if use_negamax else 'mini'}max")
                disp(board)
                disp_mini(mini)
                exit()
        
        return cur_move