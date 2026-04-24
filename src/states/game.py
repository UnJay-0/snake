import pygame
from src.entities.apple import Apple
from src.entities.game_time import GameTimer
from src.entities.grid import Grid
from src.entities.snake import Snake
from src.states.state import State
from src.utils import random_direction_from_all
from src.utils.app_settings import AppSettings, FONTS_PATH

BIG_FONT_SIZE = 70
SMALL_FONT_SIZE = 20

class GameState(State):
    def __init__(self, app_settings: AppSettings):
        self.paused = False
        # APP SETTINGS
        self.app_settings = app_settings
        self.big_font = pygame.font.Font(FONTS_PATH / "Jersey15-Regular.ttf", BIG_FONT_SIZE)
        self.small_font = pygame.font.Font(FONTS_PATH / "Jersey15-Regular.ttf", SMALL_FONT_SIZE)
        # GAME ELEMENTS
        self.field = pygame.image.load("assets/graphics/field.png")
        self.grid = Grid(self.app_settings.field_dimensions)
        self.snake = Snake(
            self.grid.random_position(),
            random_direction_from_all(),
            self.app_settings.field_dimensions,
            self.app_settings.frame_rate
        )
        self.apples = pygame.sprite.Group(Apple(self.grid.random_position()))
        # SCORE VALUES
        self.game_time = GameTimer(pygame.time.get_ticks())
        self.score = 0
        print(self.snake)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.app_settings.keybindings.player_1.keys():
                print("\nbefore: \n", self.snake)
                self.snake.add_direction(self.app_settings.keybindings.player_1[event.key])
                print("after: \n", self.snake)
            if event.key == pygame.K_r:
                self.reset()
                print("*" * 20, "RESET", "*" * 20)
                print(self.snake)
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
                self.game_time.pause(self.paused)

    def update(self):
        self.game_time.update(pygame.time.get_ticks())
        if not self.paused:
            if len(self.apples.sprites()) == 0:
                self.apples.add(Apple(
                    self.grid.random_position()
                ))
            else:
                head_cell = self.snake.get_head_cell()
                colliders = pygame.sprite.spritecollide(head_cell, self.apples, True)
                for collider in colliders:
                    self.score = collider.apply(self.snake, self.score)
            self.snake.update()
            if self.snake.head_collision():
                self.reset()
                return
            self.apples.update()

    def reset(self):
        self.snake.reset(
            self.grid.random_position(),
            random_direction_from_all())
        self.apples.empty()
        self.score = 0
        self.game_time.reset_to(pygame.time.get_ticks())

    def render(self, surface: pygame.Surface):
        surface.blit(self.field, (0,0))
        surface.blit(self.small_font.render("Score:", False, (149, 241, 72)), (24, 0))
        surface.blit(self.big_font.render(str(self.score), False, (149, 241, 72)), (32, 16))
        surface.blit(self.small_font.render("Time:", False, (149, 241, 72)), (700, 0))
        surface.blit(self.big_font.render(
            GameTimer.convert_to_str(
                self.game_time.get_time()),
            False,
            (149, 241, 72)
            ),
        (684, 16)
        )
        self.snake.render(surface)
        self.apples.draw(surface)
