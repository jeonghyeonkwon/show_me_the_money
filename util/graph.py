import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates


# 히스토그램 그래프 그리기
def draw_hist(dt, bins):
    plt.hist(dt, bins=bins)

    plt.grid(True)

    plt.savefig("./graph/hist.png")


# 히스토그램 그래프 그리기
def draw_acc(df):
    # print(df.index)
    new_index = []
    for i in df.index:
        new_index.append(i.date())

    print(new_index)

    copy_series = pd.Series(df.values, index=new_index)
    # print(copy_series)

    plt.plot(copy_series.index, copy_series.cumsum(), "b", label="BTC")

    plt.ylabel("Change %")
    start_date = copy_series.head(1).index[0] - timedelta(days=100)
    end_date = copy_series.tail(1).index[0] + timedelta(days=100)

    # print(start_date)
    # print(end_date)

    plt.xlim(start_date, end_date)

    plt.xticks(rotation=30)

    plt.grid(True)

    plt.legend(loc="best")
    # plt.figure(figsize=(50, 50))
    # print(plt.gcf())

    plt.savefig("./graph/acc.png")


# MDD 그리기
def draw_mdd(df):
    print("mdd")
    window = 7

    # print(df)
    peak = df["Close"].rolling(window, min_periods=1).max()
    # print(peak)

    drawdown = df["Close"] / peak - 1.0

    max_dd = drawdown.rolling(window, min_periods=1).min()

    plt.figure(figsize=(9, 7))

    plt.subplot(211)
    df["Close"].plot(label="BTC", title="BTC MDD", grid=True, legend=True)

    plt.subplot(212)
    drawdown.plot(c="blue", label="BTC DD", grid=True, legend=True)
    max_dd.plot(c="red", label="BTC MDD", grid=True, legend=True)
    plt.savefig("./graph/mdd.png")


# 볼린저 밴드
def draw_bollinger_band(df):
    print(df)

    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["stddev"] = df["Close"].rolling(window=20).std()
    df["upper"] = df["MA20"] + (df["stddev"] * 2)
    df["lower"] = df["MA20"] - (df["stddev"] * 2)
    df["PB"] = (df["Close"] - df["lower"]) / (df["upper"] - df["lower"])
    df["bandwidth"] = (df["upper"] - df["lower"]) / df["MA20"] * 100
    df["TP"] = (df["High"] + df["Low"] + df["Close"]) / 3
    df["PMF"] = 0
    df["NMF"] = 0

    for i in range(len(df.Close) - 1):
        if df.TP.values[i] < df.TP.values[i + 1]:
            df.PMF.values[i + 1] = df.TP.values[i + 1] * df.Volume.values[i + 1]
            df.NMF.values[i + 1] = 0
        else:
            df.NMF.values[i + 1] = df.TP.values[i + 1] * df.Volume.values[i + 1]

            df.PMF.values[i + 1] = 0

    df["MFR"] = df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum()

    df["MFI10"] = 100 - 100 / (1 + df["MFR"])

    # 반전 매매 기법
    df["II"] = (
        (2 * df["Close"] - df["High"] - df["Low"])
        / (df["High"] - df["Low"])
        * df["Volume"]
    )
    df["IIP21"] = (
        df["II"].rolling(window=21).sum() / df["Volume"].rolling(window=21).sum() * 100
    )

    df = df.dropna()

    df = df[19:]

    plt.figure(figsize=(9, 15))

    plt.subplot(4, 1, 1)
    plt.plot(df.index, df["Close"], color="#0000ff", label="CLose")
    plt.plot(df.index, df["upper"], "r--", label="Upper band")
    plt.plot(df.index, df["MA20"], "k--", label="Moving average 20")
    plt.plot(df.index, df["lower"], "c--", label="Lower band")

    plt.fill_between(df.index, df["upper"], df["lower"], color="0.9")

    for i in range(len(df.Close)):
        # 추종 주세 매매
        # if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        #     plt.plot(df.index.values[i], df.Close.values[i], "r^")
        # elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        #     plt.plot(df.index.values[i], df.Close.values[i], "bv")

        # 반전 매매 기법
        if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
            plt.plot(df.index.values[i], df.Close.values[i], "r^")
        elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
            plt.plot(df.index.values[i], df.Close.values[i], "bv")

    plt.legend(loc="best")
    plt.title("BTC Bollinger Band (20 day, 2std)")

    plt.subplot(4, 1, 2)
    plt.plot(df.index, df["PB"] * 100, color="b", label="%B x 100")

    plt.plot(df.index, df["MFI10"], "g--", label="MFI(10 day)")

    plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])
    for i in range(len(df.Close)):
        if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
            plt.plot(df.index.values[i], 0, "r^")
        elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
            plt.plot(df.index.values[i], 0, "bv")

    plt.legend(loc="best")

    plt.grid(True)

    plt.subplot(4, 1, 3)
    plt.plot(df.index, df["bandwidth"], color="m", label="Band Width")

    plt.grid(True)
    plt.legend(loc="best")

    plt.subplot(4, 1, 4)
    plt.bar(df.index, df["IIP21"], color="g", label="II% 21day")
    for i in range(0, len(df.Close)):
        if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
            plt.plot(df.index.values[i], 0, "r^")
        elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
            plt.plot(df.index.values[i], 0, "bv")

    plt.grid(True)

    plt.legend(loc="best")

    plt.savefig("./graph/bollinger.png")


# 삼중창 1
def spear1(df):
    print(df)
    ema60 = df.Close.ewm(span=60).mean()  # 주식의 12주 치수 이동평균
    ema130 = df.Close.ewm(span=130).mean()  # 주식의 26주 치수 이동평균
    macd = ema60 - ema130  # MACD선
    signal = macd.ewm(span=45).mean()  # 신호선 (MACD의 9주 지수 이동평균)
    macdhist = macd - signal

    df = df.assign(
        ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist
    ).dropna()
    df["number"] = df.index.map(mdates.date2num)

    ohlc = df[["number", "Open", "High", "Low", "Close"]]

    plt.figure(figsize=(9, 7))

    p1 = plt.subplot(2, 1, 1)
    plt.title("BTC")

    plt.grid(True)

    candlestick_ohlc(p1, ohlc.values, width=0.6, colorup="red", colordown="blue")
    p1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    plt.plot(df.number, df["ema130"], color="c", label="EMA130")

    plt.legend(loc="best")

    p2 = plt.subplot(2, 1, 2)
    plt.grid(True)
    p2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.bar(df.number, df["macdhist"], color="m", label="MACD-Hist")
    plt.plot(df.number, df["macd"], color="b", label="MACD")
    plt.plot(df.number, df["signal"], "g--", label="MACD-Signal")
    plt.legend(loc="best")
    plt.savefig("./graph/spear.png")
    print(ohlc)
