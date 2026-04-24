from __future__ import annotations
from operator import attrgetter
import pygame
from src import utils
from src.entities.animations.animation import Animation

CELL_DIMENSION = 16

class Cell(pygame.sprite.Sprite):
    def __init__(self, type: int, cell_content: Animation, position: tuple, field_dimensions: list, direction: utils.Command=None):
        super().__init__()
        self.type = type
        self.cell_content = cell_content
        self.image = self.cell_content.get_current_frame()
        self.rect = self.image.get_rect(topleft=position)
        self.field_dimensions = field_dimensions
        self.direction = direction

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
        return Cell(self.type, self.cell_content, new_position, self.field_dimensions, direction)

    def prev(self) -> Cell:
        new_cell = self.next(self.direction.get_opposite())
        new_cell.direction = self.direction
        return new_cell

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

    def apply_content(self):
        self.image = self.cell_content.get_current_frame()

    def update(self):
        self.cell_content.update()

    def __str__(self) -> str:
        return f"{self.type} - {self.rect.topleft}"


    def copy(self) -> Cell:
        return Cell(
            self.type,
            self.cell_content.copy(),
            self.rect.topleft,
            self.field_dimensions,
            self.direction
        )

class Cells():
    def __init__(self, *cells: Cell):
        # Sorting by type (HEAD - MIDDLE - TAIL)
        self.movement_speed = 2
        self.movement_index = 0
        self.cells = pygame.sprite.Group(*sorted(cells, key=attrgetter("type")))
        self.head_direction = self.cells.sprites()[0].direction

    def apply_movement(self) -> bool:
        self.movement_index += 1
        if self.movement_index == self.movement_speed:
            self.movement_index = 0
            return True
        else:
            return False

    def apply_direction(self, direction: utils.Command):
        if not self.cells.sprites()[0].direction.get_opposite() == direction:
            self.head_direction = direction

    def get_cell(self, index: int) -> Cell:
        return self.cells.sprites()[index]

    def len(self) -> int:
        return len(self.cells.sprites())

    def duplicate_cell(self, index: int):
        cells = self.cells.sprites()
        shifted_cells = []
        for cell in cells[index:]:
            print(cell)
            shifted_cells.append(cell.prev())
        cells.insert(index, cells[index].copy())
        cells[0:index+1].extend(
            shifted_cells
        )
        self.cells = pygame.sprite.Group(
            cells
        )

    def add_before_tail(self, cell_order: int, content: Animation):
            last_cell = self.cells.sprites()[-1]
            new_cell = Cell(
                cell_order,
                content,
                last_cell.rect.topleft,
                last_cell.field_dimensions,
                last_cell.direction
            )
            new_cells = self.cells.sprites()[0:-1]
            new_cells.extend([
                new_cell,
                last_cell.prev()
            ])
            self.cells = pygame.sprite.Group(
                *new_cells
            )

    def check_collision(self) -> bool:
        head_position = self.cells.sprites()[0].get_position()
        for cell in self.cells.sprites()[1:]:
            if head_position == cell.get_position():
                return True
        return False

    def update(self):
        if self.apply_movement():
            self.cells.update()
            prev_direction = self.head_direction
            new_cells = []
            for cell in self.cells.sprites():
                new_cell = cell.next(prev_direction)
                if prev_direction != cell.direction:
                    rotation_direction = cell.direction.evaluate_orientation(prev_direction.get_sign())
                    new_cell.cell_content.rotate(rotation_direction)
                    new_cell.apply_content()
                new_cells.append(new_cell)
                prev_direction = cell.direction
            self.cells = pygame.sprite.Group(*new_cells)

    def render(self, surface: pygame.Surface):
        self.cells.draw(surface)

    def __str__(self) -> str:
        rep = "Cells positions: "
        for cell in self.cells.sprites():
            rep += f"\n  {cell}"
        return rep
