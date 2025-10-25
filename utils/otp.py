from datetime import datetime, timedelta
import random


def otp_expiration_time(minutes: int = 5) -> datetime:
    return datetime.now() + timedelta(minutes=minutes)


def check_otp_expired(expiration_time: datetime) -> bool:
    return datetime.now() > expiration_time


def generate_otp(length: int = 6) -> str:
    if (length < 0):
        return ""

    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp
