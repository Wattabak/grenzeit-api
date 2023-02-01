from datetime import datetime

from fastapi import Query
from fastapi.routing import APIRouter
from loguru import logger
from neomodel import DoesNotExist
from starlette.responses import Response

from grenzeit.models import Countries, CountryModel, TerritoryModel
from grenzeit.schema import Country

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],

)


@router.get('/', response_model=Countries)
async def get_countries() -> Countries:
    # paginate
    return Countries.from_nodeset(Country.nodes.all())


@router.get('/{country}', response_model=CountryModel)
async def get_country(country: str = Query(max_length=16)) -> CountryModel | Response:
    """

    :param country:
    :type country: hex string
    :return:
    :rtype:
    """
    try:
        return CountryModel(**Country.nodes.get(uid=country))
    except DoesNotExist:
        logger.debug(f'Queried country node with id {country} does not exist')
        return Response(None, status_code=404)


@router.post('/')
async def post_country(country: CountryModel):
    try:
        c = Country(**country.dict(by_alias=True))
        c.save()
        logger.debug(f'Country object created with ID: {c.uid}')
        return Response(c.uid, status_code=200)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)


@router.put('/')
async def update_country(country: CountryModel):
    c = Country.nodes.get(uid=country.uid)
    c.update(**country.dict())


@router.delete('/{country}')
async def delete_country(country: str):
    try:
        Country.nodes.get(uid=country).delete()
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)
    return Response(status_code=200)


@router.get('/{country}/territories', tags=['Territory'])
async def claimed_territory(country: str, from_: datetime, to_: datetime):
    pass


@router.get('/{country}/territories/{territory}', tags=['Territory'])
async def claimed_territory(country: str, territory):
    pass


@router.post('/{country}/territories/', tags=['Territory'])
async def claimed_territory(country: str, territory: TerritoryModel):
    pass


@router.get('/{country}/population/', tags=['Population'])
async def population():
    pass
