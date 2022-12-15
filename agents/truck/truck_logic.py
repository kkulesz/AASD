from utils.cords import Cords
from utils.logger import Logger
from utils.route import Route
from dataclasses import dataclass
from aioxmpp import JID
from typing import Dict


class TruckLogic:
    def __init__(self,
                 logger: Logger,
                 position: Cords,
                 landfills: Dict[JID, Cords],
                 fill_level_percentage: int = 0,
                 max_volume: int = 1000,
                 range: float = 100,
                 curr_range: float = 100,
                 curr_route: Route = None):
        self.position = position
        self.fill_level_percentage = fill_level_percentage
        self.max_volume = max_volume
        self.range = range
        self.curr_range = curr_range
        self.curr_route = curr_route
        self._logger = logger
        self.landfills = landfills

    def _estimate_distance_to_landfill(self):
        if self.curr_route:
            start_point = self.curr_route.last_target()
        else:
            start_point = self.position
        dist = 0
        for landfill_cords in self.landfills.values():
            dist += landfill_cords.dist(start_point.cords)
        dist /= len(self.landfills)
        return dist

    def estimate_remaining_distance(self):
        return self.curr_route.estimate_distance(self.position) + self._estimate_distance_to_landfill() \
            if self.curr_route else 0

    def estimate_remaining_volume(self):
        curr_volume = self.max_volume * (1 - self.fill_level_percentage)
        return curr_volume - self.curr_route.estimate_rubbish_volume() if self.curr_route else curr_volume


