"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from typing import List, Tuple

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board: List[List[str]]) -> str:
    """
    Returns player who has the next turn on a board.
    """
    sum_x = 0
    for row in board:
        sum_x += row.count(X)

    sum_o = 0
    for row in board:
        sum_o += row.count(O)

    # X is the active player when O has more tiles, or when they're tied
    return X if sum_o >= sum_x else O


def actions(board: List[List[str]]) -> List[Tuple[int, int]]:
    """
    Returns set of all possible actions (i, j) available on the board.
    row -> i
    tile -> j
    """
    open_tiles = []
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == EMPTY:
                open_tiles.append((i, j))

    # list of all non occupied tiles
    return open_tiles


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    targeted_tile = board[action[0]][action[1]]
    # do not overwrite tiles
    if targeted_tile != EMPTY:
        raise ValueError("Must provide a valid action")

    # determine what player to mark
    active_player = player(board)
    # copy the board and update it
    resulting_board = deepcopy(board)
    resulting_board[action[0]][action[1]] = active_player

    return resulting_board


def winner(board: List[List[str]]) -> str:
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontals
    for row in board:
        if row.count(row[0]) == 3:
            return row[0]

    # check verticals
    for i in range(3):
        col = []
        for j in range(3):
            # static column, dynamic row
            col.append(board[j][i])
        if col.count(col[0]) == 3:
            return col[0]

    # check diagonals
    diagonals = [
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    for diagonal in diagonals:
        if diagonal.count(diagonal[0]) == 3:
            return diagonal[0]


def terminal(board: List[List[str]]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    # the board is completely full
    if actions(board) == []:
        return True

    # the game is over if somebody won
    elif winner(board):
        return True

    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player = winner(board)
    if player == X:
        return 1
    elif player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    return actions(board)[0]
