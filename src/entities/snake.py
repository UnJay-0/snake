import pygame
from src import utils
from src.entities.animations.animation import Animation, AnimationComponents, StillAnimation
from src.utils.app_settings import GRAPHICS_PATH
from src.entities.cell import Cell, Cells, CELL_DIMENSION
from src.entities import HEAD_NAME, HEAD_TYPE, MIDDLE_NAME, MIDDLE_TYPE, TAIL_NAME, TAIL_TYPE
SNAKE_ASSETS_PATH = GRAPHICS_PATH / "snake"
ANIMATION_SPEED = 10 # FRAME PER SECOND

class Snake():
    def __init__(self, head_position:tuple, direction: utils.Command, field_dimensions:list, frame_rate: int=60):
        self.field_dimensions = field_dimensions
        self.components = AnimationComponents(
            head=Animation([pygame.image.load(SNAKE_ASSETS_PATH / f"head/snake_head{i}.png").convert_alpha() for i in range(1, 11)],
                ANIMATION_SPEED,
                frame_rate),
            tail=Animation([
                pygame.image.load(SNAKE_ASSETS_PATH / f"tail/snake_tail{i}.png").convert_alpha() for i in range(1, 11)
            ], ANIMATION_SPEED, frame_rate),
            middle=StillAnimation(pygame.image.load(SNAKE_ASSETS_PATH / "snake_body.png").convert_alpha())
        )
        self.construct_body(head_position, direction)

    def construct_body(self, head_position: tuple, direction: utils.Command):
        components = self.components.copy()
        transformation, type, x, y = AnimationComponents.elaborate_first_direction(direction)
        transformation(components, type)
        self.body = Cells(
            Cell(
                HEAD_TYPE,
                components.get_component(HEAD_NAME),
                head_position,
                self.field_dimensions, direction
            ),
            Cell(MIDDLE_TYPE,
                components.get_component(MIDDLE_NAME),
                (head_position[0] + x*CELL_DIMENSION, head_position[1] + y*CELL_DIMENSION),
                self.field_dimensions, direction),
            Cell(TAIL_TYPE,
                components.get_component(TAIL_NAME),
                (head_position[0] + x*CELL_DIMENSION*2, head_position[1] + y*CELL_DIMENSION*2),
                self.field_dimensions,
                direction)
        )

    def add_direction(self, direction: utils.Command):
        self.head_orientation = direction.orientation
        self.body.apply_direction(direction)

    def get_head_cell(self) -> Cell:
        return self.body.get_cell(True)

    def increase(self):
        new_part = self.components.get_component(MIDDLE_NAME).copy()
        tail = self.body.get_cell(-1)
        transformation, type, _, _ = AnimationComponents.elaborate_first_direction(tail.direction)
        transformation(AnimationComponents(middle=new_part), type)
        self.body.add_before_tail(MIDDLE_TYPE, new_part)

    def head_collision(self) -> bool:
        return self.body.check_collision()

    def update(self):
        self.body.update()

    def reset(self, head_position: tuple, direction: utils.Command):
        self.construct_body(head_position, direction)

    def render(self, surface: pygame.Surface):
        self.body.render(surface)

    def __str__(self) -> str:
       return self.body.__str__()
