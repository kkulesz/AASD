from utils.cords import Cords
from utils.logger import Logger


class BinLogic:
    def __init__(self, position: Cords, fill_level_percentage: int, logger: Logger):
        self._position = position
        self._fill_level_percentage = fill_level_percentage
        self._logger = logger

    def add_rubbish(self, how_much: int) -> None:
        self._fill_level_percentage += how_much
        if self._fill_level_percentage >= 100:
            self._logger.important_log(f"Bin is full! Overfilling... {self._fill_level_percentage}%")

    def empty(self) -> None:
        self._fill_level_percentage = 0

    def get_fill_level(self) -> int:
        return self._fill_level_percentage

    def get_position(self) -> Cords:
        return self._position
