# CONTEXT
import pygame
from src.states.state import State
from src.utils.app_settings import AppSettings

class Scene():
    def __init__(self, caption: str,screen: pygame.Surface, initial_state: State, settings: AppSettings):
        pygame.display.set_caption(caption)
        self.frame_rate = settings.frame_rate
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = initial_state
        self.running = True

    def set_state(self, new_state: State):
        if new_state != None:
            self.state = new_state

    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit()
                case _:
                    self.set_state(self.state.handle_events(event))

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
            self.clock.tick(self.frame_rate)
