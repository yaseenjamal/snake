import numpy as np

import torch
import random
import torch.nn as nn
import torch.nn.functional as F

from game import play

MOVES = {
    0: "DOWN",
    1: "LEFT",
    2: "RIGHT",
    3: "UP"
}


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.layers = [nn.Linear(24, 18), nn.Linear(18, 18), nn.Linear(18, 4), nn.Linear(4, 4)]
        self.fitness = 0

    def update_fitness(self):
        steps, score = play(self, float("inf"))
        self.fitness = score + steps * 0.01

    def forward(self, inputs):
        for layer in self.layers[:-1]:
            inputs = torch.relu(layer(inputs))
        return F.softmax(self.layers[-1](inputs), dim=1)

    def think(self, observations):
        inputs = torch.tensor(observations).float().view(-1, 24)
        output = self.forward(inputs)
        move = np.argmax(output.tolist())
        return MOVES.get(move)

    def decode(self):
        weights = []
        biases = []
        for layer in self.layers:
            weights.extend(layer.weight.data.numpy().tolist())
            biases.extend(layer.bias.data.numpy().tolist())
        return weights, biases

    def encode(self, weights, bias):
        for layer in self.layers:
            layer.weight.data = torch.Tensor([weights.pop(0) for _ in range(len(layer.weight.data.numpy()))]).view(
                layer.weight.shape)
            layer.bias.data = torch.Tensor([bias.pop(0) for _ in range(len(layer.bias.data.numpy()))]).view(
                layer.bias.shape)

    def mutate(self, chance):
        weights, bias = self.decode()
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                if random.randint(0, chance) == chance:
                    weights[i][j] += np.random.uniform(-1, 1)
        for i in range(len(bias)):
            if random.randint(0, chance) == chance:
                bias[i] += np.random.uniform(-1, 1)
        self.encode(weights, bias)
