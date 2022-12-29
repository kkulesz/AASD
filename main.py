from utils.logger import ConsoleLogger, SilentLogger
from environment.environment_config import EnvironmentConfig
from environment.environment import Environment


if __name__ == "__main__":
    system_logger = ConsoleLogger()

    config = EnvironmentConfig.from_file("config.json")
    # print(f"config = {config.json(indent=2, sort_keys=True)}")
    env = Environment(config, system_logger)

    env.run()
