from utils.cords import Cords
from utils.logger import Logger


class BinLogic:
    def __init__(self, logger: Logger, position: Cords, fill_level_percentage: float = 0, max_volume: float = 100):
        self.position = Cords(position.x, position.y)
        self.fill_level_percentage = fill_level_percentage
        self.max_volume = max_volume
        self._logger = logger

    def add_rubbish(self, how_much: float) -> None:

        self.fill_level_percentage = min(self.fill_level_percentage + how_much, 1.0)
        if self.fill_level_percentage >= 1.0:
            self._logger.important_log(f"Bin is full!")

    def empty(self) -> None:
        self.fill_level_percentage = 0.0
