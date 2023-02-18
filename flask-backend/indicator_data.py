import yfinance as yf
import talib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import json


def get_data(stock, interval, period):
    ticker=yf.Ticker(stock)
    data=ticker.history(period=period, interval=interval)
    data.rename(columns = {'Close':'close','High':'high','Low':'low'}, inplace = True)
    return data

def get_rsi(stock, period):
    rsi_df_lib = pd.DataFrame(talib.RSI(stock['close'],timeperiod=period))
    rsi_df_lib.columns = ['rsi']
    return rsi_df_lib

def get_macd(stock):
    macd_df_lib = pd.DataFrame(talib.MACD(stock['close'])).transpose()
    macd_df_lib.columns = ['macd', 'signal', 'hist']
    return macd_df_lib

def get_bollinger_bands(stock, rate=20):
    boll_band_df_lib = pd.DataFrame(talib.BBANDS(stock['close'], timeperiod=rate)).transpose()
    boll_band_df_lib.columns = ['boll_up', 'boll_middle', 'boll_down']
    return boll_band_df_lib

def get_sma(stock,period):
    SMA = talib.SMA(stock['close'],period)
    return SMA

def get_ema(stock, period):
    exp = stock['close'].ewm(span = period, adjust = False, min_periods = period).mean()
    ema_df = pd.DataFrame(exp)
    col_name = 'EMA_' + str(period)
    ema_df.columns = [col_name]
    return ema_df

def get_atr(stock):
    ATR = talib.ATR(stock['high'], stock['low'], stock['close'], timeperiod=14)
    return ATR

def get_adx(stock):
    ADX = talib.ADX(stock['high'], stock['low'], stock['close'], timeperiod=14)
    return ADX

def get_adl(stock):
    AD = talib.AD(stock['high'], stock['low'], stock['close'], stock['Volume'])
    return AD

def get_all_data(name, interval, period):
    stock = get_indicator_data(name, interval, period)
    print(stock)
    print(get_adl(stock))
    print(get_adx(stock))
    print(get_atr(stock))
    print(get_bollinger_bands(stock, rate=20))
    print(get_ema(stock, 20))
    print(get_macd(stock))
    print(get_rsi(stock, 14))
    print(get_sma(stock, 20))

def get_indicator_data(name, ticker, interval, period):
    tk = yf.Ticker(ticker)
    data=tk.history(period=period, interval=interval)
    data.rename(columns = {'Open':'open','Close':'close','High':'high','Low':'low'}, inplace = True)
    result = data.to_json(orient="index")
    parsed = json.loads(result)
    # return parsed
    # print(type(parsed))
    data = []
    for items in parsed:
        ohlc = [parsed[items]['open'], parsed[items]['high'], parsed[items]['low'], parsed[items]['close']]
        data.append({ "x" : int(items), "y" : ohlc})

    open_val = round(tk.fast_info.open, 2)
    curr_val = round(tk.fast_info.last_price, 2)
    chg_val = round(curr_val - open_val , 2)
    percent_chg = round(((chg_val/open_val) * 100),2)

    ctx = {
        'name': name,
        'ticker': ticker,
        'currVal': curr_val,
        'changeVal': chg_val,
        'percentChange': percent_chg,
        'data': data
    }
    return ctx


if __name__ == "__main__":
    print(get_indicator_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
