import logging
from typing import Union
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, id_tg: int) -> User:
        logging.info(id_tg)
        new_user = User(id_tg=id_tg)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_user_by_id_tg(self, id_tg: int) -> User:
        query = select(User).where(User.id_tg == id_tg)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_id(self, id_user: UUID) -> Union[User, None]:
        query = select(User).where(User.id == id_user)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user_by_tg_id(self, id_tg: int, **kwargs) -> Union[User, None]:
        query = update(User).where(User.id_tg == id_tg).values(kwargs).\
            returning(User.id_tg)
        res = await self.db_session.execute(query)
        updated_user_id_row = res.fetchone()
        if res is not None:
            return updated_user_id_row[0]
