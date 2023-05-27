from fastapi import FastAPI

from grenzeit.api.v1.countries import router as countries
from fastapi_pagination import add_pagination
v1 = FastAPI(
    version="1.0.0",
    title="Grenzeit",
)

v1.include_router(countries)

add_pagination(v1)

@v1.get('/locales', tags=['locales'])
async def available_name_locales():
    raise NotImplementedError

