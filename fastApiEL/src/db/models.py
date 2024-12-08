import uuid

from sqlalchemy import Column, VARCHAR, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_tg = Column(BigInteger, nullable=False, unique=True)
    education_id = Column(BigInteger, nullable=True)
    group_id = Column(BigInteger, nullable=True)
    jwt_token = Column(VARCHAR, nullable=True)
    
