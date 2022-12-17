from utils.cords import Cords
from utils.logger import Logger
from utils.route import Route

from aioxmpp import JID
from typing import Dict, Optional
from enum import Enum
import consts

# class DeclineTypes(Enum):
#     DISTANCE = 1
#     VOLUME = 2
#
#
# class DeclineReason:
#     type: DeclineTypes
#     amount: float


class TruckLogic:
    def __init__(self,
                 logger: Logger,
                 position: Cords,
                 landfills: Dict[JID, Cords],
                 fill_level_percentage: int = 0,
                 max_volume: int = 1000,
                 range: float = 100,
                 curr_range: float = 100,
                 speed: float = 1.,
                 curr_route: Route = None):
        self.position = position
        self.fill_level_percentage = fill_level_percentage
        self.max_volume = max_volume
        self.range = range
        self.speed = speed
        self.curr_range = curr_range
        self.curr_route = curr_route
        self._logger = logger
        self.landfills = landfills

    def _estimate_distance_to_landfill(self, position: Cords = None):
        if position:
            start_point = position
        elif self.curr_route:
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

    def move(self):
        target_cords = self.curr_route.curr_target().cords
        dist = self.position.dist(target_cords)
        if dist <= self.speed:
            new_cords = target_cords
        else:
            dx = (target_cords.x - self.position.x) / dist * self.speed
            dy = (target_cords.y - self.position.y) / dist * self.speed
            # niedokładność na floatach więc dodany epsilon
            assert dx**2 + dy**2 > self.speed - consts.EPSILON and dx**2 + dy**2 < self.speed + consts.EPSILON
            new_cords = Cords(self.position.x + dx, self.position.y + dy)
        self.position = new_cords
        self.curr_range -= self.speed

    def pick_up(self, rubbish_volume: int):
        self.curr_route.pop()
        self.fill_level_percentage += rubbish_volume // self.max_volume * 100

    def remaining_space(self):
        return self.max_volume * self.fill_level_percentage

    def check_order(self, route: Route) -> Optional[int]:

        # overall_distance = self.curr_route.estimate_distance(self.position) + \
        #                    route.estimate_distance(self.curr_route.last_target().cords) + \
        #                    self._estimate_distance_to_landfill(route.last_target().cords)
        # if overall_distance >= self.curr_range:
        #     decline_reasons.append()
        overall_volume = self.curr_route.estimate_rubbish_volume() + route.estimate_rubbish_volume()
        if overall_volume > self.remaining_space():
            return overall_volume - self.remaining_space()

    def update_route(self, route: Route):
        self.curr_route.extend(route)
