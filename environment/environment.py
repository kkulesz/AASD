import time

from environment.environment_config import EnvironmentConfig
from utils.logger import Logger
from agents.bin import Bin


class Environment:
    def __init__(self, config: EnvironmentConfig, logger: Logger):
        self.bins = [
            Bin("test@test", "password", logger)
        ]
        self.trucks = []
        self.landfills = []
        self.supervisors = []

        self.agents = self.bins + self.trucks + self.landfills + self.supervisors

    def run(self):
        for agent in self.agents:
            agent.start().result()

        while True:
            self._step()
            print("tiktok")
            time.sleep(1)

    def _step(self):
        pass
