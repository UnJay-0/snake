import pygame
from src.entities.snake import Snake
from src.states.state import State
from random import randint
from src.utils import random_direction_from_all
from src.utils.app_settings import AppSettings

class GameState(State):
    def __init__(self, app_settings: AppSettings):
        self.app_settings = app_settings
        head_position = self.__random_snake_position()
        direction = random_direction_from_all()
        self.snake = Snake(head_position, direction, self.app_settings.field_dimensions)
        self.field = pygame.image.load("assets/graphics/field.png")
        print(self.snake)

    def __random_snake_position(self) -> tuple:
        return (randint(self.app_settings.field_dimensions[0][0], self.app_settings.field_dimensions[0][1]),
            randint(self.app_settings.field_dimensions[1][0], self.app_settings.field_dimensions[1][1]))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.app_settings.keybindings.player_1.keys():
                print("before: \n", self.snake)
                self.snake.add_direction(self.app_settings.keybindings.player_1[event.key])
                print("after: \n", self.snake)
            if event.key == pygame.K_r:
                self.reset()
                print("*" * 20, "RESET", "*" * 20)
                print(self.snake)

    def update(self):
        self.snake.update()

    def reset(self):
        self.snake.reset(self.__random_snake_position(), random_direction_from_all())

    def render(self, surface: pygame.Surface):
        surface.blit(self.field, (0,0))
        self.snake.render(surface)
