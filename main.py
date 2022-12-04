from utils.logger import DummyLogger, ConsoleLogger
from environment.environment_config import EnvironmentConfig
from environment.environment import Environment

###########3
from utils.cords import Cords
from protocols.base_message import BaseMessage
from protocols.bin_state.inform_about_bin_state import InformAboutBinState

if __name__ == '__main__':
    system_logger = ConsoleLogger()

    config = EnvironmentConfig.from_file('config.json')
    env = Environment(config, system_logger)

    # env.run()

    ############################################3
    msg = InformAboutBinState(fill_level_percentage=10, position=Cords(0, 0))
    print(msg.json())
    print(msg.get_metadata())
    spade_msg = msg.to_spade("to", "sender")
    print(spade_msg.sender)

    cycle_msg = BaseMessage.parse(spade_msg)
    print("=" * 30)
    print(cycle_msg.json())
    print(cycle_msg.fill_level_percentage)
    print(cycle_msg.get_metadata())
