from typing import Iterator, Tuple, Optional, Union

from aioxmpp import JID
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from agents.base_agent import BaseAgent
from protocols.disposal_message import *
from protocols.pick_up import *
from utils.logger import Logger

import random


class LandfillAgent(BaseAgent):
    def __init__(
        self,
        jid: Union[str, JID],
        password: str,
        logger: Logger,
    ):
        super().__init__(jid, password, logger)
        self.jid = jid
        self.logger = logger

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            (
                self.DisposalRequest(self.jid, self.logger),
                Template(metadata=DisposalMessage.get_metadata()),
            ),
        ]

    def step(self):
        pass

    class DisposalRequest(CyclicBehaviour):
        def __init__(
            self,
            jid: Union[str, JID],
            logger: Logger,
        ):
            super().__init__()
            self.sender = jid
            self.logger = logger

        async def run(self) -> None:
            message = await self.receive(60)
            if message:
                _ = BaseMessage.parse(message)

                self.logger.log(f"{self.sender} accept disposal of {message.sender}.")
                rsp = AcceptDisposal().to_spade(message.sender, self.sender)
                await self.send(rsp)
