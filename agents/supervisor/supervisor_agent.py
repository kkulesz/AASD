from typing import Iterator, Tuple, Optional, Union
from aioxmpp import JID
from protocols.base_message import BaseMessage
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.template import Template

from .supervisor_logic import SupervisorLogic
from agents.bin.bin_logic import BinLogic
from agents.base_agent import BaseAgent
from utils.logger import Logger


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
        self.period = 1

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            # (
            #     self.BroadcastFillLevel(self.jid, self.supervisor_jid, self.period, self.logger, self.logic),
            #     None
            # ),
            # (
            #     self.BroadcastFillLevel(self.jid, self.supervisor_jid, self.period, self.logger, self.logic),
            #     None
            # ),
            (
                self.ReceiveBinState(self.period),
                None
            ),

        ]

    def step(self):
        pass

    class ReceiveBinState(PeriodicBehaviour):
        def __init__(
                self,
                period: int,
        ):
            super().__init__(period)

        async def run(self) -> None:
            message = await self.receive(60)
            if message:
                content = BaseMessage.parse(message)
                print(
                    f"New request from {message.sender}:\n{content}"
                )
