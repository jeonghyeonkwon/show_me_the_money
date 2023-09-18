import requests
from fastapi import APIRouter, Depends
from models.coin import Coin
from repository.coin_repository import CoinRepository
from repository.candle_repository import CandleRepository
from slackApi.slack import sendMessage
from dtos.coin_response import NewCoinResponse
from models.candle import MonthCandle
from models.enum import CandleType
from fastapi.responses import StreamingResponse
import cv2
from fastapi.responses import JSONResponse
import io
import base64
from PIL import Image

router = APIRouter()

UPBIT_API = "https://api.upbit.com/v1"
headers = {"accept": "application/json"}

# 코인 이름 조회
COIN_NAME = f"{UPBIT_API}/market/all?isDetails=false"


def select_candle(candle_type: str, market: str):
    return f"{UPBIT_API}/candles/{candle_type}?count=200&market={market}"


# 월별 조회
MONTH_CANDLE = select_candle(CandleType.MONTH.value, "KRW-BTC")

# 주별 조회
WEEK_CANDLE = select_candle(CandleType.WEEK.value, "KRW-BTC")

# 일별 조회
DAY_CANDLE = select_candle(CandleType.DAY.value, "KRW-BTC")


@router.get("/total")
async def total(coinRepo: CoinRepository = Depends()):
    response = requests.get(COIN_NAME, headers=headers).json()
    coin_list = []
    for item in response:
        market = item["market"]
        korean_name = item["korean_name"]
        english_name = item["english_name"]
        coin: Coin = Coin.create(market, korean_name, english_name)
        coin_list.append(coin)

    new_list = coinRepo.create(coin_list)
    for obj in new_list:
        dto = NewCoinResponse(obj.market, obj.korean_name, obj.english_name, obj.type)
        # sendMessage(dto.toTemplate())
    return response


@router.get("/month")
async def month(month_repo: CandleRepository = Depends()):
    response = requests.get(MONTH_CANDLE, headers=headers).json()
    list = []
    for item in response:
        market = item["market"]
        coin_type = market.split("-")[0]
        if coin_type == "KRW":
            target_date = item["candle_date_time_kst"]
            opening_price = item["opening_price"]
            high_price = item["high_price"]
            low_price = item["low_price"]
            trade_price = item["trade_price"]
            volumn = item["candle_acc_trade_volume"]

            dto = MonthCandle.create(
                target_date,
                market,
                opening_price,
                high_price,
                low_price,
                trade_price,
                volumn,
            )
            list.append(dto)
    month_repo.insertMonth(list)
    return response


@router.get("/image")
async def get_image():
    # 이미지 파일을 열거나 생성합니다.
    image = Image.new("RGB", (100, 100), color="red")

    # 이미지를 바이트 스트림으로 변환합니다.
    image_stream = io.BytesIO()
    image.save(image_stream, format="PNG")
    image_stream.seek(0)

    # 이미지를 Base64로 인코딩합니다.
    base64_image = base64.b64encode(image_stream.read()).decode("utf-8")

    # JSON 응답을 생성하여 이미지를 포함시킵니다.
    response_data = {"image": base64_image}
    return JSONResponse(content=response_data)


# # 이미지를 생성하는 함수
# def generate_image():
#     # OpenCV를 사용하여 이미지 생성
#     image = cv2.imread("./앞산.jpeg")  # 이미지 파일 경로 지정

#     _, img_encoded = cv2.imencode(".jpg", image)
#     yield (
#         b"--frame\r\n"
#         b"Content-Type: image/jpeg\r\n\r\n" + img_encoded.tobytes() + b"\r\n"
#     )


# # 이미지 응답 라우트
# @router.get("/image")
# def image_route():
#     return StreamingResponse(
#         generate_image(), media_type="multipart/x-mixed-replace; boundary=frame"
#     )
