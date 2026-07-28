from fastapi import APIRouter

from src.analytics.metrics import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

analytics = AnalyticsService()


@router.get("/metrics")
def analytics_metrics():

    return analytics.get_metrics()