import ta 

def add_indicators(df):

    df["SMA50"] = ta.trend.sma_indicator(
        df["Close"],
        window = 50
    )

    df["SMA200"] = ta.trend.sma_indicator(
        df["Close"],
        window = 200
    )

    df["RSI"] = ta.momentum.rsi(
        df["Close"],
        window = 14
    )


    return df