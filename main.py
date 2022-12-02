from utils.logger import DummyLogger, ConsoleLogger
from environment.environment_config import EnvironmentConfig
from environment.environment import Environment

if __name__ == '__main__':
    system_logger = ConsoleLogger()

    config = EnvironmentConfig.from_file('config.json')
    env = Environment(config, system_logger)

    env.run()
