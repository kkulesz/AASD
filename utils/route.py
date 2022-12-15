from typing import List
from dataclasses import dataclass
from cords import Cords
from aioxmpp import JID


@dataclass
class Target:
    cords: Cords
    jid: JID
    est_rubbish_volume: int


class Route:
    def __init__(self, targets: List[Target]):
        self.targets = targets

    def estimate_distance(self, start: Cords) -> float:
        dist = 0
        curr_cords = start
        for target in self.targets:
            dist += target.cords.dist(curr_cords)
            curr_cords = target.cords
        return dist

    def estimate_rubbish_volume(self) -> int:
        volume = 0
        for target in self.targets:
            volume += target.est_rubbish_volume
        return volume

    def last_target(self) -> Target:
        return self.targets[-1]
