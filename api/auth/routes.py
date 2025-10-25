from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from core.db import db_dependency
from models.auth import Auth, Role
from utils import hash, otp
from .schemas import (
    ChangePasswordPayload,
    CheckOTPPayload,
    LoginPayload,
    RegisterPayload,
    OtpRequestPayload,
    ResetPasswordPayload
)

router = APIRouter(prefix="/auth")


def get_user_by_email(db, email: str):
    return db.query(Auth).where(Auth.email == email).first()


def response_user(user: Auth):
    return {
        "email": user.email,
        "role": str(user.role),
        "is_verified": user.is_verified
    }


@router.post("/login")
async def login_endpoint(body: LoginPayload, db: db_dependency):
    user = get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not hash.compare_password(
        body.password,
        user.hashed_password  # type: ignore
    ):
        raise HTTPException(status_code=401, detail="Wrong Password")

    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "Login successful",
                 "user": response_user(user)}
    )


@router.post("/register")
async def register_endpoint(body: RegisterPayload, db: db_dependency):
    user = Auth(
        email=body.email,
        hashed_password=hash.hash_password(body.password),
        role=Role.USER
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        msg = str(e.orig)
        detail = "Database error occurred"
        if "unique constraint" in msg and "email" in msg:
            detail = "Email already exists."
        raise HTTPException(status_code=400, detail=detail)

    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "Register successful",
                 "user": response_user(user)}
    )


@router.post("/request-otp")
async def request_otp_endpoint(body: OtpRequestPayload, db: db_dependency):
    user = get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.otp_secret = otp.generate_otp(6)
    user.otp_expiry = otp.otp_expiration_time()

    try:
        db.commit()
    except IntegrityError as e:
        raise HTTPException(
            status_code=500, detail="Failed to send OTP") from e

    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "OTP sent successfully",
                 "OTP": user.otp_secret}
    )


@router.post("/check-otp")
async def check_otp(body: CheckOTPPayload, db: db_dependency):
    user = get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if otp.check_otp_expired(user.otp_expiry):
        raise HTTPException(status_code=401, detail="OTP expired")

    if body.otp != user.otp_secret:
        raise HTTPException(status_code=401, detail="OTP mismatch")

    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "OTP matched"}
    )


@router.post("/reset-password")
async def reset_password(body: ResetPasswordPayload, db: db_dependency):
    user = get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if otp.check_otp_expired(user.otp_expiry):
        raise HTTPException(status_code=401, detail="OTP expired")

    if body.otp != user.otp_secret:
        raise HTTPException(status_code=401, detail="OTP mismatch")

    user.hashed_password = hash.hash_password(body.password)  # type: ignore
    user.otp_secret = None  # type: ignore
    user.otp_expiry = None  # type: ignore

    db.commit()

    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "Password reset successful"}
    )


@router.post("/change-password")
async def change_password(
    body: ChangePasswordPayload,
    db: db_dependency,
):
    user = get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not hash.compare_password(
            body.password,
            user.hashed_password  # type: ignore
    ):
        raise HTTPException(
            status_code=401, detail="Current password is incorrect")

    user.hashed_password = hash.hash_password(  # type: ignore
        body.new_password)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"status": True, "message": "Password changed successfully"}
    )


@router.post("/verify-account")
async def verify_account(body: CheckOTPPayload, db: db_dependency):
    user = get_user_by_email(db, body.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if otp.check_otp_expired(user.otp_expiry):
        raise HTTPException(status_code=401, detail="OTP expired")

    if body.otp != user.otp_secret:
        raise HTTPException(status_code=401, detail="OTP mismatch")

    user.is_verified = True  # type: ignore
    user.otp_secret = None  # type: ignore
    user.otp_expiry = None  # type: ignore

    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "message": "Account verified successfully"
        }
    )
