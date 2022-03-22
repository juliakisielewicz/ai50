"""
Tic Tac Toe Player
"""

from cmath import inf
from json.encoder import INFINITY
import math, copy
from pickle import FALSE
from re import T

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_squares=0
    for row in board:
        for square in row:
            if square == EMPTY:
                empty_squares += 1
    if empty_squares % 2 == 0:
        return O
    return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                result.add((i,j))
    return result

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #print(action)
    #print(type(action[0]))
    #print("###########")
    #print(board[action[0]][action[1]])
    if board[action[0]][action[1]] != EMPTY:
        raise Exception('Incorrect move!')

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    xs = [X, X, X]
    os = [O, O, O]
    diagonal_left = []
    diagonal_right = []

    for i in range(3):
        column = []
        [column.append(board[j][i]) for j in range(3)]

        if board[i][0:3] == xs or column == xs:
            return X
        if board[i][0:3] == os or column == os:
            return O

        diagonal_left.append(board[i][i])
        diagonal_right.append(board[2-i][i])
    
    if diagonal_left == xs or diagonal_right == xs:
        return X
    if diagonal_left == os or diagonal_right == os:
        return O
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True

    for row in board:
        for square in row:
            if square == EMPTY:
                return False
    
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)

    match result:
        case 'X':
            return 1
        case 'O':
            return -1
        case None:
            return 0
        case _:
            return None


def min_value(board, alpha, beta):

    if terminal(board):
        return utility(board), None

    value = float(inf)
    optimal = None

    for action in actions(board):
        opposite_value = max_value(result(board, action), alpha, beta)[0]
        beta = min(opposite_value, beta)

        if opposite_value < value: 
            value, optimal = opposite_value, action

        if alpha >= beta:
            break

    return value, optimal


def max_value(board, alpha, beta):

    if terminal(board):
        return utility(board), None

    value = -float(inf)
    optimal = None

    for action in actions(board):
        opposite_value = min_value(result(board, action), alpha, beta)[0]
        alpha = max(opposite_value, alpha)

        if opposite_value > value: 
            value, optimal = opposite_value, action

        if alpha >= beta:
            break
         
    return value, optimal


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return None
        
    alpha = -math.inf
    beta = math.inf

    if player(board) == X:
        return max_value(board, alpha, beta)[1]
    else:
        return min_value(board, alpha, beta)[1]