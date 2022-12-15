from typing import Iterator, Tuple, Optional, Union

from aioxmpp import JID
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
from spade.template import Template

from agents.base_agent import BaseAgent
from protocols.truck_state.truck_state_message import TruckStateMessage
from utils.logger import Logger
from .truck_logic import TruckLogic


class TruckAgent(BaseAgent):
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            supervisor_jid: Union[str, JID],
            period: int,
            logger: Logger,
            logic: TruckLogic
    ):
        super().__init__(str(jid), password, logger)
        self.jid = jid
        self.supervisor_jid = supervisor_jid
        self.target_bin_jid = None
        self.period = period
        self.logger = logger
        self.logic = logic

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            (
                self.SendTruckState(self.jid, self.supervisor_jid, self.period, self.logger, self.logic),
                None
            )
        ]

    def step(self):
        # TODO: add some rubbish with some probability
        self.log("tik")
        pass

    class SendTruckState(PeriodicBehaviour):
        def __init__(
                self,
                jid: Union[str, JID],
                supervisor_jid: Union[str, JID],
                period: int,
                logger: Logger,
                logic: TruckLogic
        ):
            super().__init__(period)
            self.sender = jid
            self.to = supervisor_jid
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            msg = TruckStateMessage(
                curr_est_rubbish_volume=self.logic.estimate_remaining_volume(),
                curr_est_route_distance=self.logic.estimate_remaining_distance(),
                position=self.logic.position
            ).to_spade(self.to, self.sender)

            await self.send(msg)

