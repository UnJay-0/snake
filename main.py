import pygame
from src.scene import Scene
from src.states.game import GameState
from src.utils.app_settings import AppSettings


def main():
    pygame.init()
    app_settings = AppSettings()
    screen = pygame.display.set_mode(app_settings.resolution)
    sceneContext = Scene("snake", screen, GameState(app_settings), app_settings)
    sceneContext.run()

if __name__ == "__main__":
    main()
