# CONTEXT
import pygame
from src.states.state import State
from src.utils.app_settings import load_settings

class Scene():
    def __init__(self, caption: str, initial_state: State):
        pygame.display.set_caption(caption)
        self.settings = load_settings()
        self.screen = pygame.display.set_mode(self.settings["resolution"])
        self.clock = pygame.time.Clock()
        self.state = initial_state
        self.running = True

    def set_state(self, new_state: State):
        self.state = new_state

    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case _:
                    #self.set_state(self.state.handle_events(event))
                    pass

    def update(self):
        self.state.update()
        pygame.display.update()

    def render(self):
        self.state.render(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.settings["frame_rate"])
