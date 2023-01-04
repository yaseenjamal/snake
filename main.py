import argparse

import torch

import hyperparameter
import game
from genetic_evolution import genetic_evolution

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snake")
    parser.add_argument("-p", "--play", help="play as a human", action="store_true")
    parser.add_argument("-e", "--evolve", help="evolve a new model", action="store_true")
    parser.add_argument("-t", "--test", help="test a pre-trained model")

    args = vars(parser.parse_args())
    if args.get("play"):
        game.play(None, hyperparameter.playing_speed)
    elif args.get("evolve"):
        evolved_model = genetic_evolution(hyperparameter.population_size, hyperparameter.generations)
    elif args.get("test"):
        model = torch.load(args.get("test"))
        game.play(model, hyperparameter.playing_speed)
    else:
        parser.print_help()
