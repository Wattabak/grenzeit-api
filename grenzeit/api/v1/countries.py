from datetime import date

from fastapi.routing import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate
from loguru import logger
from neomodel import DoesNotExist
from neomodel import db
from starlette.responses import Response

from grenzeit.api.v1.models import CountryModel, TerritoryModel, CountryGetFrozenModel, CountryGetFullModel, \
    TerritoryGetModel
from grenzeit.api.v1.schema import Country, Territory, Cluster

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
)


@router.get('/', response_model=Page[CountryGetFrozenModel])
async def list_countries():
    """Paginated list of available countries"""
    # TODO inefficient for now and needs a new paginate function extension for neo4j
    countries = Country.nodes.order_by('name_eng')
    return paginate([
        CountryGetFrozenModel(
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
async def world(cluster: str, show_date: date | None) -> list[CountryGetFrozenModel]:
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
        response.append(CountryGetFrozenModel(
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
        c = Country(**country.model_dump(by_alias=True, exclude={"territories", "cluster"}))
        cluster = Cluster.nodes.get(name=country.cluster)
        c.save()

        cluster_rel = c.cluster.connect(cluster)
        logger.debug(f'Country object {c.name_eng} created with ID: {c.uid} in cluster {cluster.name}')
        for territory in country.territories:
            t = Territory(geometry=territory.geometry.model_dump())
            t.save()
            logger.debug(f'Territory object created with ID: {t.uid}')
            rel = c.claims_territory.connect(t, {"date_end": territory.date_end,
                                                 "date_start": territory.date_start})
            rel.save()

        return Response(c.uid, status_code=200)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)


@router.put('/{country_id}')
async def update_country(country_id: str, country_data: CountryGetFullModel) -> Response:
    c = Country.nodes.get(uid=country_id)
    with db.transaction:
        for k, v in country_data.model_dump(exclude={"uid", "territories"}).items():
            setattr(c, k, v)
        for territory in country_data.territories:
            print(territory)
            t = Territory.nodes.get(uid=territory.uid)
            t.geometry = territory.geometry.model_dump()
            t.save()

            rel = c.claims_territory.relationship(t)
            rel.date_end = territory.date_end
            rel.date_start = territory.date_start
            rel.save()
        c.save()
        return Response(status_code=200)


@router.get('/{country_id}', response_model=CountryGetFrozenModel)
async def get_country(country_id: str, at_date: date | None = None) -> CountryGetFrozenModel | Response:
    """Retrieve a single country object at a certain point in time

    if at_date is missing, return latest territory
    """
    main_query = (f"MATCH (territory:Territory)-[terr_rel:TERRITORY]-(country:Country {{uid: '{country_id}'}})"
                  f"-[:CLUSTER]->(cluster:Cluster) ")
    condition = (f"WHERE terr_rel.date_start <= '{at_date}' "
                 f"and (terr_rel.date_end >= '{at_date}' or terr_rel.date_end is null) ")
    if not at_date:
        condition = ""
    data, meta = db.cypher_query(
        f"{main_query}"
        f"{condition}"
        f"RETURN country, terr_rel, territory, cluster",
        resolve_objects=True
    )

    country, terr_rel, territory, cluster = data[0]
    if not country:
        logger.debug(f'Country with id {country_id} does not exist')
        return Response(None, status_code=404)
    logger.info(f"Retrieved country object with id {country_id}")

    return CountryGetFrozenModel(
        uid=country.uid,
        cluster=cluster.name,
        founded_at=country.founded_at,
        dissolved_at=country.dissolved_at,
        name_eng=country.name_eng,
        name_zeit=country.name_zeit,
        territory=TerritoryModel(
            date_end=terr_rel.date_end,
            date_start=terr_rel.date_start,
            geometry=territory.geometry,
        )
    )


@router.get('/full/{country_id}', response_model=CountryGetFullModel)
async def get_full_country(country_id: str) -> CountryGetFullModel | Response:
    """Retrieves a country object with properties throughout existence of that country

    Basically as opposed to frozen it returns ALL territories, ALL flags and dates
    """
    data, meta = db.cypher_query(
        f"MATCH (country:Country {{uid: '{country_id}'}})"
        f"OPTIONAL MATCH (territories:Territory)-[terr_rels:TERRITORY]-(country)"
        f"OPTIONAL MATCH (country)-[:CLUSTER]->(cluster:Cluster) "
        f"RETURN country, collect(terr_rels), collect(territories), cluster",
        resolve_objects=True
    )
    if not data:
        return Response(None, status_code=404)

    country, terr_rels, territories, cluster = data[0]
    if not country:
        logger.debug(f'Country with id {country_id} does not exist')
        return Response(None, status_code=404)
    logger.info(f"Retrieved country object with id {country_id}")

    return CountryGetFullModel(
        cluster=cluster.name if cluster else None,
        founded_at=country.founded_at,
        dissolved_at=country.dissolved_at,
        uid=country.uid,
        name_eng=country.name_eng,
        name_zeit=country.name_zeit,
        territories=[
            TerritoryGetModel(
                uid=territory.uid,
                date_end=terr_rel.date_end,
                date_start=terr_rel.date_start,
                geometry=territory.geometry,
            )
            for territory, terr_rel in zip(territories[0], terr_rels[0])
        ]
    )


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
        t = Territory(geometry=territory.geometry.model_dump())
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
