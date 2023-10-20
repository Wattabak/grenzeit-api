from fastapi.routing import APIRouter

from grenzeit.api.v1.models import ClusterListModel, ClusterModel
from grenzeit.api.v1.schema import Cluster

router = APIRouter(
    prefix="/geometries",
    tags=["Geometry"],
)


# @router.post('/')
# async def create_geometry(geometry: GeometryBase):
#     try:
#         g = Geometry(
#             name=geometry.name,
#             geojson=
#         )
#         g.save()
#         logger.debug(f'Country object created with ID: {c.uid}')
#         if country.territory:
#             t = Territory(geometry=country.territory.geometry.dict())
#             t.save()
#             logger.debug(f'Territory object created with ID: {t.uid}')
#             rel = c.claims_territory.connect(t, {"date_end": country.territory.date_end,
#                                                  "date_start": country.territory.date_start})
#             rel.save()
#         return Response(c.uid, status_code=200)
#     except Exception as e:
#         logger.exception(e)
#         return Response(status_code=500)
#
#
# @router.get('/{country_id}', response_model=CountryGetModel)
# async def get_country(country_id: str) -> CountryGetModel | Response:
#     """Retrieve single Country object"""
#     try:
#         country = Country.nodes.get(uid=country_id)
#         territory = country.claims_territory.get()
#         rel = country.claims_territory.relationship(territory)
#         territory.date_end = rel.date_end
#         territory.date_start = rel.date_start
#         c = CountryGetModel(**country.__dict__, territory=territory.__dict__)
#         logger.info(f"Retrieved country object with id {country_id}")
#         return c
#     except DoesNotExist:
#         logger.debug(f'Country with id {country_id} does not exist')
#         return Response(None, status_code=404)

@router.get("/clusters")
async def get_clusters() -> ClusterListModel:
    return ClusterListModel(
        clusters=[
            ClusterModel(uid=cluster.uid, name=cluster.name, geometry=cluster.geometry)
            for cluster in Cluster.nodes.all()
        ]
    )
