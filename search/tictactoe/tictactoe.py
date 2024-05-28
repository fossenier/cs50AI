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
    open_tiles = set()
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == EMPTY:
                open_tiles.add((i, j))

    # list of all non occupied tiles
    return open_tiles


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
        raise ValueError("Must provide a valid action")
    targeted_tile = board[i][j]
    # do not overwrite tiles
    if targeted_tile != EMPTY:
        raise ValueError("Must provide a valid action")

    # determine what player to mark
    active_player = player(board)
    # copy the board and update it
    resulting_board = deepcopy(board)
    resulting_board[i][j] = active_player

    return resulting_board


def winner(board: List[List[str]]) -> str:
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontals
    for row in board:
        if row.count(row[0]) == 3:
            if row[0]:
                return row[0]

    # check verticals
    for i in range(3):
        col = []
        for j in range(3):
            # static column, dynamic row
            col.append(board[j][i])
        if col.count(col[0]) == 3:
            if col[0]:
                return col[0]

    # check diagonals
    diagonals = [
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    for diagonal in diagonals:
        if diagonal.count(diagonal[0]) == 3:
            if diagonal[0]:
                return diagonal[0]


def terminal(board: List[List[str]]) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    # the board is completely full
    if len(actions(board)) == 0:
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

    def recursive_minimax(board, previously_optimized=None):
        """
        Recurses down possible trees, and for each layer returns the utility and move which,
        assuming optimal plays on both sides, results in the current best outcome.
        """
        optimal_action = None
        # the game is over, no player makes a move, the utility is returned
        if terminal(board):
            return utility(board), optimal_action

        theplayer = player(board)
        # make the optimal_utility infinitely low for X (max player)
        # or infinitely high for O (min player)
        optimal_utility = float("-inf") if theplayer == X else float("inf")
        optimizer = max if theplayer == X else min

        # all actions are explored (9, then 8, then 7...)
        for action in actions(board):
            new_utility, _ = recursive_minimax(result(board, action), optimal_utility)
            # optimize for min / max
            new_optimal_utility = optimizer(optimal_utility, new_utility)

            # a more optimal action is found
            if new_optimal_utility != optimal_utility:
                optimal_action = action
                optimal_utility = new_utility

            # alpha beta pruning
            if previously_optimized:
                # if the current child player would choose one of the new explored actions
                # before what the parent is currently choosing, then stop exploring since
                # nothing new that the parent would like can be discovered
                if optimizer(previously_optimized, optimal_utility) == optimal_utility:
                    return optimal_utility, optimal_action

        return optimal_utility, optimal_action

    return recursive_minimax(board)[1]
