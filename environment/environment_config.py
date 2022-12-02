from __future__ import annotations
from dataclasses import dataclass

from utils.cords import Cords


@dataclass
class BinData:
    position: Cords


@dataclass
class TruckData:
    starting_position: Cords


@dataclass
class LandfillData:
    position: Cords


class EnvironmentConfig:
    def __init__(self):
        self.bins_data = []
        self.trucks_data = []
        self.landfills_data = []
        pass

    @staticmethod
    def from_file(file_name: str) -> EnvironmentConfig:
        return EnvironmentConfig()
