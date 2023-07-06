import pygame

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
SQUARE_SIZE = HEIGHT // BOARD_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game state
board = [
    ["", "b", "", "b", "", "b", "", "b"],
    ["b", "", "b", "", "b", "", "b", ""],
    ["", "b", "", "b", "", "b", "", "b"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["r", "", "r", "", "r", "", "r", ""],
    ["", "r", "", "r", "", "r", "", "r"],
    ["r", "", "r", "", "r", "", "r", ""],
]

selected_piece = None
possible_moves = []

# Helper function to get possible moves for a piece
def get_possible_moves(row, col):
    moves = []

    piece = board[row][col]
    if piece == "":
        return moves

    if piece == "r":
        directions = [(1, -1), (1, 1)]
    elif piece == "b":
        directions = [(-1, -1), (-1, 1)]
    else:
        return moves

    for dir in directions:
        dx, dy = dir
        new_row, new_col = row + dx, col + dy
        capture_row, capture_col = row + 2 * dx, col + 2 * dy

        if (
            0 <= new_row < BOARD_SIZE
            and 0 <= new_col < BOARD_SIZE
            and board[new_row][new_col] == ""
        ):
            moves.append((new_row, new_col))

        if (
            0 <= capture_row < BOARD_SIZE
            and 0 <= capture_col < BOARD_SIZE
            and board[new_row][new_col] != ""
            and board[new_row][new_col].lower() != piece
            and board[capture_row][capture_col] == ""
        ):
            moves.append((capture_row, capture_col))

    return moves

# Game loop
running = True
current_player = "r"  # Red player starts
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    if selected_piece is None:
        # Piece selection
        if keys[pygame.K_SPACE]:
            col = pygame.mouse.get_pos()[0] // SQUARE_SIZE
            row = pygame.mouse.get_pos()[1] // SQUARE_SIZE

            piece = board[row][col]
            if piece != "" and piece.lower() == current_player:
                selected_piece = (row, col)
                possible_moves = get_possible_moves(row, col)
    else:
        # Move piece
        if keys[pygame.K_SPACE]:
            col = pygame.mouse.get_pos()[0] // SQUARE_SIZE
            row = pygame.mouse.get_pos()[1] // SQUARE_SIZE

            if (row, col) in possible_moves:
                # Move the piece
                board[row][col] = board[selected_piece[0]][selected_piece[1]]
                board[selected_piece[0]][selected_piece[1]] = ""
                selected_piece = None
                possible_moves = []

                # Switch player turn
                current_player = "b" if current_player == "r" else "r"

    # Draw the board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(SCREEN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board[row][col]
            if piece == "r":
                pygame.draw.circle(SCREEN, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 10)
            elif piece == "b":
                pygame.draw.circle(SCREEN, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 10)

            # Draw possible move indicators
            if (row, col) in possible_moves:
                pygame.draw.circle(SCREEN, (0, 255, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   10)

    pygame.display.flip()

# Quit the game
pygame.quit()
 