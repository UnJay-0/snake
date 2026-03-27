import pygame
from src.entities.apple import Apple
from src.entities.grid import Grid
from src.entities.snake import Snake
from src.states.state import State
from src.utils import random_direction_from_all
from src.utils.app_settings import AppSettings

class GameState(State):
    def __init__(self, app_settings: AppSettings):
        self.paused = False
        self.app_settings = app_settings
        self.grid = Grid(self.app_settings.field_dimensions)
        head_position = self.grid.random_position()
        direction = random_direction_from_all()
        self.snake = Snake(head_position, direction, self.app_settings.field_dimensions)
        self.apples = pygame.sprite.Group(Apple(self.grid.random_position()))
        self.field = pygame.image.load("assets/graphics/field.png")
        print(self.snake)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.app_settings.keybindings.player_1.keys():
                print("\nbefore: \n", self.snake)
                self.snake.add_direction(self.app_settings.keybindings.player_1[event.key])
                print("after: \n", self.snake)
            if event.key == pygame.K_r:
                self.reset()
                #print("*" * 20, "RESET", "*" * 20)
                #print(self.snake)
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused

    def update(self):
        if not self.paused:
            if len(self.apples.sprites()) == 0:
                self.apples.add(Apple(
                    self.grid.random_position()
                ))
            else:
                head_cell = self.snake.get_head_cell()
                colliders = pygame.sprite.spritecollide(head_cell, self.apples, True)
                for collider in colliders:
                    collider.apply(self.snake)
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

    def render(self, surface: pygame.Surface):
        surface.blit(self.field, (0,0))
        self.snake.render(surface)
        self.apples.draw(surface)
