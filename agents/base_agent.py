from abc import ABC, abstractmethod
from spade.agent import Agent
from spade.template import Template
from spade.behaviour import CyclicBehaviour
from aioxmpp import JID
from typing import Iterator, Tuple, Optional, Union

from utils.logger import Logger


class BaseAgent(ABC, Agent):
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            logger: Logger
    ):
        super().__init__(str(jid), password)
        self._logger = logger

    @abstractmethod
    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        pass

    def log(self, msg: str):
        self._logger.log(f"{self.jid}: {msg}")

    async def setup(self) -> None:
        self.log(f"starting...")
        for behaviour, template in self.get_behaviours_with_templates():
            self.add_behaviour(behaviour, template)
