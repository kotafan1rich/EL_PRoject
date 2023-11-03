from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import MarksResult
from api.services import Mark
from db.dals import UserDAL
from db.session import get_db


marks_router = APIRouter()


def __get_marks_by_period(date_from: str, date_to: str, education_id: int, group_id, jwt_token: str) -> Union[dict, None]:
    mark = Mark()
    if jwt_token is not None and education_id:
        data = mark.get_marks(date_from=date_from, date_to=date_to, education_id=education_id, group_id=group_id, jwt_token=jwt_token)
        if data:
            res = mark.sort_marks(data, date_from=date_from, date_to=date_to)
            return res
        return data
    return {}


async def _get_marks_by_period(id_tg: int, date_from: str, date_to: str, db) -> MarksResult:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(db_session=session)
            user = await user_dal.get_user_by_id_tg(id_tg)
            education_id: int = user.education_id
            group_id: int = user.group_id
            jwt_token: str = user.jwt_token
            marks = __get_marks_by_period(date_from, date_to, education_id, group_id, jwt_token)
            return MarksResult(
                result=marks
            )


@marks_router.get("/", response_model=MarksResult)
async def get_marks_by_period(id_tg: int, date_from: str, date_to: str, db: AsyncSession = Depends(get_db)):
    res = await _get_marks_by_period(id_tg, date_from, date_to, db)
    return res
