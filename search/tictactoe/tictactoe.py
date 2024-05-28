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
    selected_tile = board[action[0]][action[1]]
    # do not overwrite tiles
    if selected_tile != EMPTY:
        raise ValueError("Must provide a valid action")

    active_player = player(board)
    resulting_board = deepcopy(board)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
