import pygame
from src.scene import Scene
from src.states.main_menu import MainMenuState


def main():
    pygame.init()
    sceneContext = Scene("snake", MainMenuState())
    sceneContext.run()

if __name__ == "__main__":
    main()
