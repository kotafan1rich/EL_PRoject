from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import MarksResult, UserPeriodsResponse
from src.db.session import get_db

from .crud import MarksCRUD

marks_router = APIRouter()


@marks_router.get("/", response_model=MarksResult)
async def get_marks_by_period(
	id_tg: int,
	date_from: str,
	date_to: str,
	period_id: int,
	db: AsyncSession = Depends(get_db),
):  
	return await MarksCRUD.get_marks_by_period(id_tg, date_from, date_to, period_id, db)


@marks_router.get("/get_user_periods", response_model=UserPeriodsResponse)
async def get_user_periods(id_tg: int, db: AsyncSession = Depends(get_db)):
	return await MarksCRUD.get_user_periods(id_tg, db)
