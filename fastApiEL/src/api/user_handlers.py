from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ShowUser, UpdateUserRequest, UpdateUserResponse
from src.db.session import get_db

from .crud import UserCRUD

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(id_tg: int, db: AsyncSession = Depends(get_db)) -> ShowUser:
	return await UserCRUD.create_user(id_tg, db)


@user_router.get("/by_id_tg", response_model=ShowUser)
async def get_user_by_id_tg(tg_id: int, db: AsyncSession = Depends(get_db)) -> ShowUser:
	user = await UserCRUD.get_user_by_tg_id(tg_id, db)
	if user is None:
		raise HTTPException(
			status_code=404, detail=f"User with tg_id {tg_id} already does not exists"
		)
	return user


@user_router.get("/by_id", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
	user = await UserCRUD.get_user_by_id(user_id, db)
	if user is None:
		raise HTTPException(
			status_code=404, detail=f"User with id {user_id} already does not exists"
		)
	return user


@user_router.post("/update", response_model=UpdateUserResponse)
async def update_user_by_id_tg(
	id_tg: int, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)
) -> UpdateUserResponse:
	update_user_params = body.dict(exclude_none=True)
	if update_user_params == {}:
		raise HTTPException(status_code=422)
	user = await UserCRUD.get_user_by_tg_id(id_tg, db)
	if user is None:
		raise HTTPException(
			status_code=404, detail=f"User with id {id_tg} already does not exists"
		)
	updated_id_tg = await UserCRUD.update_user_by_id_tg(
		update_user_params=update_user_params, id_tg=id_tg, db=db
	)
	return UpdateUserResponse(updated_id_tg=updated_id_tg)


@user_router.delete("/delete", response_model=UpdateUserResponse)
async def delete_user_by_id_tg(id_tg: int, db: AsyncSession = Depends(get_db)) -> UpdateUserResponse:
	return await UserCRUD.delete_user_by_id_tg(id_tg=id_tg, db=db)
