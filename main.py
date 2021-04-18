import pygame
import numpy as np
from modules.game import mark_square, is_available, is_completed
from modules.button import Button
from modules.minimax import best_move

# Initialize pygame and fonts
pygame.init()
pygame.font.init()

# Set screen width, height and title
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Frame rate
FPS = 60

# Colors (rgb)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (68, 68, 68)
LIGHT_BLUE = (28, 168, 252)
DARK_BLUE = (25, 73, 114)
GREEN = (0, 255, 0)
OVERLAY_COLOR = (0, 0, 0, 150)

# Set screen background color
screen.fill(DARK_BLUE)

# Draw baord
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 3
LINE_WEIGHT = 5
PADDING = 60
def draw_board():
    # Draw board background
    GRID_BACKGROUND = pygame.Rect(PADDING, PADDING, BOARD_SIZE, BOARD_SIZE)
    pygame.draw.rect(screen, WHITE, GRID_BACKGROUND)
    # Draw horizontal lines
    pygame.draw.line(screen ,BLACK, (PADDING, PADDING), (BOARD_SIZE + PADDING, PADDING), LINE_WEIGHT)
    pygame.draw.line(screen ,BLACK, (PADDING, SQUARE_SIZE + PADDING), (BOARD_SIZE + PADDING, SQUARE_SIZE + PADDING), LINE_WEIGHT)
    pygame.draw.line(screen ,BLACK, (PADDING, 2 * SQUARE_SIZE + PADDING), (BOARD_SIZE + PADDING, 2 * SQUARE_SIZE + PADDING), LINE_WEIGHT)
    pygame.draw.line(screen ,BLACK, (PADDING, BOARD_SIZE + PADDING), (BOARD_SIZE + PADDING, BOARD_SIZE + PADDING), LINE_WEIGHT)
    # Draw vertical columns
    pygame.draw.line(screen, BLACK, (PADDING, PADDING), (PADDING, BOARD_SIZE + PADDING), LINE_WEIGHT)
    pygame.draw.line(screen, BLACK, (SQUARE_SIZE + PADDING, PADDING), (SQUARE_SIZE + PADDING, BOARD_SIZE + PADDING), LINE_WEIGHT)
    pygame.draw.line(screen, BLACK, (2 * SQUARE_SIZE + PADDING, PADDING), (2 * SQUARE_SIZE + PADDING, BOARD_SIZE + PADDING), LINE_WEIGHT)
    pygame.draw.line(screen, BLACK, (BOARD_SIZE + PADDING, PADDING), (BOARD_SIZE + PADDING, BOARD_SIZE + PADDING), LINE_WEIGHT)

# Draw figures
def draw_figures(position, player):
    if player == 1:
        X_LINE_WEIGHT = 30
        X_PADDING = 50
        posX, posY = map(lambda x: x * SQUARE_SIZE + PADDING, position)
        pygame.draw.line(screen, LIGHT_BLUE, (posX + X_PADDING, posY + X_PADDING), (posX + SQUARE_SIZE - X_PADDING, posY + SQUARE_SIZE - X_PADDING), X_LINE_WEIGHT)
        pygame.draw.line(screen, LIGHT_BLUE, (posX + SQUARE_SIZE - X_PADDING, posY + X_PADDING), (posX + X_PADDING, posY + SQUARE_SIZE - X_PADDING), X_LINE_WEIGHT)
    elif player == 2:
        O_LINE_WEIGHT = 20
        O_RADUIS = 60
        posX, posY = map(lambda x: x * SQUARE_SIZE + SQUARE_SIZE // 2 + PADDING, position)
        pygame.draw.circle(screen, GREY, (posX, posY), O_RADUIS, O_LINE_WEIGHT)

# Check if the player win
def is_winner(player):
    WIN_LINE_WEIGHT = 15
    WIN_PADDING = 30
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            posY = row * SQUARE_SIZE + PADDING + SQUARE_SIZE // 2
            pygame.draw.line(screen, RED, (PADDING + WIN_PADDING, posY), (BOARD_SIZE + PADDING - WIN_PADDING, posY), WIN_LINE_WEIGHT)
            return True
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            posX = col * SQUARE_SIZE + PADDING + SQUARE_SIZE // 2
            pygame.draw.line(screen, RED, (posX, PADDING + WIN_PADDING), (posX, BOARD_SIZE + PADDING - WIN_PADDING), WIN_LINE_WEIGHT)
            return True

    # Check the main diagonal
    if board[0][0] == board[1][1] == board[2][2] == player:
        pygame.draw.line(screen, RED, (PADDING + WIN_PADDING, PADDING + WIN_PADDING), (BOARD_SIZE + PADDING - WIN_PADDING, BOARD_SIZE + PADDING - WIN_PADDING), WIN_LINE_WEIGHT)
        return True

    # Check the secondary diagonal
    if board[0][2] == board[1][1] == board[2][0] == player:
        pygame.draw.line(screen, RED, (PADDING + WIN_PADDING, BOARD_SIZE + PADDING - WIN_PADDING), (BOARD_SIZE + PADDING - WIN_PADDING, PADDING + WIN_PADDING), WIN_LINE_WEIGHT)
        return True

    return False
    
# Draw the game over state
def game_over(player):
    # Create overlay
    OVERLAY = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
    OVERLAY.fill(OVERLAY_COLOR)
    FONT = pygame.font.SysFont('comicsans', 100)
    if is_winner(player):
        # Display overlay
        screen.blit(OVERLAY, (PADDING, PADDING))
        # Display winner text
        winner_text = "Player " +str(player) + " win"
        text = FONT.render(winner_text, 1, WHITE)
        screen.blit(text, ((BOARD_SIZE - text.get_width()) // 2 + PADDING, (BOARD_SIZE - text.get_height()) // 2 + PADDING))
        score[player - 1] += 1
        pygame.display.update()
        pygame.time.wait(3000)
        return True

    if is_completed(board):
        # Display overlay
        screen.blit(OVERLAY, (PADDING, PADDING))
        # Display winner text
        draw_text = "Draw"
        text = FONT.render(draw_text, 1, WHITE)
        screen.blit(text, ((BOARD_SIZE - text.get_width()) // 2 + PADDING, (BOARD_SIZE - text.get_height()) // 2 + PADDING))
        pygame.display.update()
        pygame.time.wait(3000)
        return True

    return False

# Restart game
def restart():
    for row in range(3):
        for col in range(3):
            board[row][col] = 0
    draw_board()
    global player
    if mode == 1:
        player = 1
    else:
        player = player % 2 + 1

# Draw score
score_w = 150
score_h = 80
score_y = (HEIGHT - score_h) // 2
score_p = 30
X_score_x = (WIDTH - (BOARD_SIZE + PADDING) - (score_w * 2 + score_p)) // 2 + BOARD_SIZE + PADDING
O_score_x = X_score_x + score_w + score_p
def draw_score(player):
    figure_p = 15
    FONT = pygame.font.SysFont('comicsansms', 50)

    # First player score
    x_rect = pygame.Rect(X_score_x, score_y, score_w, score_h)
    pygame.draw.rect(screen, WHITE, x_rect)
    # Draw figure
    X_LINE_WEIGHT = 10
    pygame.draw.line(screen, LIGHT_BLUE, (X_score_x + figure_p, score_y + figure_p), (X_score_x + score_h - figure_p, score_y + score_h - figure_p), X_LINE_WEIGHT)
    pygame.draw.line(screen, LIGHT_BLUE, (X_score_x + figure_p, score_y + score_h - figure_p), (X_score_x + score_h - figure_p, score_y + figure_p), X_LINE_WEIGHT)
    # Draw score
    X_score = FONT.render(":" + str(score[0]), 1, DARK_BLUE)
    screen.blit(X_score, (X_score_x + (score_w -  score_h) + (score_h - X_score.get_width()) // 2, score_y + (score_h - X_score.get_height()) // 2))

    # Second player score
    o_rect = pygame.Rect(O_score_x, score_y, score_w, score_h)
    pygame.draw.rect(screen, WHITE, o_rect)
    # Draw figure
    O_LINE_WEIGHT = 8
    O_RADIUS = 30
    pygame.draw.circle(screen, GREY, (O_score_x + score_w - score_h // 2, score_y + score_h // 2), O_RADIUS, O_LINE_WEIGHT)
    # Draw score
    O_score = FONT.render(str(score[1]) + ":", 1, DARK_BLUE)
    screen.blit(O_score, (O_score_x + (score_h - O_score.get_width()) // 2, score_y + (score_h - O_score.get_height()) // 2))
    
    # Player turn
    if player == 1:
        pygame.draw.rect(screen, RED, x_rect, 5)
        pygame.draw.rect(screen, WHITE, o_rect, 5)
    elif player == 2:
        pygame.draw.rect(screen, RED, o_rect, 5)
        pygame.draw.rect(screen, WHITE, x_rect, 5)

# Restart game button
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100
BUTTON_X = (WIDTH - (BOARD_SIZE + PADDING) - BUTTON_WIDTH) // 2 + BOARD_SIZE + PADDING
BUTTON_Y = 400 + PADDING
restart_game = Button(screen, BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "Restart game", restart)

# Change mode
def change_mode(new_mode):
    global mode
    if new_mode == mode:
        return None
    mode = new_mode # Change mode
    # Clear board
    for row in range(3):
        for col in range(3):
            board[row][col] = 0
    draw_board()
    score[0], score[1] = 0, 0 # Reset score
    global player
    player = 1

# Draw change mode buttons
mode_w = 150
mode_h = 80
mode_y = 100 + PADDING
mode_p = 30
first_mode_x = (WIDTH - (BOARD_SIZE + PADDING) - (mode_w * 2 + mode_p)) // 2 + BOARD_SIZE + PADDING
second_mode_x = first_mode_x + mode_w + mode_p
def draw_mode():
    FONT = pygame.font.SysFont('comicsansms', 30)
    # First player score
    first_mode_rect = pygame.Rect(first_mode_x, mode_y, mode_w, mode_h)
    pygame.draw.rect(screen, WHITE, first_mode_rect)
    # Draw score
    first_mode = FONT.render("1 vs AI", 1, BLACK)
    screen.blit(first_mode, (first_mode_x + (mode_w - first_mode.get_width()) // 2, mode_y + (mode_h - first_mode.get_height()) // 2))

    # Second player score
    second_mode_rect = pygame.Rect(second_mode_x, mode_y, mode_w, mode_h)
    pygame.draw.rect(screen, WHITE, second_mode_rect)
    # Draw score
    second_mode = FONT.render("1 vs 1", 1, BLACK)
    screen.blit(second_mode, (second_mode_x + (score_w - second_mode.get_width()) // 2, mode_y + (score_h - second_mode.get_height()) // 2))
    
    # Player turn
    if mode == 1:
        pygame.draw.rect(screen, GREEN, first_mode_rect, 5)
        pygame.draw.rect(screen, WHITE, second_mode_rect, 5)
    elif mode == 2:
        pygame.draw.rect(screen, GREEN, second_mode_rect, 5)
        pygame.draw.rect(screen, WHITE, first_mode_rect, 5)

def click(position):
    restart_game.click(position)
    posX, posY = position
    if first_mode_x <= posX <= first_mode_x + mode_w and mode_y <= posY <= mode_y + mode_h:
        change_mode(1)
        draw_mode()
    elif second_mode_x <= posX <= second_mode_x + mode_w and mode_y <= posY <= mode_y + mode_h:
        change_mode(2)
        draw_mode()

def hover(position):
    restart_game.hover(position)

# Main function
def main():
    draw_board()
    draw_mode()
    global player
    restart_game.draw_button()
    clock = pygame.time.Clock()
    quit = False
    while not quit:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if mode == 1 and player == 2:
                pygame.display.update()
                move = best_move(board)
                draw_figures(move, player)
                if game_over(player):
                    restart()
                player = 1
            hover_position = pygame.mouse.get_pos()
            hover(hover_position)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_position = pygame.mouse.get_pos()
                click(click_position)
                posX, posY = map(lambda x: (x - PADDING) // SQUARE_SIZE, click_position)
                position = (posX, posY)
                if is_available(board, position):
                    draw_figures(position, player)
                    mark_square(board, position, player)
                    if game_over(player):
                        restart()
                        continue
                    player = player % 2 + 1
        
        pygame.display.update()
        draw_score(player)

    pygame.quit()

if __name__ == "__main__":
    board = np.zeros((3, 3)) # Initialize board
    start_player = 1 # Initialize start player
    player = start_player
    score = [0, 0] # Initialize score
    mode = 1 # Initialize mode
    main()
