from protocols.base_message import BaseMessage


class PickUpMessage(BaseMessage):

    @classmethod
    def get_performative(cls) -> str:
        return "inform"


class PickUpResponse(BaseMessage):
    volume: int

    @classmethod
    def get_performative(cls) -> str:
        return "inform"
