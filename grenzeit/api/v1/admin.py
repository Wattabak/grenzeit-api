from fastapi.routing import APIRouter

from grenzeit.api.v1.models import CountryGetFullModel

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)



@router.get("/schema/full_country")
async def full_country_schema():
    return CountryGetFullModel.model_json_schema()
