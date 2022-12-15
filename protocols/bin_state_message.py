from protocols.base_message import BaseMessage
from utils.cords import Cords


class BinStateMessage(BaseMessage):
    fill_level_percentage: int
    position: Cords

    @classmethod
    def get_performative(cls) -> str:
        return "inform"
