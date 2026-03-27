from random import choice

class Grid():
    def __init__(self, field_dimensions: tuple[list[int]]):
        self.positions = [(x, y)
            for x in range(field_dimensions[0][0], field_dimensions[0][1], 16)
            for y in range(field_dimensions[1][0], field_dimensions[1][1], 16)]


    def random_position(self, exclude: list[tuple[int, int]]=[]):
        return choice([pos for pos in self.positions if pos not in exclude])
