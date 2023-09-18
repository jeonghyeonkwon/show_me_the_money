from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
import uuid
from db.database import Base
from util.util import UtilService


# 월 데이터
class MonthCandle(Base):
    __tablename__ = "month_candle"
    id = Column(Integer, primary_key=True, index=True)
    target_date = Column(DateTime, nullable=False)
    market = Column(String(20), nullable=False)
    opening_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    trade_price = Column(Float, nullable=False)
    volumn = Column(Float, nullable=False)
    coin_type = Column(String(10), nullable=False)

    @classmethod
    def create(
        cls,
        target_date: DateTime,
        market: str,
        opening_price: float,
        high_price: float,
        low_price: float,
        trade_price: float,
        volumn: float,
    ):
        coin_type = market.split("-")[0]
        return cls(
            target_date=target_date,
            market=market,
            opening_price=opening_price,
            high_price=high_price,
            low_price=low_price,
            trade_price=trade_price,
            volumn=volumn,
            coin_type=coin_type,
        )
