import entities
import pygame

from src.entities.cell import Cell
from src.entities import CELL_DIMENSION
SNAKE_ASSETS_PATH = "assets/graphics/snake"


class Snake():
    def __init__(self, head_position:tuple, direction: int, field_dimensions:list):
        self.head_frames = [
            pygame.image.load(SNAKE_ASSETS_PATH + f"/head/snake_head{i}.png") for i in range(1, 4)
        ]
        self.tail_frames = [
            pygame.image.load(SNAKE_ASSETS_PATH + f"/head/snake_tail{i}.png") for i in range(1, 4)
        ]
        self.middle = pygame.image.load(SNAKE_ASSETS_PATH + "snake_body.png")
        self.field_dimensions = field_dimensions
        self.body = pygame.sprite.Group(self._construct_body(head_position, direction))
        self.direction_stack = [(None, direction)]

    def _construct_body(self, head_position: tuple, direction: int) -> list[Cell]:
        transformation, type, x_cell_value, y_cell_value = Snake.elaborate_direction(direction)
        head = self.head_frames[0].copy()
        tail = self.tail_frames[0].copy()
        middle = self.middle.copy()
        if transformation:
            head = transformation(head, type)
            tail = transformation(tail, type)
            middle = transformation(middle, type)
        return [
            Cell(head, head_position, self.field_dimensions),
            Cell(middle, (head_position[0] + x_cell_value, head_position[1] + y_cell_value), self.field_dimensions),
            Cell(tail, (head_position[0] + x_cell_value, head_position[1] + y_cell_value), self.field_dimensions)
        ]

    @staticmethod
    def elaborate_direction(direction:int) -> tuple:
        match direction:
            case entities.UP:
                return (Snake.rotate, True, 0, CELL_DIMENSION)
            case entities.DOWN:
                return (Snake.rotate, False, 0, -CELL_DIMENSION)
            case entities.LEFT:
                return (None, False, -CELL_DIMENSION, 0)
            case entities.RIGHT:
                return (None, True, CELL_DIMENSION, 0)

    @staticmethod
    def flip(surface: pygame.Surface, horizontally: bool) -> pygame.Surface:
        pass

    @staticmethod
    def rotate(surface: pygame.Surface, up: bool) -> pygame.Surface:
        pass
