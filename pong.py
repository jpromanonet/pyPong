import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
FPS = 60
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Pong")

# Initialize game variables
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [2 * random.choice((1, -1)), 2 * random.choice((1, -1))]
player_pos = [0, HEIGHT // 2 - PADDLE_HEIGHT // 2]
computer_pos = [WIDTH - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2]
paddle_speed = 5

# Scores
player_score = 0
computer_score = 0

# Game state
game_over = False

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Check if the game is over
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Reset the game
            game_over = False
            player_score = 0
            computer_score = 0
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_speed = [2 * random.choice((1, -1)), 2 * random.choice((1, -1))]

    # If the game is not over, update the game
    if not game_over:
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= paddle_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - PADDLE_HEIGHT:
            player_pos[1] += paddle_speed

        # Computer AI
        if computer_pos[1] + PADDLE_HEIGHT / 2 < ball_pos[1]:
            computer_pos[1] += paddle_speed
        elif computer_pos[1] + PADDLE_HEIGHT / 2 > ball_pos[1]:
            computer_pos[1] -= paddle_speed

        # Update ball position
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # Ball collisions
        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_RADIUS:
            ball_speed[1] = -ball_speed[1]

        if (
            player_pos[0] <= ball_pos[0] <= player_pos[0] + PADDLE_WIDTH
            and player_pos[1] <= ball_pos[1] <= player_pos[1] + PADDLE_HEIGHT
        ) or (
            computer_pos[0] <= ball_pos[0] <= computer_pos[0] + PADDLE_WIDTH
            and computer_pos[1] <= ball_pos[1] <= computer_pos[1] + PADDLE_HEIGHT
        ):
            ball_speed[0] = -ball_speed[0]

        # Check for scoring
        if ball_pos[0] <= 0:
            computer_score += 1
            if computer_score == 21:
                game_over = True
        elif ball_pos[0] >= WIDTH - BALL_RADIUS:
            player_score += 1
            if player_score == 21:
                game_over = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, pygame.Rect(player_pos[0], player_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, pygame.Rect(computer_pos[0], computer_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2))

    # Draw the middle line
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)

    # Draw scores
    player_text = FONT.render("Player: " + str(player_score), True, WHITE)
    computer_text = FONT.render("Computer: " + str(computer_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 10))
    screen.blit(computer_text, (3 * WIDTH // 4 - 20, 10))

    # Draw game-over screen if the game is over
    if game_over:
        winner_text = FONT.render("Player wins!" if player_score == 21 else "Computer wins!", True, WHITE)
        game_over_text = FONT.render("Game Over. Press SPACE to play again.", True, WHITE)
        screen.blit(winner_text, (WIDTH // 4, HEIGHT // 2 - 20))
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2 + 20))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
