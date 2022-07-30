from fastapi import FastAPI, Response

from grenzeit.config import logger
from grenzeit.models import CountryModel
from grenzeit.schema import Country

api_v1 = FastAPI(docs_url="/docs")


@api_v1.get("/locales")
async def available_name_locales():
    return {

    }


@api_v1.get("/countries")
async def get_countries():
    return await Country.nodes.all()


@api_v1.post("/countries")
async def post_countries(country: CountryModel):
    try:
        country = Country(**country.dict())
        country.save()
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)
    return Response(status_code=200)
