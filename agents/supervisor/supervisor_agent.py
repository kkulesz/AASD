from typing import Iterator, Tuple, Optional, Union
from aioxmpp import JID
from protocols.base_message import BaseMessage
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.template import Template

from .supervisor_logic import SupervisorLogic
from agents.bin.bin_logic import BinLogic
from agents.base_agent import BaseAgent
from utils.logger import Logger
from protocols.bin_state_message import BinStateMessage
from protocols.truck_state_message import TruckStateMessage


class SupervisorAgent(BaseAgent):
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            logger: Logger,
            logic: SupervisorLogic
    ):
        super().__init__(jid, password, logger)
        self.jid = jid
        self.logger = logger
        self.logic = logic

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            (
                self.ReceiveTruckState(),
                Template(metadata=TruckStateMessage.get_metadata())
            ),
            # (
            #     self.ReceiveTruckEvent(),
            #     None
            # ),
            (
                self.ReceiveBinState(),
                Template(metadata=BinStateMessage.get_metadata()),
            ),

        ]

    def step(self):
        pass

    class ReceiveTruckState(CyclicBehaviour):
        def __init__(
                self,
        ):
            super().__init__()

        async def run(self) -> None:
            message: TruckStateMessage = await self.receive(60)
            if message:
                content = BaseMessage.parse(message)
                print(
                    f"New {type(content)} from {message.sender}:\n{content} TruckStateMessage"
                )
    
    # class ReceiveTruckEvent(CyclicBehaviour):
    #     def __init__(
    #             self,
    #     ):
    #         super().__init__()

    #     async def run(self) -> None:
    #         message = await self.receive(60)
    #         if message:
    #             content = BaseMessage.parse(message)
    #             print(
    #                 f"New request from {message.sender}:\n{content} TruckEvent"
    #             )

    class ReceiveBinState(CyclicBehaviour):
        def __init__(
                self,
        ):
            super().__init__()

        async def run(self) -> None:
            message = await self.receive(60)
            if message:
                content: BinStateMessage = BaseMessage.parse(message)
                print(
                    f"New {type(content)} from {message.sender}:\n{content} BinState"
                )
