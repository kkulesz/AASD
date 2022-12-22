from __future__ import annotations
from typing import List
from pydantic import BaseModel
import json

from utils.cords import Cords


class BinData(BaseModel):
    position: Cords
    start_bin_level: float


class TruckData(BaseModel):
    starting_position: Cords


class LandfillData(BaseModel):
    position: Cords
    jid: str


class SupervisorData(BaseModel):
    pass


class EnvironmentConfig(BaseModel):
    bins_data: List[BinData]
    trucks_data: List[TruckData]
    landfills_data: List[LandfillData]
    supervisor_data: SupervisorData

    @staticmethod
    def from_file(file_name: str) -> EnvironmentConfig:
        f = open(file_name, "r")
        file_content = f.read()
        params = json.loads(file_content)
        return EnvironmentConfig(**params)
