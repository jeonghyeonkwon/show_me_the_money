from fastapi import APIRouter, Depends
import requests
import pandas as pd
from datetime import datetime
import mplfinance as mpf
import matplotlib as mpdatas
from util.spring_test import spring_candle_dataframe
from util.graph import draw_hist, draw_acc, draw_mdd, draw_bollinger_band, spear1
from repository.graph_repository import GraphRepository

router = APIRouter()

SPRING_API = "http://localhost:8088"
SPRING_API_TEST_WEEK = SPRING_API + "/v1/candle/week"
SPRING_API_TEST_DAY = SPRING_API + "/v1/candle/day"

headers = {"accept": "application/json"}


@router.get("/graph")
async def show_graph_test():
    sorted_df = spring_candle_dataframe(SPRING_API_TEST_WEEK, headers)

    # print(sorted_df)

    # print(sorted_df["Close"])

    # print(sorted_df["Close"].shift(1))

    sec_dpc = (sorted_df["Close"] / sorted_df["Close"].shift(1) - 1) * 100
    sec_dpc.iloc[0] = 0

    # print(sec_dpc)
    # draw_hist(sec_dpc, 30)
    # print(sec_dpc.cumsum().index)
    # print(sec_dpc)

    # draw_acc(sec_dpc)

    # draw_mdd(sorted_df)

    draw_bollinger_band(sorted_df)

    print("*******&")
    # kwargs = dict(
    #     title="chart",
    #     type="candle",
    #     volume=True,
    #     mav=(2, 4, 6),
    #     ylabel="ohlc candle",
    #     datetime_format="%Y-%m-%d",
    #     yscale="linear",
    # )

    # 2020-09-07 09:00:00  12353000.0  12571000.0  11860000.0  12377000.0  20616.03
    # 2020-11-01 09:00:00  15606000.0  21459000.0  15011000.0  21315000.0  183580.50

    # 주석

    # mc = mpf.make_marketcolors(
    #     up="r",
    #     down="b",
    #     inherit=True,
    # )
    # s = mpf.make_mpf_style(
    #     marketcolors=mc,
    # )
    # now = datetime.now()

    # # 원하는 형식의 문자열로 변환
    # date_string = now.strftime("%Y년%m월%d일%H시%M분%S초")
    # print(date_string)
    # mpf.plot(
    #     sorted_df,
    #     **kwargs,
    #     style=s,
    #     savefig=f"./graph/candle/testsave_{date_string}.png",
    # )

    return "response"


@router.get("/graph-day")
async def show_graph_test(graphRepo: GraphRepository = Depends()):
    sorted_df = spring_candle_dataframe(SPRING_API_TEST_DAY, headers)
    print(sorted_df)
    sec_dpc = (sorted_df["Close"] / sorted_df["Close"].shift(1) - 1) * 100
    sec_dpc.iloc[0] = 0
    # print(sec_dpc)
    spear1(sorted_df, graphRepo)
    return "response"
