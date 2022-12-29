from typing import Iterator, Tuple, Optional, Union

from aioxmpp import JID
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.template import Template

from agents.base_agent import BaseAgent
from protocols.truck_state_message import TruckStateMessage
from protocols.pick_up import *
from protocols.route_order import *
from utils.route import Target
from protocols.base_message import BaseMessage
from protocols.disposal_message import *
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
        logic: TruckLogic,
    ):
        super().__init__(str(jid), password, logger)
        self.jid = jid
        self.supervisor_jid = supervisor_jid
        self.period = period
        self.logger = logger
        self.logic = logic

    def get_behaviours_with_templates(self) -> Iterator[Tuple[CyclicBehaviour, Optional[Template]]]:
        return [
            (self.SendTruckState(self.jid, self.supervisor_jid, self.period, self.logger, self.logic), None),
            (
                self.ReceiveRouteOrder(self.jid, self.logger, self.logic),
                Template(metadata=RouteOrder.get_metadata()),
            ),
            (self.PickUpRubbish(self.jid, self.logger, self.logic), None),
            (
                self.ReceivePickUpResponse(self.jid, self.logger, self.logic),
                Template(metadata=PickUpResponse.get_metadata()),
            ),
            (self.EmptyTruckRequest(self.jid, self.logger, self.logic), None),
            (
                self.ReciveAcceptDisposal(self.logger, self.logic),
                Template(metadata=AcceptDisposal.get_metadata()),
            ),
            (self.EmptyTruck(self.logger, self.logic), None),
        ]

    def step(self):
        self.logic.move()
        # TODO na razie gdy zapełni się co najmniej do połowy to chcemy ją opróżnić
        if self.logic.fill_level_percentage > 0.5:
            self.logic.need_empty = True

    class PickUpRubbish(CyclicBehaviour):
        def __init__(self, jid: Union[str, JID], logger: Logger, logic: TruckLogic):
            super().__init__()
            self.sender = jid
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            target = self.logic.curr_target()
            if (
                target
                and self.logic.position == target.cords
                and not self.logic.stop
                and not target.cords in self.logic.landfills.values()
            ):
                msg = PickUpMessage().to_spade(JID(*target.jid), self.sender)
                await self.send(msg)
                self.logic.stop = True

    class ReceivePickUpResponse(CyclicBehaviour):
        def __init__(self, jid: Union[str, JID], logger: Logger, logic: TruckLogic):
            super().__init__()
            self.sender = jid
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            rsp = await self.receive()
            if rsp:
                rsp_content: PickUpResponse = BaseMessage.parse(rsp)
                self.logic.pick_up(rsp_content.volume)

    class ReceiveRouteOrder(CyclicBehaviour):
        def __init__(self, jid: Union[str, JID], logger: Logger, logic: TruckLogic):
            super().__init__()
            self.sender = jid
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            msg = await self.receive()
            if msg:
                msg_content: RouteOrder = BaseMessage.parse(msg)
                overflow_volume = self.logic.check_order(msg_content.route)
                if overflow_volume:
                    rsp = DeclineOrder(overflow_volume=overflow_volume).to_spade(msg.sender, self.sender)
                    self.logger.log("DECLINE")
                else:
                    rsp = AcceptOrder().to_spade(msg.sender, self.sender)
                    self.logic.update_route(msg_content.route)
                await self.send(rsp)

    class SendTruckState(PeriodicBehaviour):
        def __init__(
            self, jid: Union[str, JID], supervisor_jid: Union[str, JID], period: int, logger: Logger, logic: TruckLogic
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
                position=self.logic.position,
            ).to_spade(self.to, self.sender)

            await self.send(msg)

    class EmptyTruckRequest(CyclicBehaviour):
        def __init__(self, jid: Union[str, JID], logger: Logger, logic: TruckLogic):
            super().__init__()
            self.sender = jid
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            if self.logic.need_empty and not self.logic.on_way:
                self.logic.on_way = True
                garbage_amount = self.logic.max_volume - self.logic.estimate_remaining_volume()
                msg = DisposalMessage(garbage_amount=garbage_amount).to_spade(self.logic.select_landlift(), self.sender)
                await self.send(msg)

    class ReciveAcceptDisposal(CyclicBehaviour):
        def __init__(self, logger: Logger, logic: TruckLogic):
            super().__init__()
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            msg = await self.receive()
            if msg:
                garbage_amount = self.logic.max_volume - self.logic.estimate_remaining_volume()
                _ = BaseMessage.parse(msg)
                self.logic.update_route(
                    Route([Target(self.logic.landfills[str(msg.sender)], str(msg.sender), -garbage_amount)])
                )

    class EmptyTruck(CyclicBehaviour):
        def __init__(self, logger: Logger, logic: TruckLogic):
            super().__init__()
            self.logger = logger
            self.logic = logic

        async def run(self) -> None:
            target = self.logic.curr_target()
            if (
                target
                and self.logic.position == target.cords
                and not self.logic.stop
                and target.cords in self.logic.landfills.values()
            ):
                self.logic.fill_level_percentage = 0
                self.logic.stop = True
                self.logic.on_way = False
