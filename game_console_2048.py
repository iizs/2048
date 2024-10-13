import sys
import pygame
import datetime
from game_of_2048 import GameOf2048


BLACK = 0, 0, 0
WHITE = 255, 255, 255
COLOR_BOARD = 200, 200, 200
COLOR_NUM = {
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
        self._information_surface_coord_ = (0, 0)
        self._information_surface_size_ = (1000, 100)

        self._reset_button_color_ = 'gray'
        self._reset_button_size_ = (150, 40)
        self._reset_button_coord_ = (580, 20)
        self._reset_button_font_name_ = 'Roboto'
        self._reset_button_font_size_ = 36
        self._reset_button_font_color_ = BLACK
        
        self._tile_size_ = 150
        self._tile_margin_ = 10
        self._tile_text_font_name_ = 'Roboto'
        self._board_surface_coord_ = (100, 120)
        self._board_surface_size_ = ((self._tile_size_ + self._tile_margin_) * 4, (self._tile_size_ + self._tile_margin_) * 4)

        self._information_text_font_ = pygame.font.SysFont(
            self._information_text_font_name_,
            self._information_text_font_size_
        )
        self._reset_button_font_ = pygame.font.SysFont(
            self._reset_button_font_name_,
            self._reset_button_font_size_
        )
        self._tile_text_font_large_ = pygame.font.SysFont(
            self._tile_text_font_name_,
            130
        )
        self._tile_text_font_medium_ = pygame.font.SysFont(
            self._tile_text_font_name_,
            100
        )
        self._tile_text_font_small_ = pygame.font.SysFont(
            self._tile_text_font_name_,
            80
        )
        self._tile_text_fonts_ = {
            2: self._tile_text_font_large_,
            4: self._tile_text_font_large_,
            8: self._tile_text_font_large_,
            16: self._tile_text_font_large_,
            32: self._tile_text_font_large_,
            64: self._tile_text_font_large_,
            128: self._tile_text_font_medium_,
            256: self._tile_text_font_medium_,
            512: self._tile_text_font_medium_,
            1024: self._tile_text_font_small_,
            2048: self._tile_text_font_small_,
            4096: self._tile_text_font_small_,
            8192: self._tile_text_font_small_,
        }
        # self._tile_text_sizes_ has been pre-calculated to enhance performance. 
        # (text.get_height(), text.get_width()) respectively
        # If font type and size are changed, this values also have to be re-calculated.
        self._tile_text_sizes_ = {
                2: (89, 49),
                4: (89, 49),
                8: (89, 49),
                16: (89, 98),
                32: (89, 103),
                64: (89, 98),
                128: (68, 118),
                256: (68, 114),
                512: (68, 114),
                1024: (55, 128),
                2048: (55, 133),
                4096: (55, 133),
                8192: (55, 127),
        }
        self._tile_text_offsets_ = { 
            k: ( (self._tile_size_ - v[1]) / 2, (self._tile_size_ - v[0]) / 2 ) 
            for k, v in self._tile_text_sizes_.items() 
        }

        # main instances
        self._screen_ = pygame.display.set_mode(self._display_size_)
        self._information_surface_ = pygame.Surface(self._information_surface_size_)
        self._board_surface_ = pygame.Surface(self._board_surface_size_)
        self._game_ = GameOf2048()
    
    def update_information_surface(self):
        self._information_surface_.fill(self._screen_background_color_)

        if self._game_.game_ended:
            end_time = self._game_.end_time
            end_game_text_color = self._information_text_font_color_
        else:
            end_time = datetime.datetime.now()
            end_game_text_color = self._screen_background_color_

        score_text = self._information_text_font_.render(
            f"Score: {self._game_.score}",
            True,
            self._information_text_font_color_
        )
        score_text_rect = score_text.get_rect()
        score_text_rect.left = 10
        score_text_rect.top = 10

        time_text = self._information_text_font_.render(
            f"Elapsed Time: {end_time - self._game_.start_time}",
            True,
            self._information_text_font_color_
        )
        time_text_rect = time_text.get_rect()
        time_text_rect.left = 10
        time_text_rect.top = score_text_rect.top + score_text_rect.height + 10

        end_game_text = self._information_text_font_.render(
            f"Game Over",
            True,
            end_game_text_color
        )
        end_game_text_rect = end_game_text.get_rect()
        end_game_text_rect.left = 10
        end_game_text_rect.top = time_text_rect.top + time_text_rect.height + 10

        self._information_surface_.blit(score_text, score_text_rect)
        self._information_surface_.blit(time_text, time_text_rect)
        self._information_surface_.blit(end_game_text, end_game_text_rect)

        self._screen_.blit(self._information_surface_, self._information_surface_coord_)

    def update_board_surface(self):
        self._board_surface_.fill(self._screen_background_color_)

        for x in range(GameOf2048.BOARD_SIZE):
            for y in range(GameOf2048.BOARD_SIZE):
                num = self._game_.get_tile(x, y)
                if num is not None and num != 0:
                    num_text = self._tile_text_fonts_[num].render(f"{num}", True, BLACK)
                    if num in COLOR_NUM:
                        tile_color = COLOR_NUM[num]
                    else:
                        tile_color = COLOR_BOARD
                else:
                    num_text = None
                    tile_color = COLOR_BOARD

                pygame.draw.rect(
                    self._board_surface_,
                    tile_color,
                    pygame.Rect(
                        x * (self._tile_size_ + self._tile_margin_),
                        y * (self._tile_size_ + self._tile_margin_),
                        self._tile_size_,
                        self._tile_size_
                    )
                )

                if num_text is not None:
                    num_text_rect = num_text.get_rect()
                    num_text_rect.left = x * (self._tile_size_ + self._tile_margin_) + self._tile_text_offsets_[num][0]
                    num_text_rect.top = y * (self._tile_size_ + self._tile_margin_) + self._tile_text_offsets_[num][1]
                    self._board_surface_.blit(num_text, num_text_rect)
        
        self._screen_.blit(self._board_surface_, self._board_surface_coord_)
    
    def update_reset_button(self):
        pygame.draw.rect(
            self._screen_,
            self._reset_button_color_,
            pygame.Rect(self._reset_button_coord_, self._reset_button_size_)
        )
        reset_button_text = self._reset_button_font_.render(
            "RESET",
            True,
            self._reset_button_font_color_
        )
        reset_button_text_rect = reset_button_text.get_rect()
        reset_button_text_rect.left = self._reset_button_coord_[0] + 35
        reset_button_text_rect.top = self._reset_button_coord_[1] + 8
        self._screen_.blit(reset_button_text, reset_button_text_rect)

    def update_screen(self):
        self._screen_.fill(self._screen_background_color_)

        self.update_information_surface()
        self.update_board_surface()
        self.update_reset_button()
        
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos() 
                    if (self._reset_button_coord_[0] <= mouse[0] <= self._reset_button_coord_[0] + self._reset_button_size_[0] 
                        and self._reset_button_coord_[1] <= mouse[1] <= self._reset_button_coord_[1] + self._reset_button_size_[1]): 
                        self._game_.reset()
