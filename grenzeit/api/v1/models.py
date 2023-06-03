from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field


# class TerritoryType(Enum):
#     pass


class CountryModel(BaseModel):
    uid: str | None
    founded_at: datetime | date
    dissolved_at: Optional[datetime | date] = Field(
        description='When, if ever, the country stopped existing/changed its name etc.'
    )
    name_zeit: str = Field(description='Name of the country as it is/was called by its citizens')
    name_eng: str = Field(description='en_US name of the country')

# class TerritoryModel(BaseModel):
#     date_start: datetime | date
#     date_end: datetime | date
#     # geometry: MultiPolygon
