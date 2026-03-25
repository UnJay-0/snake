import pygame
from src import utils
from src.utils.app_settings import GRAPHICS_PATH
from src.entities.cell import Cell, Cells
from src.entities import HEAD_TYPE, MIDDLE_TYPE, TAIL_TYPE
SNAKE_ASSETS_PATH = GRAPHICS_PATH / "snake"


class Snake():
    __HEAD_INDEX = 0

    def __init__(self, head_position:tuple, direction: utils.Command, field_dimensions:list):
        self.head_frames = [
            pygame.image.load(SNAKE_ASSETS_PATH / f"head/snake_head{i}.png").convert_alpha() for i in range(1, 5)
        ]
        self.tail_frames = [
            pygame.image.load(SNAKE_ASSETS_PATH / f"tail/snake_tail{i}.png").convert_alpha() for i in range(1, 5)
        ]
        self.middle = pygame.image.load(SNAKE_ASSETS_PATH / "snake_body.png").convert_alpha()
        self.field_dimensions = field_dimensions
        self.body = self.__construct_initial_body(head_position, direction)

    def __construct_initial_body(self, head_position: tuple, direction: utils.Command) -> Cells:
        transformation, type, x_cell_value, y_cell_value = Cells.elaborate_first_direction(direction)
        head = self.head_frames[0].copy()
        tail = self.tail_frames[0].copy()
        middle = self.middle.copy()
        if transformation:
            head = transformation(head, type)
            tail = transformation(tail, type)
            middle = transformation(middle, type)
        return Cells(
            Cell(HEAD_TYPE,
                head,
                head_position,
                self.field_dimensions,
                direction),
            Cell(MIDDLE_TYPE,
                middle,
                (head_position[0] + x_cell_value, head_position[1] + y_cell_value),
                self.field_dimensions, direction),
            Cell(TAIL_TYPE,
                tail,
                (head_position[0] + x_cell_value*2, head_position[1] + y_cell_value*2),
                self.field_dimensions,
                direction)
        )

    def add_direction(self, direction: utils.Command):
        self.head_orientation = direction.orientation
        self.body.apply_direction(direction)


    def get_head_cell(self) -> Cell:
        return self.body.get_cell(self.__HEAD_INDEX)

    def head_collision(self, sprite: pygame.sprite.Sprite):
        pass

    def update(self):
        self.body.update()

    def reset(self, head_position: tuple, direction: utils.Command):
        self.body = self.__construct_initial_body(head_position, direction)

    def render(self, surface: pygame.Surface):
        self.body.render(surface)

    def __str__(self) -> str:
       return self.body.__str__()
