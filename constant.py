SCREEN_LENGTH = 400
GRID_LENGTH = 20
GRID_RATIO = SCREEN_LENGTH / GRID_LENGTH
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
MOVES = {
    "UP": UP,
    "DOWN": DOWN,
    "RIGHT": RIGHT,
    "LEFT": LEFT
}
CARDINAL_DIRECTIONS = list(MOVES.values()) + [(1, -1), (1, 1), (-1, 1), (-1, -1)]
ACTIONS = dict((action, name[1]) for name, action in MOVES.items())
