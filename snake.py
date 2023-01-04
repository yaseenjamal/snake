import math
import sys
import random

import pygame

from constant import ACTIONS, SCREEN_LENGTH, CARDINAL_DIRECTIONS, GRID_LENGTH, UP, DOWN, RIGHT, LEFT


def euclidean_distance(start_point, end_point):
    return math.sqrt(pow(start_point[0] - end_point[0], 2) + pow(start_point[1] - end_point[1], 2))


class Snake:
    def __init__(self):
        self.length = 3
        self.direction = random.choice(list(ACTIONS.keys()))
        self.positions = [((SCREEN_LENGTH / 2), (SCREEN_LENGTH / 2))]
        self.color = (192, 192, 192)

    def head(self):
        return self.positions[0]

    def observe_environment(self, food):
        data = []
        for direction in CARDINAL_DIRECTIONS:
            view = []
            point = (self.head()[0] + direction[0] * GRID_LENGTH, self.head()[1] + direction[1] * GRID_LENGTH)
            while 0 <= point[0] <= SCREEN_LENGTH and 0 <= point[1] <= SCREEN_LENGTH:
                view.append(point)
                point = (point[0] + direction[0] * GRID_LENGTH, point[1] + direction[1] * GRID_LENGTH)
            if food in view:
                data.append(euclidean_distance(self.head(), food.position) / GRID_LENGTH)
            else:
                data.append(0)
            found = False
            for bit in self.positions[1:]:
                if bit in view:
                    found = True
                    data.append(euclidean_distance(bit, self.head()) / GRID_LENGTH)
                    break
            if not found:
                data.append(0)
            data.append(len(view))
        return data

    def turn(self, point):
        if not (self.length > 1 and (-point[0], -point[1]) == self.direction):
            self.direction = point

    def move(self):
        current_position = self.head()

        x, y = self.direction
        new_position = (
            (current_position[0] + (x * GRID_LENGTH)),
            (current_position[1] + (y * GRID_LENGTH))
        )
        if len(self.positions) > 2 and new_position in self.positions[2:]:
            return False
        else:
            self.positions.insert(0, new_position)
            if self.head()[0] >= SCREEN_LENGTH \
                    or self.head()[0] < 0 \
                    or self.head()[1] >= SCREEN_LENGTH \
                    or self.head()[1] < 0:
                return False
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 3
        self.direction = random.choice([UP, DOWN, RIGHT, LEFT])
        self.positions = [((SCREEN_LENGTH / 2), (SCREEN_LENGTH / 2))]
        self.positions.append((self.positions[0] + self.direction[0], self.positions[1] + self.direction[1]))

    def draw(self, plane):
        for position in self.positions:
            cell = pygame.Rect((position[0], position[1]), (GRID_LENGTH, GRID_LENGTH))
            pygame.draw.rect(plane, self.color, cell)
            pygame.draw.rect(plane, (192, 192, 192), cell, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.exit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
