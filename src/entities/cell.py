from __future__ import annotations
from operator import attrgetter
import pygame
from src import utils

CELL_DIMENSION = 16

class Cell(pygame.sprite.Sprite):
    def __init__(self, type: int, surface: pygame.Surface, position: tuple, field_dimensions: list, direction: utils.Command=None):
        super().__init__()
        self.type = type
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.field_dimensions = field_dimensions
        self.current_direction = direction

    def next(self, direction: int) -> Cell:
        new_position = self.rect.topleft
        match direction:
            case utils.UP:
                new_position = (self.rect.topleft[0], self.rect.topleft[1] - CELL_DIMENSION)
            case utils.DOWN:
                new_position = (self.rect.topleft[0], self.rect.topleft[1] + CELL_DIMENSION)
            case utils.LEFT:
                new_position = (self.rect.topleft[0] - CELL_DIMENSION, self.rect.topleft[1])
            case utils.RIGHT:
                new_position = (self.rect.topleft[0] + CELL_DIMENSION, self.rect.topleft[1])
        new_position = self._normalize(new_position)
        return Cell(self.type, self.image, new_position, self.field_dimensions, direction)

    def get_position(self) -> tuple:
        return self.rect.topleft


    def _normalize(self, position: tuple) -> tuple:
        x = (((position[0] - (self.field_dimensions[0][0])) %
            (self.field_dimensions[0][1] - self.field_dimensions[0][0]))
            + (self.field_dimensions[0][0]))
        y = (((position[1] - (self.field_dimensions[1][0])) %
            (self.field_dimensions[1][1] - self.field_dimensions[1][0]))
            + (self.field_dimensions[1][0]))
        return (x, y)

    def __str__(self) -> str:
        return f"{self.type} - {self.rect.topleft}"


class Cells():
    def __init__(self, *cells: Cell):
        # Sorting by type (HEAD - MIDDLE - TAIL)
        self.cells = pygame.sprite.Group(sorted(cells, key=attrgetter("type")))
        self.head_direction = self.cells.sprites()[0].current_direction

    def apply_direction(self, direction: utils.Command):
        if not self.cells.sprites()[0].current_direction.get_opposite() == direction:
            self.head_direction = direction
            print(direction)

    def update(self):
        prev_direction = self.head_direction
        new_cells = []
        for cell in self.cells.sprites():
                new_cells.append(cell.next(prev_direction))
                prev_direction = cell.current_direction
        self.cells = pygame.sprite.Group(*new_cells)

    def render(self, surface: pygame.Surface):
        self.cells.draw(surface)

    def __str__(self) -> str:
        rep = "Cells positions: "
        for cell in self.cells.sprites():
            rep += f"\n  {cell}"
        return rep
