# STATE INTERFACE
from pygame import Surface
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle_events(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def render(self, surface: Surface):
        pass
