from enum import Enum
import datetime


class GameOf2048:
    class Status(Enum):
        IN_PLAY = 1
        GAME_END = 2

    class Direction(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    def __init__(self):
        self.status = GameOf2048.Status.IN_PLAY

        # in game variables
        self.game_board = None
        self.start_time = None
        self.score = None

        self.reset()

    def reset(self):
        self.score = 0
        self.start_time = datetime.datetime.now()
        self.game_board = [0, 2, 4, 8,
                           16, 32, 64, 128,
                           256, 512, 1024, 2048,
                           4096, 8192, 16384, None]

    def move(self, direction):
        pass

    def get_tile(self, x, y):
        if x < 4 and y < 4:
            return self.game_board[x + 4 * y]
        else:
            return None
