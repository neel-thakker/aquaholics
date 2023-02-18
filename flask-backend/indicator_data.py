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
    EMA = stock['close'].ewm(span = period, adjust = False, min_periods = period).mean()
    return EMA

def get_atr(stock):
    ATR = talib.ATR(stock['high'], stock['low'], stock['close'], timeperiod=14)
    return ATR

def get_adx(stock):
    ADX = talib.ADX(stock['high'], stock['low'], stock['close'], timeperiod=14)
    return ADX

def get_adl(stock):
    AD = talib.AD(stock['high'], stock['low'], stock['close'], stock['Volume'])
    return AD

def get_sma_slope(sma,period):
    slope = (sma.iloc[-1] - sma.iloc[-period]) / period
    return slope

def get_adl_slope(adl,period):
    slope = (adl.iloc[-1] - adl.iloc[-period]) / period
    return slope

def get_indicator_info(name, ticker, interval, period, indicator):
    tk = yf.Ticker(ticker)
    data=tk.history(period=period, interval=interval)
    data.rename(columns = {'Open':'open','Close':'close','High':'high','Low':'low'}, inplace = True)


    if indicator[0:3] == "SMA":
        func = get_sma
        if indicator[3:5] == "20":
            period = 20
        elif indicator[3:5] == "50":
            period = 50
        elif indicator[3:6] == "100":
            period = 100

    elif indicator[0:3] == "EMA":
        func = get_ema
        if indicator[3:5] == "20":
            period = 20
        elif indicator[3:5] == "50":
            period = 50
        elif indicator[3:6] == "100":
            period = 100

    val = func(data, period)
    result = val.to_json(orient="index")
    parsed = json.loads(result)

    df = []
    for items in parsed:
        df.append({ "x" : int(items), "y" : parsed[items]})

    ctx = {
        'name': name,
        'ticker': ticker,
        'data': df
    }
    return ctx

def get_analysis(data):
    #get_macd(data)
    sma20=get_sma(data,20)
    sma100=get_sma(data,100)
    #get_bollinger_bands(data)
    adx=get_adx(data)
    #get_ema(data,20)
    #get_atr(data)
    adl=get_adl(data)
    res = []
    sma20S=get_sma_slope(sma20,5)
    sma100S=get_sma_slope(sma100,10)
    adlS=get_adl_slope(adl,5)
    if(data['rsi'].iloc[-1] > 70):
        res.append("The value of RSI have exeeded 70. This shows that the stock is overbought and its price is expected to drop. This can be considered as a sell signal.")
    elif(data['rsi'].iloc[-1] < 30):
        res.append("The value of RSI have dropped below 30. This shows that the stock is oversold and its price is expected to increase. This can be considered as a buy signal.")
    else:
        res.append("RSI value is oscillating in middle showing no specifi trend. Thus, currently investors should avoid taking any positions.")

    if(adx.iloc[-1]>75):
        res.append("The value of ADX is very high indicating that the current trend is very strong and the price is expected to follow the current trend. Currently investors can take positions with low risk.")
    elif(adx.iloc[-1]>50):
        res.append("The current trend is moderatly strong. The price is expected to follow the current trend but can reverse in near future.")
    else:
        res.append("The value of ADX is very low indicating that the stock price is not following any trend. Investors should avoid taking any positions in current situation.")

    if(sma20S<0):
        res.append("Short term moving averages are indicating a downward trend in the share price.")
    else:
        res.append("Short term moving averages are indicating a upward trend in the share price.")
    if(sma100S>0):
        res.append("Long term moving averages are indicating a upward trend in the share price.")
    else:
        res.append("Long term moving averages are indicating a downward trend in the share price.")

    if(adlS<0 and sma20S<0):
        res.append("The ADL indicator is indicating that the downward trend is expected to continue and the price of share would further decrease. Investors should take a sell position.")
    elif(adlS>0 and sma20S<0):
        res.append("The ADL indicator is indicating that there may be buying pressure and the price trend is expected to reverse. The price of share is expected to rise in near future.")
    elif(adlS<0 and sma20S>0):
        res.append("The ADL indicator is indicating that there may be selling pressure and the price trend is expected to reverse. The price of share is expected to fall in near future.")
    else:
        res.append("The ADL indicator is indicating that the upward trend is expected to continue and the price of share would further increase. Investors should take a buy position.")
    return res


def get_indicator_data(name, ticker, interval, period):
    tk = yf.Ticker(ticker)
    data=tk.history(period=period, interval=interval)
    data.rename(columns = {'Open':'open','Close':'close','High':'high','Low':'low'}, inplace = True)
    rsi_val = get_rsi(data, 14)['rsi']
    data['rsi'] = rsi_val
    result = data.to_json(orient="index")
    parsed = json.loads(result)
    df = []
    for items in parsed:
        val = [parsed[items]['open'], parsed[items]['high'], parsed[items]['low'], parsed[items]['close']]
        df.append({ "x" : int(items), "y" : val, "v" : parsed[items]['Volume'], "r": parsed[items]['rsi']})

    open_val = round(tk.fast_info.open, 2)
    curr_val = round(tk.fast_info.last_price, 2)
    chg_val = round(curr_val - open_val , 2)
    percent_chg = round(((chg_val/open_val) * 100),2)

    anal_data = get_analysis(data)

    ctx = {
        'name': name,
        'ticker': ticker,
        'currVal': curr_val,
        'changeVal': chg_val,
        'percentChange': percent_chg,
        'data': df,
        'analysis': anal_data
    }
    return ctx


if __name__ == "__main__":
    print(get_indicator_info(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
