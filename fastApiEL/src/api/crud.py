from typing import Union
from uuid import UUID

import aiohttp
from fastapi import HTTPException

from .schemas import (
	MarksResult,
	ShowUser,
	UpdateUserResponse,
	UserPeriodRequest,
	UserPeriodsResponse,
)
from .services import Mark
from src.db.dals import UserDAL


class MarksCRUD:
	@staticmethod
	async def get_marks_by_period(
		id_tg: int, date_from: str, date_to: str, period_id: int, db
	) -> MarksResult:
		async with db as session:
			async with session.begin():
				user_dal = UserDAL(db_session=session)
				user = await user_dal.get_user_by_id_tg(id_tg)
				education_id: int = user.education_id
				jwt_token: str = user.jwt_token
				if jwt_token is not None and education_id:
					session = aiohttp.ClientSession()
					mark = Mark(jwt_token=jwt_token, session=session)
					group_id: int = user.group_id
					marks = await mark.get_marks(
						date_from=date_from,
						date_to=date_to,
						education_id=education_id,
						group_id=group_id,
						period_id=period_id,
					)
					await session.close()
					return MarksResult(result=marks)
				raise HTTPException(status_code=404, detail="No data")

	@staticmethod
	async def get_user_periods(id_tg: int, db) -> UserPeriodRequest:
		async with db as session:
			async with session.begin():
				user_dal = UserDAL(db_session=session)
				user_info = await user_dal.get_user_by_id_tg(id_tg=id_tg)
				group_id: int = user_info.group_id
				jwt_token: str = user_info.jwt_token
				session = aiohttp.ClientSession()
				periods = (
					await Mark(jwt_token=jwt_token, session=session).get_periods(
						group_id=group_id
					)
					if group_id and jwt_token
					else {}
				)
				await session.close()
				return UserPeriodsResponse(result=periods)


class UserCRUD:
	@staticmethod
	async def create_user(id_tg: int, db) -> ShowUser:
		async with db as session:
			async with session.begin():
				user_dal = UserDAL(db_session=session)
				user = await user_dal.create_user(id_tg)
				return ShowUser.model_validate(user, from_attributes=True)

	@staticmethod
	async def get_user_by_tg_id(id_tg: int, db) -> Union[ShowUser, None]:
		async with db as session:
			async with session.begin():
				user_dal = UserDAL(db_session=session)
				user = await user_dal.get_user_by_id_tg(id_tg)
				if user is not None:
					return ShowUser.model_validate(user, from_attributes=True)

	@staticmethod
	async def get_user_by_id(user_id: UUID, db) -> Union[ShowUser, None]:
		async with db as session:
			async with session.begin():
				user_dal = UserDAL(session)
				user = await user_dal.get_user_by_id(user_id)
				if user is not None:
					return ShowUser.model_validate(user, from_attributes=True)

	@staticmethod
	async def update_user_by_id_tg(
		update_user_params: dict, id_tg: int, db
	) -> UpdateUserResponse:
		async with db as session:
			async with session.begin():
				user_dal = UserDAL(session)
				return await user_dal.update_user_by_tg_id(id_tg, **update_user_params)
