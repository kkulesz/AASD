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
import consts


class Environment:
    def __init__(self, config: EnvironmentConfig, logger: Logger):
        self.logger = logger

        bins_jid = JID(consts.BIN1_JIT.split('@')[0], consts.BIN1_JIT.split('@')[1], None)
        self.bins = [
            BinAgent(
                bins_jid, consts.COMMON_PASSWORD, consts.SUPERVISOR_JIT, consts.BIN_INFORM_PERIOD, self.logger,
                BinLogic(position=data.position, fill_level_percentage=data.start_bin_level, logger=self.logger)
            ) for i, data in enumerate(config.bins_data)
        ]

        self.trucks = []
        self.landfills = []
        supervisor_jid = JID(consts.SUPERVISOR_JIT.split('@')[0], consts.SUPERVISOR_JIT.split('@')[1], None)
        self.supervisors = SupervisorAgent(supervisor_jid,
            consts.COMMON_PASSWORD,
            self.logger, SupervisorLogic()
        )

        self.agents: List[BaseAgent] = self.bins + self.trucks + self.landfills + [self.supervisors]

    def run(self):
        for agent in reversed(self.agents):
            print(agent.jid)
            agent.start().result()

        while True:
            self._step()
            self.logger.log("tiktok")
            time.sleep(1)

    def _step(self):
        for agent in self.agents:
            agent.step()
