"""
Tic Tac Toe Player
"""

import math
import copy
from os import close

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
    ##if evertyhing in board = empty, return X
    countx = 0
    counto = 0
    for sublist in board:
        for item in sublist:
            if item == X:
                countx += 1
            if item == O:
                counto += 1
            
    if counto >= countx:
        return X
    elif counto < countx:
        return O
    else:
        return None
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    my_set = set()
    for sublist_idx, sublist in enumerate(board):
        for item_idx, item in enumerate(sublist):
            if item == EMPTY:
                my_set.add((sublist_idx, item_idx))
    return my_set

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("This action is not valid for the board!")
    
    copied_board = copy.deepcopy(board)

    copied_board[action[0]][action[1]] = player(board)

    return copied_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_o_counter = 0
    win_x_counter = 0
    ## check horizontally
    for row in board:
        for item in row:
            if item == O:
                win_o_counter += 1
            elif item == X:
                win_x_counter += 1
        if win_o_counter == 3:
            return O
        elif win_x_counter == 3:
            return X
    ## reset counters
        else:
            win_o_counter = 0
            win_x_counter = 0
    # check verticallly
    for col_index in range(3):
        column = [row[col_index] for row in board]
        for item in column:
            if item == O:
                win_o_counter += 1
            elif item == X:
                win_x_counter += 1
        if win_o_counter == 3:
            return O
        elif win_x_counter == 3:
            return X
        else:
            win_x_counter = 0
            win_o_counter = 0
    
    #diagonal checks
    ##from top-left to bottom-right
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    ##right-to-left
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True     
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True
    
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    value = float('-inf')
    move = None
    for action in actions(board):
        #specify the best value and move while considering opponents possible moves
        aux, act = min_value(result(board, action))
        if aux > value:
            value = aux
            move = action
            if value == 1:
                return value, move

    return value, move


def min_value(board):
    if terminal(board):
        return utility(board), None

    value = float('inf')
    move = None
    for action in actions(board):
        aux, act = max_value(result(board, action))
        if aux < value:
            value = aux
            move = action
            if value == -1:
                return value, move

    return value, move


