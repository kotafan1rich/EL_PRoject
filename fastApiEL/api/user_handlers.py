from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ShowUser, UpdateUserResponse, UpdateUserRequest
from db.dals import UserDAL
from db.session import get_db

user_router = APIRouter()


async def _create_user(id_tg: int, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(db_session=session)
            user = await user_dal.create_user(id_tg)
            return ShowUser(
                id=user.id,
                id_tg=user.id_tg,
                # group_name=user.group_name,
                education_id=user.education_id,
                group_id=user.group_id,
                jwt_token=user.jwt_token,
            )


async def _get_user_by_tg_id(id_tg: int, db) -> Union[ShowUser, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(db_session=session)
            user = await user_dal.get_user_by_id_tg(id_tg)
            if user is not None:
                return ShowUser(
                    id=user.id,
                    id_tg=user.id_tg,
                    # group_name=user.group_name,
                    education_id=user.education_id,
                    group_id=user.group_id,
                    jwt_token=user.jwt_token,
                )


async def _get_user_by_id(user_id: UUID, db) -> Union[ShowUser, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id)
            if user is not None:
                return ShowUser(
                    id=user.id,
                    id_tg=user.id_tg,
                    # group_name=user.group_name,
                    education_id=user.education_id,
                    group_id=user.group_id,
                    jwt_token=user.jwt_token,
                )


async def _update_user_by_id_tg(update_user_params: dict, id_tg: int, db) -> UpdateUserResponse:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_id_tg = await user_dal.update_user_by_tg_id(id_tg, **update_user_params)
            return updated_id_tg


@user_router.post("/", response_model=ShowUser)
async def create_user(id_tg: int, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_user(id_tg, db)


@user_router.get("/by_id_tg", response_model=ShowUser)
async def get_user_by_id_tg(tg_id: int, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_tg_id(tg_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with tg_id {tg_id} already does not exists')
    return user


@user_router.get("/by_id", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} already does not exists')
    return user


@user_router.post("/update", response_model=UpdateUserResponse)
async def update_user_by_id_tg(id_tg: int, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)) -> UpdateUserResponse:
    update_user_params = body.dict(exclude_none=True)
    if update_user_params == {}:
        raise HTTPException(status_code=422)
    user = await _get_user_by_tg_id(id_tg, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with id {id_tg} already does not exists')
    updated_id_tg = await _update_user_by_id_tg(update_user_params=update_user_params, id_tg=id_tg, db=db)
    return UpdateUserResponse(updated_id_tg=updated_id_tg)
