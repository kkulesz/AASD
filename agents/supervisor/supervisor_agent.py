from typing import Iterator, Tuple, Optional, Union
from aioxmpp import JID
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from .supervisor_logic import SupervisorLogic
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

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        pass

    def step(self):
        pass
