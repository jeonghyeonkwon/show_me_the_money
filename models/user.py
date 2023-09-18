from sqlalchemy import Column, Integer, String, DateTime, BigInteger

from db.database import Base
from dtos.user_response import UserResponse
from dtos.user_request import ReqAccessDto
from models.enum import ReqResult
from util.util import UtilService


# 유저
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    usableMoney = Column(BigInteger, default=0)

    @classmethod
    def create(cls, response: UserResponse):
        return cls(userId=response.userId, password=response.hashedPwd, usableMoney=0)


# 접근 로그
class UserAccessLog(Base):
    __tablename__ = "user_access_log"
    id = Column(Integer, primary_key=True, index=True)
    result = Column(String(50))
    accessIP = Column(String(50))
    userAgent = Column(String(50))
    created_at = Column(DateTime, default=UtilService.get_time())

    @classmethod
    def create(cls, result: ReqResult, req_data: ReqAccessDto):
        return cls(
            result=result.value,
            accessIP=req_data.accessIP,
            userAgent=req_data.userAgent,
        )
