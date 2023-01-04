import random

import pygame

from constant import GRID_RATIO, GRID_LENGTH


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 102, 102)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, int(GRID_LENGTH - 1)) * GRID_RATIO,
            random.randint(0, int(GRID_LENGTH - 1)) * GRID_RATIO
        )

    def draw(self, plane):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_LENGTH, GRID_LENGTH))
        pygame.draw.rect(plane, self.color, r)
        pygame.draw.rect(plane, (255, 102, 102), r, 1)
