from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import MarksResult, UserPeriodsResponse, UserPeriodRequest
from api.services import Mark
from db.dals import UserDAL
from db.session import get_db


marks_router = APIRouter()


def __get_marks_by_period(date_from: str, date_to: str, education_id: int, group_id, jwt_token: str, period_id: int) -> Union[dict, None]:
    if jwt_token is not None and education_id:
        mark = Mark(jwt_token=jwt_token)
        data = mark.get_marks(date_from=date_from, date_to=date_to, education_id=education_id, group_id=group_id, period_id=period_id)
        return data
    return {}


async def _get_marks_by_period(id_tg: int, date_from: str, date_to: str, period_id: int, db) -> MarksResult:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(db_session=session)
            user = await user_dal.get_user_by_id_tg(id_tg)
            education_id: int = user.education_id
            group_id: int = user.group_id
            jwt_token: str = user.jwt_token
            marks = __get_marks_by_period(date_from, date_to, education_id, group_id, jwt_token, period_id)
            return MarksResult(
                result=marks
            )


async def _get_user_periods(id_tg: int, db) -> UserPeriodRequest:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(db_session=session)
            user_info = await user_dal.get_user_by_id_tg(id_tg=id_tg)
            group_id: int = user_info.group_id
            jwt_token: str = user_info.jwt_token
            periods = Mark(jwt_token=jwt_token).get_periods(group_id=group_id) if group_id and jwt_token else {}

            return UserPeriodsResponse(result=periods)


@marks_router.get("/", response_model=MarksResult)
async def get_marks_by_period(id_tg: int, date_from: str, date_to: str, period_id: int, db: AsyncSession = Depends(get_db)):
    res = await _get_marks_by_period(id_tg, date_from, date_to, period_id, db)
    return res


@marks_router.get("/get_user_periods", response_model=UserPeriodsResponse)
async def get_user_periods(id_tg: int, db: AsyncSession = Depends(get_db)):
    res: dict = await _get_user_periods(id_tg, db)
    return res
