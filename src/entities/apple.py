import pygame
from src.utils.app_settings import GRAPHICS_PATH
APPLE_ASSETS_PATH = GRAPHICS_PATH / "apple"

class Apple(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.image = pygame.image.load(APPLE_ASSETS_PATH / "apple.png")
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        pass
