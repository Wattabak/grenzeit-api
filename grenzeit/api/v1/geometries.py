from fastapi.routing import APIRouter

from grenzeit.api.v1.models import ClusterListModel, ClusterModel
from grenzeit.api.v1.schema import Cluster

router = APIRouter(
    prefix="/geometries",
    tags=["Geometry"],
)


@router.get("/clusters")
async def get_clusters() -> ClusterListModel:
    return ClusterListModel(
        clusters=[
            ClusterModel(uid=cluster.uid, name=cluster.name, geometry=cluster.geometry)
            for cluster in Cluster.nodes.all()
        ]
    )
