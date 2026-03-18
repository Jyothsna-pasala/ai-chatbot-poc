# from fastapi import APIRouter
# from app.services.service import metrics_service

# router = APIRouter()


# @router.get("/metrics/summary")
# async def metrics_summary():
#     return metrics_service.get_summary()


# @router.get("/metrics/trends")
# async def metrics_trends():
#     return metrics_service.get_trends()


from fastapi import APIRouter
from app.services.service import metrics_service

router = APIRouter(
    prefix="/api/metrics",
    tags=["Metrics"]
)


@router.get("/summary")
async def metrics_summary():
    return metrics_service.get_summary()


@router.get("/trends")
async def metrics_trends():
    return metrics_service.get_trends()