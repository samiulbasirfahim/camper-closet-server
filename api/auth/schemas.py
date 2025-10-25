from pydantic import BaseModel, EmailStr
from typing import Annotated
from fastapi import Query


class AuthBase(BaseModel):
    email: EmailStr
    password: Annotated[str, Query(min_length=8)]


class RegisterPayload(AuthBase):
    pass


class LoginPayload(AuthBase):
    pass


class OtpRequestPayload(BaseModel):
    email: EmailStr


class CheckOTPPayload(BaseModel):
    email: EmailStr
    otp: Annotated[str, Query(min_length=6, max_length=6)]


class ResetPasswordPayload(CheckOTPPayload):
    password: Annotated[str, Query(min_length=8)]


class ChangePasswordPayload(AuthBase):
    new_password: Annotated[str, Query(min_length=8)]
