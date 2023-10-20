from datetime import datetime, date
from typing import Optional

from geojson_pydantic import MultiPolygon, Polygon
from pydantic import BaseModel, Field


# class TerritoryType(Enum):
#     pass

class ReadOnlyIdMixin(BaseModel):
    """This is a model that implements a read-only id field"""
    uid: str | None


class TerritoryBase(BaseModel):
    date_start: date
    date_end: date | None
    geometry: MultiPolygon | Polygon


class TerritoryGetModel(TerritoryBase, ReadOnlyIdMixin):
    pass


class TerritoryModel(TerritoryBase):
    pass


class CountryBase(BaseModel):
    founded_at: datetime | date
    dissolved_at: Optional[datetime | date] = Field(
        description='When, if ever, the country stopped existing/changed its name etc.'
    )
    name_zeit: str = Field(description='Name of the country as it is/was called by its citizens')
    name_eng: str = Field(description='en_US name of the country')
    cluster: str | None = None
    territory: TerritoryModel | None


class CountryGetFrozenModel(CountryBase, ReadOnlyIdMixin):
    """Return a country object at a certain point in time

    This will return an object with properties that were applicable at a requested point in time
    """
    pass


class CountryGetFullModel(CountryBase, ReadOnlyIdMixin):
    """"""
    territories: list[TerritoryGetModel]

    class Config:
        fields = {'territory': {'exclude': True}}

class CountryModel(CountryBase):
    pass


class ClusterModel(BaseModel):
    uid: str | None
    name: str
    geometry: MultiPolygon | Polygon
    boundary: MultiPolygon | Polygon | None


class ClusterListModel(BaseModel):
    clusters: list[ClusterModel]


class GeometryBase(BaseModel):
    name: str
