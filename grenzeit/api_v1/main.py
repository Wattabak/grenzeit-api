from fastapi import FastAPI

from grenzeit.api_v1.countries import router as countries

api_v1 = FastAPI(
    version="1.0.0",
    title="Grenzeit",

)

api_v1.include_router(countries)


@api_v1.get('/locales', tags=['locales'])
async def available_name_locales():
    raise NotImplementedError

