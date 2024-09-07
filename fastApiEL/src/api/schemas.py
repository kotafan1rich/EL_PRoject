import uuid
from typing import Union

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class UpdateUserResponse(TunedModel):
    updated_id_tg: int


class UpdateUserRequest(TunedModel):
    user_id: Union[None, int] = None
    education_id: Union[None, int] = None
    group_id: Union[None, int] = None
    jwt_token: Union[None, str] = None


class ShowUser(TunedModel):
    id: uuid.UUID
    id_tg: int
    education_id: Union[None, int]
    group_id: Union[None, int]
    jwt_token: Union[None, str]


class MarksResult(TunedModel):
    result: dict


class UserPeriodsResponse(TunedModel):
    result: dict


class UserPeriodRequest(TunedModel):
    id_tg: int
    group_id: int
