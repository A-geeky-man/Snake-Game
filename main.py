import pygame
from pygame import mixer
import sys
import random

# Initializing pygame
pygame.init()

screen = pygame.display.set_mode((400, 400))

# Icon and Caption
pygame.display.set_caption('SNAKE')
icon = pygame.image.load('icon_32.png')
pygame.display.set_icon(icon)

# Snake details
x_snake = 200
y_snake = 20
x_snake_change = 0
y_snake_change = 0
snake_list = []
length_of_snake = 1

# Food details
x_food = random.randint(0, 19)
y_food = random.randint(0, 19)

clock = pygame.time.Clock()

# Game Over Text
over_font = pygame.font.Font('NaughtyMonster.ttf', 20)

# Score
score_font = pygame.font.Font('freesansbold.ttf', 32)


'''def draw_grid():
    block_size = 20
    for i in range(400):
        for j in range(400):
            grid = pygame.Rect(i * block_size, j * block_size, block_size, block_size)
            pygame.draw.rect(screen, (200, 200, 200), grid, 1)'''


# Food
def draw_food(x_food, y_food):
    food = pygame.Rect(x_food * 20, y_food * 20, 20, 20)
    pygame.draw.rect(screen, (0, 255, 0), food)


# Snake
def draw_snake(snake_list):
    for coordinate in snake_list:
        snake = pygame.Rect(coordinate[0], coordinate[1], 20, 20)
        pygame.draw.rect(screen, (255, 0, 0), snake)


def game_over(msg):
    over_text = over_font.render(msg, True, (255, 255, 255))
    screen.blit(over_text, (60, 200))


def score(message):
    score_text = score_font.render(message, True, (255, 255, 255))
    screen.blit(score_text, (100, 240))


# Game Loop
def main():
    global x_snake_change, y_snake_change, x_snake, y_snake, length_of_snake, snake_list, x_food, y_food
    running = True
    game_close = False
    l, r, u, d = 0, 0, 0, 0    # To maintain the jumping of the snake as player press same arrow button more than once
    lr, ud = True, True        # To maintain the game_over condition if player press the opposite arrow button.
    points = 0
    while running:
        screen.fill((0, 0, 0))

        while game_close:
            screen.fill((0, 0, 255))
            game_over('You lost! Press C-Play again, Q-Quit')
            score(f"Score : {str(points)}")

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        # Snake details
                        x_snake = 200
                        y_snake = 20
                        x_snake_change = 0
                        y_snake_change = 0
                        snake_list = []
                        length_of_snake = 1
                        main()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        for event in pygame.event.get():
            # To quit the game
            if event.type == pygame.QUIT:
                running = False

            # To control the snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    l += 1
                    r, u, d = 0, 0, 0
                    ud = True
                    if l > 1 or not lr:
                        pass
                    else:
                        x_snake_change -= 20
                        y_snake_change = 0
                    lr = False
                elif event.key == pygame.K_RIGHT:
                    r += 1
                    l, u, d = 0, 0, 0
                    ud = True
                    if r > 1 or not lr:
                        pass
                    else:
                        x_snake_change += 20
                        y_snake_change = 0
                    lr = False
                elif event.key == pygame.K_UP:
                    u += 1
                    r, l, d = 0, 0, 0
                    lr = True
                    if u > 1 or not ud:
                        pass
                    else:
                        y_snake_change -= 20
                        x_snake_change = 0
                    ud = False
                elif event.key == pygame.K_DOWN:
                    d += 1
                    r, u, l = 0, 0, 0
                    lr = True
                    if d > 1 or not ud:
                        pass
                    else:
                        y_snake_change += 20
                        x_snake_change = 0
                    ud = False

        # draw_grid()
        draw_food(x_food, y_food)

        x_snake += x_snake_change
        y_snake += y_snake_change
        # Condition if Snake crosses boundary of screen - Sanke comes from the other side
        if x_snake > 380:
            x_snake = 0
        if x_snake < 0:
            x_snake = 380
        if y_snake > 380:
            y_snake = 0
        if y_snake < 0:
            y_snake = 380

        # Condition if Snake crosses boundary of screen - Game Over
        '''if x_snake > 380 or x_snake < 0 or y_snake > 380 or y_snake < 0:
            game_over_sound = mixer.Sound('game_over.wav')
            game_over_sound.play()
            game_close = True'''

        snake_head = []
        snake_head.append(x_snake)
        snake_head.append(y_snake)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]
        draw_snake(snake_list)

        for x in snake_list[:-1]:
            if x == snake_head:
                game_over_sound = mixer.Sound('game_over.wav')
                game_over_sound.play()
                game_close = True

        if x_snake == x_food * 20 and y_snake == y_food * 20:
            hit_sound = mixer.Sound('hit.wav')
            hit_sound.play()
            x_food = random.randint(0, 19)
            y_food = random.randint(0, 19)
            length_of_snake += 1
            points += 1

        clock.tick(10)
        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
