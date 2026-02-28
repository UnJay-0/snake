import pygame

from src import entities

CELL_DIMENSION = 16

class Cell(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, position: tuple, field_dimensions: list):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.field_dimensions = field_dimensions

    def next(self, direction: int):
        new_position = self.rect.topleft
        match direction:
            case entities.UP:
                new_position = (self.rect.topleft[0], self.rect.topleft[1] - CELL_DIMENSION)
            case entities.DOWN:
                new_position = (self.rect.topleft[0], self.rect.topleft[1] + CELL_DIMENSION)
            case entities.LEFT:
                new_position = (self.rect.topleft[0] - CELL_DIMENSION, self.rect.topleft[1])
            case entities.RIGHT:
                new_position = (self.rect.topleft[0] + CELL_DIMENSION, self.rect.topleft[1])
        new_position = self._normalize(new_position)
        return Cell(self.image, new_position, self.field_dimensions)


    def _normalize(self, position: tuple) -> tuple:
        x = (((position[0] - (self.field_dimensions[0][0])) %
            (self.field_dimensions[0][1] - self.field_dimensions[0][0]))
            + (self.field_dimensions[0][0]))
        y = (((position[1] - (self.field_dimensions[1][0])) %
            (self.field_dimensions[1][1] - self.field_dimensions[1][0]))
            + (self.field_dimensions[1][0]))
        return (x, y)
