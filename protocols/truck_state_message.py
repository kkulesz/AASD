from protocols.base_message import BaseMessage
from utils.cords import Cords


class TruckStateMessage(BaseMessage):
    curr_est_route_distance: float
    curr_est_rubbish_volume: int
    position: Cords

    @classmethod
    def get_performative(cls) -> str:
        return "inform"
