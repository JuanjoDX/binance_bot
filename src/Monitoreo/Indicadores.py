def indicadores(df,t):
    import pandas_ta as ta
    if t == "1m":
        df["HMA10"] = ta.hma(df['Close'], length=10).shift(1)
        df["SMA5"] = df["Close"].rolling(window = 5).mean().shift(1)
        df["SMA10"] = df["Close"].rolling(window = 10).mean().shift(1)
        df["SMA30"] = df["Close"].rolling(window = 30).mean().shift(1)
        df["SMA60"] = df["Close"].rolling(window = 60).mean().shift(1)
        df["SMA120"] = df["Close"].rolling(window = 120).mean().shift(1)
        df["SMA240"] = df["Close"].rolling(window = 240).mean().shift(1)
        df["RSI9"] = ta.rsi(df["Close"], length=9).shift(1)
        df["RSI14"] = ta.rsi(df["Close"], length=14).shift(1)
        df["RSI25"] = ta.rsi(df["Close"], length=25).shift(1)
        return(df)
    elif t == "3m":
        df["HMA5"] = ta.hma(df['Close'], length=5).shift(1)
        df["SMA3"] = df["Close"].rolling(window = 3).mean().shift(1)
        df["SMA5"] = df["Close"].rolling(window = 5).mean().shift(1)
        df["SMA10"] = df["Close"].rolling(window = 10).mean().shift(1)
        df["SMA20"] = df["Close"].rolling(window = 20).mean().shift(1)
        df["SMA50"] = df["Close"].rolling(window = 50).mean().shift(1)
        df["RSI9"] = ta.rsi(df["Close"], length=9).shift(1)
        df["RSI14"] = ta.rsi(df["Close"], length=14).shift(1)
        df["RSI25"] = ta.rsi(df["Close"], length=25).shift(1)
        return(df)
    
    elif t == "5m":
        df["HMA6"] = ta.hma(df['Close'], length=6).shift(1)
        df["SMA2"] = df["Close"].rolling(window = 2).mean().shift(1)
        df["SMA3"] = df["Close"].rolling(window = 3).mean().shift(1)
        df["SMA6"] = df["Close"].rolling(window = 6).mean().shift(1)
        df["SMA12"] = df["Close"].rolling(window = 12).mean().shift(1)
        df["SMA24"] = df["Close"].rolling(window = 24).mean().shift(1)
        df["RSI9"] = ta.rsi(df["Close"], length=9).shift(1)
        df["RSI14"] = ta.rsi(df["Close"], length=14).shift(1)
        df["RSI25"] = ta.rsi(df["Close"], length=25).shift(1)
        return(df)