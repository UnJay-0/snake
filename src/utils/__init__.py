from __future__ import annotations
from dataclasses import dataclass
from random import choice



@dataclass(frozen=True)
class Command:
    name: str
    value: int
    orientation: int

    def get_opposite(self) -> Command:
        return Command("", -self.value, self.orientation)

    def evaluate_orientation(self, new_value: int) -> bool:
        sign = self.get_sign()
        return self.orientation * sign * new_value > 0

    def get_sign(self):
        return (self.value > 0) - (self.value < 0)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if type(other) is Command:
            return other.value == self.value
        return False





UP = Command("UP", 1, -1)
DOWN = Command("DOWN", -1, -1)
LEFT = Command("LEFT", -2, 1)
RIGHT = Command("RIGHT", 2, 1)
CONFIRM = Command("CONFIRM", 4, 0)



def random_direction(allowed: list[Command]) -> Command:
    return choice(allowed)

def random_direction_from_all() -> Command:
    return random_direction([UP, DOWN, LEFT, RIGHT])
