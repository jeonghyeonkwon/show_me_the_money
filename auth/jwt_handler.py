from fastapi import HTTPException, status
from setting import settings
import time
from datetime import datetime
from jose import jwt, JWTError


def create_jwt(username: str) -> str:
    payload = {"username": username, "expires": time.time() + 3600}

    token = jwt.encode(payload, settings.jwt_secret, settings.jwt_algorithm)
    return token


def verify_jwt(token: str) -> bool:
    try:
        data = jwt.decode(token, settings.jwt_secret, settings.jwt_algorithm)
        expire = data.get("expires")
        if expire is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="접근 불가")
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="토큰 만료")
        return data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="접근 불가2")
