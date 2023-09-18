from enum import Enum


class DeviceType(Enum):
    안드로이드 = "ANDROID"
    IOS = "IOS"
    윈도우 = "WINDOW"
    맥 = "MAC"


class TradeType(Enum):
    구매 = "BUY"
    판매 = "SEL"


class ReqResult(Enum):
    접속 = "SUCCESS"
    아이디_없음 = "NOT_USER"
    비밀번호_틀림 = "NOT_MATCH_PASSWORD"


class LogType(Enum):
    NAVER_SEARCH = "네이버 검색"
    UPBIT_TOTAL = "업비트 코인 검색"


class CandleType(Enum):
    MONTH = "months"
    WEEK = "weeks"
    DAY = "days"
