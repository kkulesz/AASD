import math
from dataclasses import dataclass


@dataclass
class Cords:
    x: int
    y: int

    def dist(self, other):
        return math.dist([self.x, self.y], [other.x, other.y])
