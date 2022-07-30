from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TerritoryType(Enum):
    pass


class CountryModel(BaseModel):
    _id: int = Field(alias="id")
    founded_at: datetime
    dissolved_at: datetime
    name_zeit: str
    name_eng: str

    def territory(self, edge_type: str = ''):
        pass

