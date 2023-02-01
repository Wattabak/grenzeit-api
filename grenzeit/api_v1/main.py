from fastapi import FastAPI

from grenzeit.api_v1.countries import router as countries

api_v1 = FastAPI(docs_url='/docs')

api_v1.include_router(countries)


@api_v1.get('/locales', tags=['locales'])
async def available_name_locales():
    raise NotImplementedError

