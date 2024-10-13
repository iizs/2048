from enum import IntEnum, Enum
import datetime
import random


class GameOf2048:
    class Status(Enum):
        IN_PLAY = 1
        GAME_END = 2

    class Direction(IntEnum):
        LEFT = 0
        DOWN = 1
        RIGHT = 2
        UP = 3

    BOARD_SIZE = 4
    EMPTY_BOARD = [None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None]
    COLOR_TEST_BOARD = [2, 4, 8, 16,
                        32, 64, 128, 256,
                        512, 1024, 2048, 4096,
                        8192, None, None, None]
    # 0 1 2 3        c 8 4 0
    # 4 5 6 7   =>   d 9 5 1
    # 8 9 a b        e a 6 2
    # c d e f        f b 7 3
    INDEX_ROTATE_CLOCKWISE = [12, 8, 4, 0, 13, 9, 5, 1, 14, 10, 6, 2, 15, 11, 7, 3]

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
        self.game_board = list(self.EMPTY_BOARD)
        self.spawn_new_tile()
        self.spawn_new_tile()

    def move(self, direction):
        board = list(self.game_board)
        for i in range(direction):
            board = GameOf2048.rotate_clockwise(board)
        board, score_up = GameOf2048.push_left(board)
        for i in range(GameOf2048.BOARD_SIZE - direction):
            board = GameOf2048.rotate_clockwise(board)
        if board != self.game_board:
            self.score += score_up
            self.game_board = board
            self.spawn_new_tile()
            if not self.has_more_move():
                print("No more move")

    def has_more_move(self):
        board = list(self.game_board)
        for i in range(GameOf2048.BOARD_SIZE):
            prev_board = list(board)
            next_board = GameOf2048.push_left(prev_board)
            if prev_board != next_board:
                return True
            board = GameOf2048.rotate_clockwise(board)
        return False

    @staticmethod
    def rotate_clockwise(board):
        # 0 1 2 3        c 8 4 0
        # 4 5 6 7   =>   d 9 5 1
        # 8 9 a b        e a 6 2
        # c d e f        f b 7 3
        new_board = []
        for idx in GameOf2048.INDEX_ROTATE_CLOCKWISE:
            new_board.append(board[idx])
        return new_board

    @staticmethod
    def push_left_one_row(row):
        idx = 0
        score_up = 0
        while idx < GameOf2048.BOARD_SIZE:
            if row[idx] is None:
                all_none = True
                for idx_2 in range(idx+1, GameOf2048.BOARD_SIZE):
                    if row[idx_2] is not None:
                        row[idx] = row[idx_2]
                        row[idx_2] = None
                        all_none = False
                        break
                if all_none:
                    idx += 1
            else:
                for idx_2 in range(idx + 1, GameOf2048.BOARD_SIZE):
                    if row[idx_2] is None:
                        continue
                    elif row[idx_2] == row[idx]:
                        row[idx] += row[idx_2]
                        row[idx_2] = None
                        score_up += row[idx]
                        break
                    else:  # row[idx_2] != row[idx]
                        break
                idx += 1
        return row, score_up

    @staticmethod
    def push_left(board):
        new_board = []
        score_up = 0
        for r in range(GameOf2048.BOARD_SIZE):
            new_row, score = GameOf2048.push_left_one_row(board[r * 4:(r + 1) * 4])
            new_board.extend(new_row)
            score_up += score
        return new_board, score_up

    def get_tile(self, x, y):
        if x < GameOf2048.BOARD_SIZE and y < GameOf2048.BOARD_SIZE:
            return self.game_board[x + GameOf2048.BOARD_SIZE * y]
        else:
            return None

    def spawn_new_tile(self):
        value = 4 if random.random() > 0.9 else 2
        empty_tiles = []
        for i in range(len(self.game_board)):
            if self.game_board[i] is None:
                empty_tiles.append(i)
        random.shuffle(empty_tiles)
        self.game_board[empty_tiles[0]] = value
