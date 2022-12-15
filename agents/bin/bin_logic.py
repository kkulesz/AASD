from utils.cords import Cords
from utils.logger import Logger


class BinLogic:
    def __init__(self, logger: Logger, position: Cords, fill_level_percentage: int = 0, max_volume: int = 100):
        self.position = position
        self.fill_level_percentage = fill_level_percentage
        self.max_volume = max_volume
        self._logger = logger

    def add_rubbish(self, how_much: int) -> None:
        self.fill_level_percentage += how_much
        if self.fill_level_percentage >= 100:
            self._logger.important_log(f"Bin is full! Overfilling... {self.fill_level_percentage}%")

    def empty(self) -> None:
        self.fill_level_percentage = 0
