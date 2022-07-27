import sys
import pygame
import datetime
from game_of_2048 import GameOf2048


BLACK = 0, 0, 0
WHITE = 255, 255, 255
COLOR_BOARD = 200, 200, 200
COLOR_NUM = {
    0: (0, 0, 0),
    2: (190, 190, 190),
    4: (180, 180, 180),
    8: (170, 170, 170),
    16: (160, 160, 160),
    32: (150, 150, 150),
    64: (140, 140, 140),
    128: (130, 130, 130),
    256: (120, 120, 120),
    512: (110, 110, 110),
    1024: (100, 100, 100),
    2048: (90, 90, 90),
    4096: (80, 80, 80),
    8192: (70, 70, 70),
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

        # main instances
        self._screen_ = pygame.display.set_mode(self._display_size_)
        self._game_ = GameOf2048()
        self._information_text_font_ = pygame.font.SysFont(
            self._information_text_font_name_,
            self._information_text_font_size_
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

        for x in range(4):
            for y in range(4):
                num = self._game_.get_tile(x, y)
                if num is not None and num != 0:
                    num_text = self._information_text_font_.render(f"{num}", True, BLACK)
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
                        print("up")
                    elif event.key == pygame.K_DOWN:
                        print("down")
                    elif event.key == pygame.K_LEFT:
                        print("left")
                    elif event.key == pygame.K_RIGHT:
                        print("right")
