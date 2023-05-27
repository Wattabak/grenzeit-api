from fastapi import Query
from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate
from loguru import logger
from neomodel import DoesNotExist
from starlette.responses import Response

from grenzeit.api.v1.models import CountryModel
from grenzeit.api.v1.schema import Country

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
)


@router.get('/', response_model=Page[CountryModel])
async def list_countries():
    """Paginated list of available countries"""
    # TODO inefficient for now and needs a new paginate function extension for neo4j
    countries = Country.nodes.all()
    print(countries[0])
    pages = paginate([CountryModel(**country.__dict__) for country in countries])
    return pages


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


@router.get('/{country}', response_model=CountryModel)
async def get_country(country: int) -> CountryModel | Response:
    """Retrieve single Country object"""
    try:
        return CountryModel(**Country.nodes.get(uid=country).__dict__)
    except DoesNotExist:
        logger.debug(f'Country with id {country} does not exist')
        return Response(None, status_code=404)


@router.delete('/{country}')
async def delete_country(country: str):
    try:
        Country.nodes.get(uid=country).delete()
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)
    return Response(status_code=200)


# @router.get('/{country}/territories', tags=['Territory'])
# async def claimed_territory(country: str, from_: datetime, to_: datetime):
#     pass
#
#
# @router.get('/{country}/territories/{territory}', tags=['Territory'])
# async def claimed_territory(country: str, territory):
#     pass
#
#
# @router.post('/{country}/territories/', tags=['Territory'])
# async def claimed_territory(country: str, territory: TerritoryModel):
#     pass
#
#
# @router.get('/{country}/population/', tags=['Population'])
# async def population():
#     pass
