from fastapi import APIRouter, Depends
from repository.candle_repository import CandleRepository
from models.candle import MonthCandle
import pandas as pd

# import matplotlib.pyplot as plt
import mplfinance as mpf
import base64
import io
import matplotlib.dates as mpdates

router = APIRouter()


@router.get("/graph")
async def show_graph(candle_repo: CandleRepository = Depends()):
    month_list: list[MonthCandle] = candle_repo.select_month()
    trade_list = [o.trade_price for o in month_list]
    target_list = [o.target_date for o in month_list]
    # s = pd.Series(trade_list)
    # s.index = pd.Index(target_list)

    # mpf.title("graph")
    # mpf.plot(s, "--bs")
    # mpf.xticks(s.index, rotation=45)

    # mpf.yticks(s.values)
    # mpf.grid(True)
    # mpf.savefig("save_config.png")
    index = []
    rows = []
    columns = ["Open", "High", "Low", "Close", "Volume"]

    for obj in month_list:
        index.append(obj.target_date)

        rows.append(
            [
                obj.opening_price,
                obj.high_price,
                obj.low_price,
                obj.trade_price,
                obj.volumn,
            ]
        )

    df = pd.DataFrame(rows, columns=columns, index=index)

    print(df)

    kwargs = dict(
        title="chart",
        type="candle",
        volume=True,
        mav=(2, 4, 6),
        ylabel="ohlc candle",
        datetime_format="%Y-%m-%d",
        y_on_right=False,
    )

    mc = mpf.make_marketcolors(up="r", down="b", inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(df, **kwargs, style=s, savefig="testsave.png")
    # mpf.plot(df, savefig="testsave.png")

    print(df)

    return month_list
