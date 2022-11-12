from fastapi import Depends
from fastapi.routing import APIRouter

from .deps import require_basic_auth
from .endpoints import radarr, sonarr

router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(require_basic_auth)],
)

router.include_router(radarr.router)
router.include_router(sonarr.router)
