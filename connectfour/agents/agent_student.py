# s3563242 - Richard Kuoch
# s3602202 - Matthew Lu 

from connectfour.agents.computer_player import RandomAgent
from connectfour.agents.agent import Agent
import random
import math

class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 3


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.minimax(next_state, self.MaxDepth, -math.inf, math.inf, True))

        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    # new minimax with alpha beta pruning
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):

        if depth == 0 or board.terminal():
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        if maximizingPlayer:
            bestVal = -math.inf
            for move in valid_moves:
                    next_state = board.next_state(self.id % 2 + 1, move[1])
                    next_score = self.minimax(next_state, depth - 1, alpha, beta, False)
                    if next_score > bestVal:
                        bestVal = next_score
                    alpha = max(alpha, bestVal)
                    if alpha >= beta:
                        break
            return bestVal

        #Minimizing player
        else:
            bestVal = math.inf
            for move in valid_moves:
                next_state = board.next_state(self.id, move[1])
                next_score = self.minimax(next_state, depth - 1, alpha, beta, True)
                if next_score < bestVal:
                    bestVal = next_score
                beta = min(beta, bestVal)
                if alpha >= beta:
                    break
            return bestVal

    def evaluateGroupPieces(self, group, current_row, is_row):
       score = 0
       opponent_id = 0
       empty_cell = 0
       if ((self.id / 2) == 1):
           opponent_id = 1
       else:
           opponent_id = 2

       # check 4 in a row for AI pieces
       if group.count(self.id) == 4:
           score += 1000

       # check 4 in a row for opponent pieces
       if group.count(opponent_id) == 4:
           score -= 1000

       # check 2 in a row for AI pieces
       if group.count(self.id) == 2 and group.count(empty_cell) == 2:
           score += 2

       # check 2 in a row for opponent pieces
       if group.count(opponent_id) == 2 and group.count(empty_cell) == 2:
           score -= 10

       # check 3 in a row for AI pieces
       if group.count(self.id) == 3 and group.count(empty_cell) == 1:
           score += 15

    # check 3 in a row for opponent pieces
       if group.count(opponent_id) == 3 and group.count(empty_cell) == 1:
           score -= 100

    # odd-even strategy commented out below as unable to test against all agent projects.
        # if group.count(self.id) == 3 and group.count(empty_cell) == 1:
        #     if is_row == 1 and self.id == 1 and current_row % 2 != 0:
        #         score += 30
        #     elif is_row == 1 and self.id == 2 and current_row % 2 == 0:
        #         score += 30
        #     else:
        #         score += 15
        #
        # if group.count(opponent_id) == 3 and group.count(empty_cell) == 1:
        #     if is_row == 1 and opponent_id == 1 and current_row % 2 != 0:
        #         score -= 120
        #     elif is_row == 1 and opponent_id == 2 and current_row % 2 == 0:
        #         score -= 120
        #     else:
        #         score -= 100

       return score


    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it.
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.
        Board Variables:
            board.width = 7
            board.height = 6
            board.last_move
            board.num_to_connect = 4
            board.winning_zones
            board.score_array
            board.current_player_score
        Board Functions:
            get_cell_value(row, col) - retrieve the value at a specific (row, col) location. 1 - P1, 2 - P2, 0 - Empty
            try_move(col) - returns the appropriate row where the piece will be located
            valid_move(row, col) - returns True/False whether the row value is the bottom most empty position in column
            valid_moves() - a generator of all valid moves in the current board state
            terminal(self) - returns true when the game is finished, otherwise false
            legal_moves() - returns the full list of legal moves for next player
            next_state(turn)
            winner() - if the game has a winner, it returns the player number(P1 - 1, P2 - 2) If game is still going, returns 0s
        """
        # return random.uniform(0, 1)


        # scoring heuristic / evaluation heuristic

        # center column                 +4
        # lines of two                  +2
        # lines of three                +15
        # win! connect 4                +1000
        # opponent lines of 2           -10
        # opponent winnable line of 3  -100
        # win! opponent connect 4       -1000

        score = 0
        bottom_row_position = 5
        cell_value_empty = 0

        opponent_id = 0
        if ((self.id / 2) == 1):
            opponent_id = 1
        else:
            opponent_id = 2

        # center column position heuristic +4
        for row in range(board.height):
            for col in range(board.width):

                if (board.get_cell_value(bottom_row_position, board.width //2) == self.id):
                    score += 4

                if (board.get_cell_value(row, board.width //2) == self.id):
                    score += 1

                if (board.get_cell_value(bottom_row_position, col) == self.id):
                    score += 0

        # check rows
        for col in range(board.width - 3):
            for row in range(board.height):
                group = [board.get_cell_value(row, col)]
                for i in range(1, 4):
                    next_value = board.get_cell_value(row, col + i)
                    group.append(next_value)
                current_row = i
                is_row = 1
                score += self.evaluateGroupPieces(group, current_row, is_row)

        # check columns
        for col in range(board.width):
            for row in range(board.height - 3):
                group = [board.get_cell_value(row, col)]
                for i in range(1, 4):
                    next_value = board.get_cell_value(row + i, col)
                    group.append(next_value)
                current_row = i
                is_row = 0
                score += self.evaluateGroupPieces(group, current_row, is_row)

                # if (board.get_cell_value(row, col) == self.id and board.get_cell_value(row + 1,col) == self.id and
                #     board.get_cell_value(row + 2, col) == self.id and board.get_cell_value(row + 3, col) == self.id):
                #     score += 1000

        # check positive diagonal
        for col in range(board.width - 3):
            for row in range(board.height - 3):
                group = [board.get_cell_value(row, col)]
                for i in range(1, 4):
                    next_value = board.get_cell_value(row + i, col + i)
                    group.append(next_value)
                current_row = i
                is_row = 0
                score += self.evaluateGroupPieces(group, current_row, is_row)

        # check negative diagonal
        for col in range(board.width - 3):
            for row in range(3, board.height):
                group = [board.get_cell_value(row, col)]
                for i in range(1, 4):
                    next_value = board.get_cell_value(row - i, col + i)
                    group.append(next_value)
                current_row = i
                is_row = 0
                score += self.evaluateGroupPieces(group, current_row, is_row)



        return score
