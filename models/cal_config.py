from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from db.database import Base
from util.util import UtilService


# 현재 계산 방식
class CalConfig(Base):
    __name__ = "cal_config"
    # 원화로 보유할 금액
    holdMoney = Column(BigInteger, default=0, nullable=False)
    # 1회 최대 투자 금액
    oneTimeMaximumInvest = Column(BigInteger, default=0, nullable=False)
    # 코인 최대 수익율
    oneCoinMaxRateOfReturn = Column(Float, default=0, nullable=False)
    # 코인 최소 수익율
    oneCoinMinRateOfReturn = Column(Float, default=0, nullable=False)
    # 상향 비율
    upperRate = Column(Float, default=0, nullable=False)
    # 하양 비율
    underRate = Column(Float, default=0, nullable=False)

    memo = Column(String(500))


# 계산 방식 로그
class CalConfigLog(Base):
    __name__ = "cal_config_log"
    id = Column(Integer, primary_key=True, index=True)
    # 원화로 보유할 금액
    holdMoney = Column(BigInteger, default=0, nullable=False)
    # 1회 최대 투자 금액
    oneTimeMaximumInvest = Column(BigInteger, default=0, nullable=False)
    # 코인 최대 수익율
    oneCoinMaxRateOfReturn = Column(Float, default=0, nullable=False)
    # 코인 최소 수익율
    oneCoinMinRateOfReturn = Column(Float, default=0, nullable=False)
    # 상향 비율
    upperRate = Column(Float, default=0, nullable=False)
    # 하양 비율
    underRate = Column(Float, default=0, nullable=False)

    created_at = Column(DateTime, default=UtilService.get_time())
