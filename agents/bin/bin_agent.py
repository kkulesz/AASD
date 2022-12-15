from typing import Iterator, Tuple, Optional, Union

from aioxmpp import JID
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.template import Template

from agents.base_agent import BaseAgent
from protocols.bin_state_message import BinStateMessage
from utils.logger import Logger
from .bin_logic import BinLogic


class BinAgent(BaseAgent):
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            supervisor_jid: Union[str, JID],
            period: int,
            logger: Logger,
            logic: BinLogic
    ):
        super().__init__(str(jid), password, logger)
        self.jid = jid
        self.supervisor_jid = supervisor_jid
        self.period = period
        self.logger = logger
        self.logic = logic

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            (
                self.BroadcastFillLevel(self.jid, self.supervisor_jid, self.period, self.logger, self.logic),
                None
            )
        ]

    def step(self):
        # TODO: add some rubbish with some probability
        self.log("tik")
        pass

    class BroadcastFillLevel(PeriodicBehaviour):
        def __init__(
                self,
                jid: Union[str, JID],
                supervisor_jid: Union[str, JID],
                period: int,
                logger: Logger,
                logic: BinLogic
        ):
            super().__init__(period)
            self.sender = jid
            self.to = supervisor_jid
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            msg = BinStateMessage(
                fill_level_percentage=self.logic.fill_level_percentage,
                max_volume=self.logic.max_volume,
                position=self.logic.position
            ).to_spade(self.to, self.sender)

            await self.send(msg)
