import requests
from datetime import datetime
import pandas as pd


def spring_candle_dataframe(url, headers):
    response = requests.get(url, headers=headers).json()

    index = []

    rows = []

    columns = ["Open", "High", "Low", "Close", "Volume"]

    format_string = "%Y-%m-%d %H:%M:%S"  # 입력된 날짜 및 시간 형식

    for obj in response:
        index.append(datetime.strptime(obj["targetDate"], format_string))

        rows.append(
            [
                obj["openingPrice"],
                obj["highPrice"],
                obj["lowPrice"],
                obj["tradePrice"],
                obj["volume"],
            ]
        )

    df = pd.DataFrame(rows, columns=columns, index=index)
    sorted_df = df.sort_index()
    return sorted_df
