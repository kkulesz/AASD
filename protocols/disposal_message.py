from protocols.base_message import BaseMessage


class DisposalMessage(BaseMessage):
    garbage_amount: float

    @classmethod
    def get_performative(cls) -> str:
        return "inform"


class AcceptDisposal(BaseMessage):
    @classmethod
    def get_performative(cls) -> str:
        return "accept"


class DeclineDisposal(BaseMessage):
    overflow_volume: float

    @classmethod
    def get_performative(cls) -> str:
        return "refuse"