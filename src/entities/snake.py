import pygame
from src import utils
from src.entities.cell import Cell, CELL_DIMENSION, Cells
from src.entities import HEAD_TYPE, MIDDLE_TYPE, TAIL_TYPE
SNAKE_ASSETS_PATH = "assets/graphics/snake"


class Snake():
    __HEAD_INDEX = 0
    __TAIL_INDEX = -1

    def __init__(self, head_position:tuple, direction: utils.Command, field_dimensions:list):
        self.head_frames = [
            pygame.image.load(SNAKE_ASSETS_PATH + f"/head/snake_head{i}.png").convert_alpha() for i in range(1, 5)
        ]
        self.tail_frames = [
            pygame.image.load(SNAKE_ASSETS_PATH + f"/tail/snake_tail{i}.png").convert_alpha() for i in range(1, 5)
        ]
        self.middle = pygame.image.load(SNAKE_ASSETS_PATH + "/snake_body.png").convert_alpha()
        self.field_dimensions = field_dimensions
        self.body = self.__construct_initial_body(head_position, direction)

    def __construct_initial_body(self, head_position: tuple, direction: utils.Command) -> Cells:
        transformation, type, x_cell_value, y_cell_value = Snake.__elaborate_direction(direction)
        head = self.head_frames[0].copy()
        tail = self.tail_frames[0].copy()
        middle = self.middle.copy()
        if transformation:
            head = transformation(head, type)
            tail = transformation(tail, type)
            middle = transformation(middle, type)
        return Cells(
            Cell(HEAD_TYPE, head, head_position, self.field_dimensions, direction),
            Cell(MIDDLE_TYPE, middle, (head_position[0] + x_cell_value, head_position[1] + y_cell_value), self.field_dimensions, direction),
            Cell(TAIL_TYPE, tail, (head_position[0] + x_cell_value*2, head_position[1] + y_cell_value*2), self.field_dimensions, direction)
        )

    def add_direction(self, direction: utils.Command):
        self.body.apply_direction(direction)

    @staticmethod
    def __elaborate_direction(direction: utils.Command) -> tuple:
        match direction:
            case utils.UP:
                return (Snake.__rotate, True, 0, CELL_DIMENSION)
            case utils.DOWN:
                return (Snake.__rotate, False, 0, -CELL_DIMENSION)
            case utils.LEFT:
                return (Snake.__flip, True, CELL_DIMENSION, 0)
            case utils.RIGHT:
                return (None, False, -CELL_DIMENSION, 0)

    @staticmethod
    def __flip(surface: pygame.Surface, horizontally: bool) -> pygame.Surface:
        return pygame.transform.flip(surface, horizontally, not horizontally)

    @staticmethod
    def __rotate(surface: pygame.Surface, up: bool) -> pygame.Surface:
        return pygame.transform.rotate(surface, 90 if up else -90)

    def update(self):
        self.body.update()

    def reset(self, head_position: tuple, direction: utils.Command):
        self.body = self.__construct_initial_body(head_position, direction)

    def render(self, surface: pygame.Surface):
        self.body.render(surface)

    def __str__(self) -> str:
       return self.body.__str__()
