from indicator_data import *

def get_sma_slope(sma,period):
  slope = (sma.iloc[-1] - sma.iloc[-period]) / period
  return slope
def get_adl_slope(adl,period):
  slope = (adl.iloc[-1] - adl.iloc[-period]) / period
  return slope
def get_analysis(rsi,adx,sma100,sma20,adl):
    res=[]
    sma20S=get_sma_slope(sma20,5)
    sma100S=get_sma_slope(sma100,10)
    adlS=get_adl_slope(adl,5)
    if(rsi['rsi'].iloc[-1] > 70):
        res.append("The value of RSI have exeeded 70. This shows that the stock is overbought and its price is expected to drop. This can be considered as a sell signal.")
    elif(rsi['rsi'].iloc[-1] < 30):
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

def final_analysis(data):
    rsi=get_rsi(data,14)
    #get_macd(data)
    sma20=get_sma(data,20)
    sma100=get_sma(data,100)
    #get_bollinger_bands(data)
    adx=get_adx(data)
    #get_ema(data,20)
    #get_atr(data)
    adl=get_adl(data)
    print(get_analysis(rsi,adx,sma100,sma20,adl))

if __name__ == "__main__":
    df = get_data(sys.argv[1], sys.argv[2], sys.argv[3])
    final_analysis(df)
