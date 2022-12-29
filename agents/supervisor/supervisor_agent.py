from typing import Iterator, Tuple, Optional, Union, Set
from aioxmpp import JID
from protocols.base_message import BaseMessage
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.template import Template

from .supervisor_logic import SupervisorLogic
from agents.bin.bin_logic import BinLogic
from agents.base_agent import BaseAgent
from utils.logger import Logger
from protocols.bin_state_message import BinStateMessage
from protocols.route_order import *
from protocols.truck_state_message import TruckStateMessage


class SupervisorAgent(BaseAgent):
    def __init__(self, jid: Union[str, JID], password: str, logger: Logger, logic: SupervisorLogic, period: int):
        super().__init__(jid, password, logger)
        self.jid = jid
        self.logger = logger
        self.period = period
        self.logic = logic

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            (self.ReceiveTruckState(self.logger, self.logic), Template(metadata=TruckStateMessage.get_metadata())),
            # (
            #     self.ReceiveTruckEvent(),
            #     None
            # ),
            (
                self.ReceiveBinState(self.logger, self.logic),
                Template(metadata=BinStateMessage.get_metadata()),
            ),
            (self.SendRouteOrder(self.jid, self.period, self.logger, self.logic), None),
            (
                self.ReceiveDeclineOrder(self.logger, self.logic),
                Template(metadata=DeclineOrder.get_metadata()),
            ),
            (
                self.ReceiveAcceptOrder(self.logger, self.logic),
                Template(metadata=AcceptOrder.get_metadata()),
            ),
        ]

    def step(self):
        pass

    class ReceiveTruckState(CyclicBehaviour):
        def __init__(self, logger: Logger, logic: SupervisorLogic):
            super().__init__()
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            message = await self.receive(60)
            if message:
                content: TruckStateMessage = BaseMessage.parse(message)
                print(f"New {type(content)} from {message.sender}:\n{content} TruckStateMessage")
                self.logic.register_truck_state(
                    message.sender, content.position, content.curr_est_rubbish_volume, content.curr_est_route_distance
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
        def __init__(self, logger: Logger, logic: SupervisorLogic):
            super().__init__()
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            message = await self.receive(60)
            if message:
                content: BinStateMessage = BaseMessage.parse(message)
                print(f"New {type(content)} from {message.sender}:\n{content} BinState")
                self.logic.register_bin_state(
                    message.sender, content.position, content.max_volume, content.fill_level_percentage
                )

    class SendRouteOrder(PeriodicBehaviour):
        def __init__(
            self,
            jid: Union[str, JID],
            period: int,
            logger: Logger,
            logic: SupervisorLogic,
        ):
            super().__init__(period)
            self.sender = jid
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            self.logic.plan()
            if self.logic.pending_routes:
                jid, route = self.logic.peek_route()
                if self.logic.got_response(jid):
                    msg = RouteOrder(route=route).to_spade(jid, self.sender)
                    await self.send(msg)
                    self.logic.await_response(jid)

    class ReceiveAcceptOrder(CyclicBehaviour):
        def __init__(self, logger: Logger, logic: SupervisorLogic):
            super().__init__()
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            rsp = await self.receive()
            if rsp:
                self.logic.pop_route(rsp.sender)
                self.logic.awaiting_response = None

    class ReceiveDeclineOrder(CyclicBehaviour):
        def __init__(self, logger: Logger, logic: SupervisorLogic):
            super().__init__()
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            rsp = await self.receive()
            if rsp:
                rsp_content: DeclineOrder = BaseMessage.parse(rsp)
                self.logic.process_decline(rsp_content.overflow_volume)
