from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from core.db import Base
from enum import Enum as PyEnum


class Role(PyEnum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    USER = "user"


class Auth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    otp_secret = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)
