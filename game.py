import pygame

from constant import GRID_LENGTH, GRID_RATIO, SCREEN_LENGTH, ACTIONS, MOVES
from food import Food
from snake import Snake


def draw_grid(plane):
    for y in range(0, int(GRID_RATIO)):
        for x in range(0, int(GRID_RATIO)):
            square = pygame.Rect((x * GRID_LENGTH, y * GRID_LENGTH), (GRID_LENGTH, GRID_LENGTH))
            pygame.draw.rect(plane, (0, 0, 0), square)


def play(agent, speed):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_LENGTH))
    surface = pygame.Surface(screen.get_size()).convert()
    draw_grid(surface)
    snake, food = Snake(), Food()
    score, steps = [0 for _ in range(2)]
    lifespan = 100  # Prevent evolving models from looping in circles.
    while True:
        pygame.display.update()
        clock.tick(speed)
        if lifespan <= 0 and agent is not None:
            return steps, score
        input_layer = snake.observe_environment(food)
        steps += 1
        lifespan -= 1
        if agent is None:
            snake.handle_keys()
            input_layer.append(ACTIONS[snake.direction])
        else:
            move = agent.think(input_layer)
            snake.turn(MOVES.get(move))
        draw_grid(surface)
        if not snake.move():
            return steps, score
        if snake.head() == food.position:
            snake.length += 1
            score += 1
            lifespan += 20
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = pygame.font.SysFont("Calibri", 14).render("Score: {0}".format(score), True, (255, 255, 255))
        screen.blit(text, (5, 10))
        pygame.display.update()
