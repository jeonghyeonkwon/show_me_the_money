from fastapi import APIRouter, Depends
import requests
from setting import settings
from html import escape, unescape
from datetime import datetime
from dtos.naver_response import NaverResponse
from slackApi.slack import sendMessage
from db.database import get_db
from sqlalchemy.orm import Session
from models.slack import SlackLog
from repository.slack_repository import SlackRepository
from models.enum import LogType

router = APIRouter()
NAVER_API = "https://openapi.naver.com"
NEWS_REQUEST = f"{NAVER_API}/v1/search/news.json"

header = {
    "X-Naver-Client-Id": settings.naver_client_id,
    "X-Naver-Client-Secret": settings.naver_secret_key,
}


def news_request_url(query, display, start, sort="date"):
    return f"{NEWS_REQUEST}?query={query}&display={display}&start={start}&sort={sort}"


@router.get("/news")
async def news_response(slackRepo: SlackRepository = Depends()):
    keyword = "비트코인"
    print(news_request_url(keyword, 10, 1))

    response = requests.get(news_request_url(keyword, 10, 1), headers=header)

    if response.status_code == 200:
        slackLog: SlackLog = SlackLog.create(LogType.NAVER_SEARCH, keyword)
        slackRepo.insert_log(slackLog)

        item_list = response.json()["items"]
        dtos = []
        for item in item_list:
            title = unescape(item["title"])
            originallink = escape(item["originallink"])
            link = escape(item["link"])
            description = unescape(item["description"])

            us_date = datetime.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")

            # 한국 날짜 형식으로 포맷팅
            kr_date_string = us_date.strftime("%Y-%m-%d %H:%M:%S")

            dto = NaverResponse(title, originallink, link, description, kr_date_string)

            # sendMessage(dto.toTemplate())

            dtos.append(dto)

    return dtos


@router.get("/send")
def news_send():
    return
