import time
from typing import List

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

        self.bins = [
            BinAgent(
                f"{i+1}@bin", consts.COMMON_PASSWORD, consts.SUPERVISOR_JIT, consts.BIN_INFORM_PERIOD, self.logger,
                BinLogic(position=data.position, fill_level_percentage=data.start_bin_level, logger=self.logger)
            ) for i, data in enumerate(config.bins_data)
        ]

        self.trucks = []
        self.landfills = []
        self.supervisors = SupervisorAgent(
            consts.SUPERVISOR_JIT, consts.COMMON_PASSWORD,
            self.logger, SupervisorLogic()
        )

        self.agents: List[BaseAgent] = self.bins + self.trucks + self.landfills + [self.supervisors]

    def run(self):
        # TODO: uncomment when server is available
        # for agent in self.agents:
        #     agent.start().result()

        while True:
            self._step()
            self.logger.log("tiktok")
            time.sleep(1)

    def _step(self):
        for agent in self.agents:
            agent.step()
