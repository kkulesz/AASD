from protocols.base_message import BaseMessage
from utils.route import Route


class RouteOrder(BaseMessage):
    route: Route

    @classmethod
    def get_performative(cls) -> str:
        return "request"


class AcceptOrder(BaseMessage):
    @classmethod
    def get_performative(cls) -> str:
        return "accept"


class DeclineOrder(BaseMessage):
    overflow_volume: int

    @classmethod
    def get_performative(cls) -> str:
        return "refuse"
