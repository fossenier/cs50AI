import pygame
import sys
import time

HEIGHT = 8
WIDTH = 8
MINES = 8

# Colors.
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)


class Life(object):
    def __init__(self) -> None:
        self.board = [[False] * WIDTH] * HEIGHT


# Create game.
pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
game = Life()

# Default font.
font = pygame.font.Font(None, 26)

# Compute board size.
BOARD_PADDING = 20
board_width = width - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

while True:
    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Draw board.
    cells = []
    for i, board_row in enumerate(game.board):
        row = []
        for j, board_cell in enumerate(board_row):

            # Draw rectangle for cell.
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            row.append(rect)
        cells.append(row)

    left, _, right = pygame.mouse.get_pressed()
    # Check for a right-click or left-click
    if right == 1 or left == 1:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse):
                    game.board
                    time.sleep(0.2)
