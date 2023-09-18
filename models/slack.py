from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

from datetime import datetime

from db.database import Base
from util.util import UtilService


class SlackLog(Base):
    __tablename__ = "slack_log"
    id = Column(Integer, primary_key=True, index=True)
    memo = Column(String(500))
    created_at = Column(DateTime, default=UtilService.get_time())

    @classmethod
    def create(cls, keyword: str, value: str):
        return cls(memo=f"슬랙 보냄 -> keyword : {keyword} -> value : {value}")
