import bcrypt
import jwt
from dtos.user_response import UserResponse
from setting import settings
from datetime import datetime
from pytz import timezone


class UtilService:
    encoding: str = "UTF-8"

    def get_time() -> datetime:
        return datetime.now(timezone("Asia/Seoul"))

    def get_time_kor() -> str:
        now = datetime.now()
        date_string = now.strftime("%Y년%m월%d일%H시%M분%S초")
        return date_string

    def init_user(self):
        hassed_password: bytes = bcrypt.hashpw(
            settings.init_pwd.encode(self.encoding), salt=bcrypt.gensalt()
        )

        return UserResponse(settings.init_user, hassed_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding), hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {"username": username},
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

    def verify_jwt(self, token: str) -> bool:
        return jwt.decode(
            token,
            settings.jwt_secret,
        )
