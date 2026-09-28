from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.metrics_service import metrics_service
from app.schemas.schemas import AdminDashboardMetrics

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/stats", response_model=AdminDashboardMetrics)
async def get_admin_stats(db: AsyncSession = Depends(get_db)):
    return await metrics_service.get_dashboard_metrics(db)
