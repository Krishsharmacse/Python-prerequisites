# Import necessary libraries
import pygame
import random
import sys

# **Game Initialization**
pygame.init()

# **Game Constants**
red = (255, 0, 0)  # Color red
black = (0, 0, 0)  # Color black
white = (255, 255, 255)  # Color white
blue = (0, 0, 255)  # Color blue for the paused screen
green = (0, 255, 0)  # Color green for the snake
screen_width = 1200  # Screen width
screen_height = 600  # Screen height
fps = 30  # Frames per second
init_velocity = 12  # Initial snake speed

# **Game Variables**
snake_X = 100  # Initial snake x position
snake_Y = 100  # Initial snake y position
snake_size = 15  # Snake size
velocity_x = 0  # Initial snake velocity x
velocity_y = 0  # Initial snake velocity y
food_x = random.randint(0, screen_width - snake_size)  # Initial food x position
food_y = random.randint(0, screen_height - snake_size)  # Initial food y position
exit_game = False  # Game exit flag
game_over = False  # Game over flag
paused = False  # Game paused flag
score = 0  # Initial score
high_score = 0  # Highest score
snake_length = 1  # Initial snake length
snake_list = []  # Snake position list

# **Game Window**
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kisu Bhaiya Ka SAAP")

# **Game Clock**
clock = pygame.time.Clock()

# **Font and Display**
font = pygame.font.SysFont(None, 55)

def show_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# **Draw Snake**
def draw_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# **Pause Function**
def pause_game():
    global paused
    paused = True
    gameWindow.fill(blue)
    show_text("Game Paused - Press 'P' to Resume", white, 250, 250)
    pygame.display.update()

    # Wait for the player to resume the game
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

# **Game Loop**
while not exit_game:
    if game_over:
        # Display game over screen
        gameWindow.fill(white)
        show_text("Game Over! Press Space to Restart", red, 250, 250)
        show_text(f"Score: {score}", black, 250, 300)
        show_text(f"High Score: {high_score}", black, 250, 350)
        pygame.display.update()

        #  for restarting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset game variables for restarting
                    snake_X = 100
                    snake_Y = 100
                    velocity_x = 0
                    velocity_y = 0
                    food_x = random.randint(0, screen_width - snake_size)
                    food_y = random.randint(0, screen_height - snake_size)
                    score = 0
                    snake_length = 1
                    snake_list = []
                    game_over = False

    else:
        # Event handling for snake movement and pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    velocity_x = init_velocity
                    velocity_y = 0
                if event.key == pygame.K_LEFT:
                    velocity_x = -init_velocity
                    velocity_y = 0
                if event.key == pygame.K_UP:
                    velocity_y = -init_velocity
                    velocity_x = 0
                if event.key == pygame.K_DOWN:
                    velocity_y = init_velocity
                    velocity_x = 0
                if event.key == pygame.K_p:
                    pause_game()  # Pause the game when 'P' is pressed

        # **Snake Movement**
        snake_X = snake_X + velocity_x
        snake_Y = snake_Y + velocity_y

        # **Boundary Collision**
        if snake_X < 0 or snake_X > screen_width or snake_Y < 0 or snake_Y > screen_height:
            game_over = True

        # **Food Collision**
        if abs(snake_X - food_x) < snake_size and abs(snake_Y - food_y) < snake_size:
            score += 1
            snake_length += 1
            food_x = random.randint(0, screen_width - snake_size)
            food_y = random.randint(0, screen_height - snake_size)

            # Update high score
            if score > high_score:
                high_score = score

            # Increase speed as the score increases
            if score % 5 == 0:
                init_velocity += 1  # Snake gets faster

        # **Snake Update**
        snake_list.append([snake_X, snake_Y])
        if len(snake_list) > snake_length:
            del snake_list[0]

        # **Self Collision**
        for block in snake_list[:-1]:
            if block == [snake_X, snake_Y]:
                game_over = True

        # **Game Window Update**
        gameWindow.fill(white)
        show_text(f"Score: {score}  High Score: {high_score}", black, 5, 5)
        pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
        draw_snake(gameWindow, green, snake_list, snake_size)

    pygame.display.update()
    clock.tick(fps)

# **Quit Game**
pygame.quit()
sys.exit()
