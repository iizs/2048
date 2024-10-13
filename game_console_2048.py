import sys
import pygame
import datetime
from game_of_2048 import GameOf2048


BLACK = 0, 0, 0
WHITE = 255, 255, 255
COLOR_BOARD = 200, 200, 200
COLOR_NUM = {
    0: (0, 0, 0),
    2: (255, 207, 218),
    4: (255, 218, 185),
    8: (253, 253, 150),
    16: (179, 238, 232),
    32: (189, 252, 201),
    64: (230, 230, 250),
    128: (255, 182, 193),
    256: (255, 180, 159),
    512: (255, 239, 104),
    1024: (173, 216, 230),
    2048: (152, 251, 152),
    4096: (221, 160, 221),
    8192: (174, 226, 232),
}


class GameConsole2048:
    def __init__(self):
        pygame.init()

        # Display attributes
        self._display_size_ = self.display_width, self.display_height = 1280, 960
        self._screen_background_color_ = BLACK
        self._information_text_font_name_ = 'Roboto'
        self._information_text_font_size_ = 24
        self._information_text_font_color_ = WHITE
        self._tile_size_ = 150
        self._tile_text_font_name_ = 'Roboto'
        self._tile_text_font_size_ = 64
        self._tile_text_font_color_ = WHITE

        # main instances
        self._screen_ = pygame.display.set_mode(self._display_size_)
        self._game_ = GameOf2048()
        self._information_text_font_ = pygame.font.SysFont(
            self._information_text_font_name_,
            self._information_text_font_size_
        )
        self._tile_text_font_ = pygame.font.SysFont(
            self._tile_text_font_name_,
            self._tile_text_font_size_
        )

    def update_screen(self):
        self._screen_.fill(self._screen_background_color_)

        score_text = self._information_text_font_.render(
            f"Score: {self._game_.score}",
            True,
            self._information_text_font_color_
        )
        score_text_rect = score_text.get_rect()
        score_text_rect.left = 10
        score_text_rect.top = 10

        time_text = self._information_text_font_.render(
            f"Elapsed Time: {datetime.datetime.now() - self._game_.start_time}",
            True,
            self._information_text_font_color_
        )
        time_text_rect = time_text.get_rect()
        time_text_rect.left = 10
        time_text_rect.top = 10 + score_text_rect.height + 10

        self._screen_.blit(score_text, score_text_rect)
        self._screen_.blit(time_text, time_text_rect)

        for x in range(GameOf2048.BOARD_SIZE):
            for y in range(GameOf2048.BOARD_SIZE):
                num = self._game_.get_tile(x, y)
                if num is not None and num != 0:
                    num_text = self._tile_text_font_.render(f"{num}", True, BLACK)
                    if num in COLOR_NUM:
                        tile_color = COLOR_NUM[num]
                    else:
                        tile_color = COLOR_BOARD
                else:
                    num_text = None
                    tile_color = COLOR_BOARD

                pygame.draw.rect(
                    self._screen_,
                    tile_color,
                    pygame.Rect(
                        self._tile_size_ + x * (self._tile_size_ + 10),
                        self._tile_size_ + y * (self._tile_size_ + 10),
                        self._tile_size_,
                        self._tile_size_
                    )
                )

                if num_text is not None:
                    num_text_rect = num_text.get_rect()
                    num_text_rect.left = self._tile_size_ + x * (self._tile_size_ + 10) + 10
                    num_text_rect.top = self._tile_size_ + y * (self._tile_size_ + 10) + 10
                    self._screen_.blit(num_text, num_text_rect)

        pygame.display.flip()

    def run(self):
        wait = True
        while wait:
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self._game_.move(GameOf2048.Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self._game_.move(GameOf2048.Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self._game_.move(GameOf2048.Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self._game_.move(GameOf2048.Direction.RIGHT)
