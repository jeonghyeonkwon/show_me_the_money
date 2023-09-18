from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

from db.database import Base
from util.util import UtilService


# 코인
class Coin(Base):
    __tablename__ = "coin"
    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(20), nullable=False)
    korean_name = Column(String(20), nullable=False)
    english_name = Column(String(30), nullable=False)
    type = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=UtilService.get_time())

    @classmethod
    def create(cls, market: str, korean_name: str, english_name: str):
        type = market.split("-")[0]

        return cls(
            market=market, korean_name=korean_name, english_name=english_name, type=type
        )


# 코인 트레이드 로그
class CoinTradeLog(Base):
    __tablename__ = "coin_trade_log"
    id = Column(Integer, primary_key=True, index=True)
    tade_type = Column(String(10), nullable=False)
    count = Column(Float)
    created_at = Column(DateTime, default=UtilService.get_time())
