from datetime import date

from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate
from loguru import logger
from neomodel import DoesNotExist
from neomodel import db
from starlette.responses import Response

from grenzeit.api.v1.models import CountryModel, TerritoryModel, CountryGetModel
from grenzeit.api.v1.schema import Country, Territory

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
)


@router.get('/', response_model=Page[CountryGetModel])
async def list_countries():
    """Paginated list of available countries"""
    # TODO inefficient for now and needs a new paginate function extension for neo4j
    countries = Country.nodes.all()
    return paginate([
        CountryGetModel(
            cluster=country.cluster[0].name,
            founded_at=country.founded_at,
            dissolved_at=country.dissolved_at,
            uid=country.uid,
            name_eng=country.name_eng,
            name_zeit=country.name_zeit,
        )
        for country in countries
    ])


@router.get("/world/{cluster}", )
async def world(cluster: str, show_date: date | None) -> list[CountryGetModel]:
    """Get countries in a cluster by date"""
    parsed_date = show_date.strftime("%Y-%m-%d")
    countries, meta = db.cypher_query(
        f"MATCH (t:Territory)-[rt:TERRITORY]-(z:Country)"
        f"-[:CLUSTER]->(c:Cluster {{name: '{cluster}'}})"
        f"WHERE rt.date_start <= '{parsed_date}' and (rt.date_end >= '{parsed_date}' or rt.date_end is null)"
        f" RETURN z, rt, c, t",
        resolve_objects=True
    )
    response = []
    for country, rel, cluster, terr in countries:
        # TODO: still too damn slow :(
        # gotta figure out a way to stream this somehow
        # leaning towards sockets for now
        territory = TerritoryModel(**terr.__dict__, date_start=rel.date_start)
        response.append(CountryGetModel(
            cluster=cluster.name,
            founded_at=country.founded_at,
            dissolved_at=country.dissolved_at,
            uid=country.uid,
            name_eng=country.name_eng,
            name_zeit=country.name_zeit,
            territory=territory
        ))

    return response


@router.post('/')
async def post_country(country: CountryModel):
    try:
        c = Country(**country.dict(by_alias=True, exclude={"territory"}))
        c.save()
        logger.debug(f'Country object created with ID: {c.uid}')
        if country.territory:
            t = Territory(geometry=country.territory.geometry.dict())
            t.save()
            logger.debug(f'Territory object created with ID: {t.uid}')
            rel = c.claims_territory.connect(t, {"date_end": country.territory.date_end,
                                                 "date_start": country.territory.date_start})
            rel.save()
        return Response(c.uid, status_code=200)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)


@router.put('/{country_id}')
async def update_country(country_id: str, country_data: CountryGetModel) -> Response:
    c = Country.nodes.get(uid=country_id)
    with db.transaction:
        for k, v in country_data.dict(exclude={"uid"}).items():
            setattr(c, k, v)
        c.save()
        return Response(status_code=200)


@router.get('/{country_id}', response_model=CountryGetModel)
async def get_country(country_id: str) -> CountryGetModel | Response:
    """Retrieve single Country object"""
    try:
        country = Country.nodes.get(uid=country_id)
        territory = country.claims_territory.get()
        rel = country.claims_territory.relationship(territory)
        territory.date_end = rel.date_end
        territory.date_start = rel.date_start
        c = CountryGetModel(
            cluster=country.cluster[0].name,
            founded_at=country.founded_at,
            dissolved_at=country.dissolved_at,
            uid=country.uid,
            name_eng=country.name_eng,
            name_zeit=country.name_zeit,
            territory=territory.__dict__
        )
        logger.info(f"Retrieved country object with id {country_id}")
        return c
    except DoesNotExist:
        logger.debug(f'Country with id {country_id} does not exist')
        return Response(None, status_code=404)


@router.delete('/{country_id}')
async def delete_country(country_id: str):
    try:
        Country.nodes.get(uid=country_id).delete()
        return Response(status_code=200)
    except DoesNotExist as e:
        logger.exception(e)
        return Response(e, status_code=404)


# @router.get('/{country}/territories', tags=['Territory'])
# async def claimed_territory(country: str, from_: datetime, to_: datetime):
#     pass


# @router.get('/{country}/territories/{territory}', tags=['Territory'])
# async def claimed_territory(country: str, territory):
#     pass


@router.post('/{country_id}/territories/', tags=['Territory'])
async def claimed_territory(country_id: str, territory: TerritoryModel):
    """Creates a territory that was claimed by the country"""
    c = Country.nodes.get(uid=country_id)
    try:
        t = Territory(geometry=territory.geometry.dict())
        t.save()
        logger.debug(f'Territory object created with ID: {t.uid}')
        rel = c.connect(t, {"date_end": territory.date_end, "date_start": territory.date_start})
        rel.save()
        return Response(t.uid, status_code=200)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)

# @router.get('/{country}/population/', tags=['Population'])
# async def population():
#     pass
