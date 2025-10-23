if abs(snake_X - food_x) < snake_size and abs(snake_Y - food_y) < snake_size:
            score += 1
            snake_length += 1
            food_x = random.randint(0, screen_width - snake_size)
            food_y = random.randint(0, screen_height - snake_size)