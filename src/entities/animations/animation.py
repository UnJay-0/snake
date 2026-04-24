from __future__ import annotations
from pygame import Surface, transform
from src import utils

class AnimationComponents():
    def __init__(self, **components: Animation):
        self.animation_components = components

    def get_current_frame(self, component_name: str):
        return self.animation_components[component_name].get_current_frame()

    def get_component(self, component_name: str):
        return self.animation_components[component_name]

    def copy(self) -> AnimationComponents:
        copy_components = {}
        for key, component in self.animation_components.items():
            copy_components[key] = component.copy()
        return AnimationComponents(**copy_components)

    @staticmethod
    def flip(components: AnimationComponents, horizontally: bool):
        for _, component in components.animation_components.items():
            component.flip(horizontally)

    @staticmethod
    def rotate(components: AnimationComponents, up: bool):
        for _, component in components.animation_components.items():
            component.rotate(up)

    @staticmethod
    def do_nothing(*args):
        pass

    @staticmethod
    def elaborate_first_direction(direction: utils.Command) -> tuple:
        match direction:
            case utils.UP:
                return (AnimationComponents.rotate, True, 0, 1)
            case utils.DOWN:
                return (AnimationComponents.rotate, False, 0, -1)
            case utils.LEFT:
                return (AnimationComponents.flip, True, 1, 0)
            case utils.RIGHT:
                return (AnimationComponents.do_nothing, False, -1, 0)

    def update(self):
        for _, component in self.animation_components.items():
            component.update()

    def reset(self):
        for _, component in self.animation_components.items():
            component.reset()

class Animation():
    def __init__(self, frames: list[Surface], speed: float, frame_rate:int):
        self.frames = frames
        self.speed = speed
        print(frame_rate)
        self.frame_rate = frame_rate
        self.counter = 0
        self.index = 0

    def get_current_frame(self) -> Surface:
        return self.frames[self.index]

    def flip(self, horizontally: bool):
        new_frames = []
        for frame in self.frames:
            new_frames.append(transform.flip(frame, horizontally, not horizontally))
        self.frames = new_frames

    def rotate(self, up: bool):
        new_frames = []
        for frame in self.frames:
            new_frames.append(transform.rotate(frame, 90 if up else -90))
        self.frames = new_frames

    def copy(self) -> Animation:
        animation_copy = Animation(
            list(map(lambda surface: Surface.copy(surface), self.frames)),
            self.speed,
            self.frame_rate
        )
        animation_copy.counter = self.counter
        animation_copy.index = self.index
        return animation_copy

    def update(self):
        self.counter += 1
        if self.counter == (self.frame_rate // self.speed):
            self.counter = 0
            self.index = (self.index + 1) % len(self.frames)

    def reset(self):
        self.counter = 0

class StillAnimation(Animation):
    def __init__(self, frame: Surface):
        self.frame = frame

    def get_current_frame(self) -> Surface:
        return self.frame

    def flip(self, horizontally: bool):
        self.frame = transform.flip(self.frame, horizontally, not horizontally)

    def rotate(self, up: bool) -> Surface:
        self.frame = transform.rotate(self.frame, 90 if up else -90)

    def copy(self) -> StillAnimation:
        return StillAnimation(Surface.copy(self.frame))

    def update(self):
        pass

    def reset(self):
        pass
