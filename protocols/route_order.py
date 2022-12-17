from typing import Optional

from protocols.base_message import BaseMessage
from utils.route import Route


class RouteOrder(BaseMessage):
    # TODO z jakiegoś powodu jak to się odkomentuje to się wywala
    # route: Optional[Route]

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
