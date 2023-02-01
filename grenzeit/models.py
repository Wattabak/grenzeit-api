from datetime import datetime, date
from enum import Enum
from typing import Optional, Any

from neomodel import NodeSet
from pydantic import BaseModel, Field
from shapely.geometry import MultiPolygon


class TerritoryType(Enum):
    pass


class CountryModel(BaseModel):
    uid: str
    founded_at: datetime | date
    dissolved_at: Optional[datetime] = Field(
        description='When, if ever, the country stopped existing/changed its name etc.'
    )
    name_zeit: str = Field(description='Name of the country as it is/was called by its citizens')
    name_eng: str = Field(description='en_US name of the country')

    def territory(self, edge_type: str = ''):
        pass


class Countries(BaseModel):
    countries: list[CountryModel]

    @classmethod
    def from_nodeset(cls, nodeset: NodeSet):
        return cls(
            countries=[
                CountryModel(**node) for node in nodeset
            ]
        )


class TerritoryModel(BaseModel):
    date_start: datetime | date
    date_end: datetime | date
    # geometry: MultiPolygon
