import time
from typing import List
from aioxmpp import JID

from environment.environment_config import EnvironmentConfig
from utils.logger import Logger
from agents.base_agent import BaseAgent
from agents.bin.bin_agent import BinAgent
from agents.bin.bin_logic import BinLogic
from agents.supervisor.supervisor_agent import SupervisorAgent
from agents.supervisor.supervisor_logic import SupervisorLogic
from agents.truck.truck_agent import TruckAgent
from agents.truck.truck_logic import TruckLogic
from agents.landfill.landfill_agent import LandfillAgent
from utils.cords import Cords
from utils.route import Route, Target
import consts


class Environment:
    def __init__(self, config: EnvironmentConfig, logger: Logger):
        self.logger = logger

        bins_jid = [
            JID(consts.BIN1_JIT.split("@")[0], consts.BIN1_JIT.split("@")[1], None),
            JID(consts.BIN2_JIT.split("@")[0], consts.BIN2_JIT.split("@")[1], None),
        ]
        self.bins = [
            BinAgent(
                bins_jid[i],
                consts.COMMON_PASSWORD,
                consts.SUPERVISOR_JIT,
                consts.BIN_INFORM_PERIOD,
                self.logger,
                BinLogic(position=data.position, fill_level_percentage=data.start_bin_level, logger=self.logger),
            )
            for i, data in enumerate(config.bins_data)
        ]
        truck_jid1 = JID(consts.TRUCK1_JIT.split("@")[0], consts.TRUCK1_JIT.split("@")[1], None)
        truck_jid2 = JID(consts.TRUCK2_JIT.split("@")[0], consts.TRUCK2_JIT.split("@")[1], None)
        self.trucks = [
            TruckAgent(
                truck_jid1,
                consts.COMMON_PASSWORD,
                consts.SUPERVISOR_JIT,
                3,
                self.logger,
                TruckLogic(
                    self.logger,
                    Cords(0, 0),
                    {
                        config.landfills_data[0].jid: Cords(
                            config.landfills_data[0].position.x, config.landfills_data[0].position.y
                        )
                    },
                    max_volume=110,
                ),
            ),
            TruckAgent(
                truck_jid2,
                consts.COMMON_PASSWORD,
                consts.SUPERVISOR_JIT,
                3,
                self.logger,
                TruckLogic(
                    self.logger,
                    Cords(0, 0),
                    {
                        config.landfills_data[0].jid: Cords(
                            config.landfills_data[0].position.x, config.landfills_data[0].position.y
                        )
                    },
                    max_volume=110,
                ),
            ),
        ]

        landfill_jid1 = JID(consts.LANDFILL_JIT.split("@")[0], consts.LANDFILL_JIT.split("@")[1], None)
        self.landfills = [LandfillAgent(landfill_jid1, consts.COMMON_PASSWORD, self.logger)]
        supervisor_jid = JID(consts.SUPERVISOR_JIT.split("@")[0], consts.SUPERVISOR_JIT.split("@")[1], None)
        self.supervisors = SupervisorAgent(
            supervisor_jid, consts.COMMON_PASSWORD, self.logger, SupervisorLogic(self.logger), consts.PLAN_PERIOD
        )

        self.agents: List[BaseAgent] = self.bins + self.trucks + self.landfills + [self.supervisors]

    def run(self):
        for agent in reversed(self.agents):
            agent.start().result()

        while True:
            self._step()
            self.logger.log("tiktok")
            time.sleep(1)

    def _step(self):
        for agent in self.agents:
            agent.step()
