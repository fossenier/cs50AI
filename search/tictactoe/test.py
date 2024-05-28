import tictactoe as ttt


X = "X"
O = "O"
EMPTY = None

# XOX
# XOO
#
board = [[X, O, X], [X, O, O], [None, None, None]]

result = ttt.minimax(board)
result_1 = ttt.terminal(board)
print(result)
print(result_1)
