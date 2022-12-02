from typing import Iterator, Tuple, Optional, Union

from aioxmpp import JID
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template

from agents.base_agent import BaseAgent
from utils.logger import Logger


class Bin(BaseAgent):
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            logger: Logger,
            fill_level_percentage: int = 0
    ):
        super().__init__(str(jid), password, logger)
        self.fill_level_percentage = fill_level_percentage

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            (self.BroadcastFillLevel(), None)  # TODO
        ]

    class BroadcastFillLevel(CyclicBehaviour):
        def __init__(self):
            super().__init__()

        async def run(self) -> None:
            pass
