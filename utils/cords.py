import math
from dataclasses import dataclass


@dataclass
class Cords:
    x: float
    y: float

    def dist(self, other):
        return math.dist([self.x, self.y], [other.x, other.y])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
