# Relative Strenght Index (RSI)
import pandas as pd
import talib
import numpy as np
import sys


def get_rsi(stock, period):
    rsi_df_lib = pd.DataFrame(talib.RSI(stock['close'],timeperiod=period))
    rsi_df_lib.columns = ['rsi']
    return rsi_df_lib

def get_rsi_trend(rsi_df):
  if(rsi_df['rsi'].iloc[-1] > 70):
    return 0 #sell
  if(rsi_df['rsi'].iloc[-1] < 30):
    return 1 #buy
  else:
    return 2 #hold
# Moving Average Convergence Divergence (MACD)
# SMA = (N - Sum of stock closing values throughout the period) / N
# Weighted multiplier(k) = 2 / (time period + 1)
# EMA = Todays price * k + EMA(yesterday) * (1 - k)
# MACD = EMA(12 days) - EMA(26 days)

def get_macd(stock):
    macd_df_lib = pd.DataFrame(talib.MACD(stock['close'])).transpose()
    macd_df_lib.columns = ['macd', 'signal', 'hist']
    return macd_df_lib

def get_macd_trend(macd_df_lib,idx):
  if(macd_df_lib['macd'].iloc[-idx] > macd_df_lib['signal'].iloc[-idx]):
    return 1 #buy
  elif(macd_df_lib['macd'].iloc[-idx] < macd_df_lib['signal'].iloc[-idx]):
    return 0 #sell
  else:
    return 2 #hold

# Stochastic RSI

def get_stochRSI(stock):
    stochRSI_df_lib = pd.DataFrame(talib.STOCHRSI(stock['close'])).transpose()
    stochRSI_df_lib.columns = ['fast_K', 'fast_D']
    return stochRSI_df_lib

def get_stochRSI_trend(stochRSI_df_lib):
  if(stochRSI_df_lib['fast_K'].iloc[-1] > 80):
    return 0 #sell
  elif(stochRSI_df_lib['fast_K'].iloc[-1] < 20):
    return 1 #buy
  else:
    return 2 #hold

# Exponential Moving Average (EMA)

def get_ema(stock, period):
    exp = stock['close'].ewm(span = period, adjust = False, min_periods = period).mean()

    return exp

def get_ema_trend(ema_50df, ema_200df):
  if(ema_50df['EMA_50'].iloc[-1] > ema_200df['EMA_200'].iloc[-1]):
    return 1 #buy
  elif(ema_50df['EMA_50'].iloc[-1] < ema_200df['EMA_200'].iloc[-1]):
    return 0 #sell
  else:
    return 2 #hold

# Bollinger Bands
def get_bollinger_bands(stock, rate=20):
    boll_band_df_lib = pd.DataFrame(talib.BBANDS(stock['close'], timeperiod=rate)).transpose()
    boll_band_df_lib.columns = ['boll_up', 'boll_middle', 'boll_down']
    return boll_band_df_lib

# Moving Averages
def get_sma(stock,period):
  SMA = talib.SMA(stock['close'],period)
  return SMA

def get_sma_trend(stock,SMA):
  if(stock['close'].iloc[-1]>SMA[-1]):
    return 1
  return 0

def get_sma_slope(sma,period,idx):
  slope = (sma[-idx] - sma[-idx-period]) / period
  return slope

# VWAP Indicator

# Create VWAP function
def get_vwap(stock):
  v = stock['Volume'].values
  tp = (stock['low'] + stock['close'] + stock['high']).div(3).values
  vwap=(tp * v).cumsum() / v.cumsum()
  return vwap

# ATR

def get_atr(stock):
  ATR = talib.ATR(stock['high'], stock['low'], stock['close'], timeperiod=14)
  return ATR

# ADX

def get_adx(stock):
  ADX = talib.ADX(stock['high'], stock['low'], stock['close'], timeperiod=14)
  return ADX


#AD
def get_ad(stock):
  AD = talib.AD(stock['high'], stock['low'], stock['close'], stock['Volume'])
  return AD

# getTrend returns

# 0 for Absent or Weak Trend

# 1 for Strong Trend

# 2 for Very Strong Trend

# 3 for Extremely Strong Trend

def get_adx_trend(ADX):
  ADX=ADX.tolist()
  if(ADX[-1]<25):
    return 0
  elif(ADX[-1]<50):
    return 1
  elif (ADX[-1]<75):
    return 2
  return 3

# OBV

def get_obv(stock):
  OBV = talib.OBV(stock['close'], stock['Volume'])
  return OBV

# Accumulation Distribution Line

def get_ad(stock):
  AD = talib.AD(stock['high'], stock['low'], stock['close'], stock['Volume'])
  return AD

# Combination of Indicators :
# 1: RSI + Bollinger Bands

def rsi_and_bollinger(stock,bollingerBands,rsi_df_lib,sma20,idx):
    '''
    assuming the variables in hand :
    1. current price
    2. bollinger band 2D array consisting of data :
    S.No. | Time/Date | Upper-Bollinger-level | Lower-Bollinger-level | 20-Period-SMA
      1   |   11:00   |     500               |     400               |     450
      2   |   11:05   |     499               |     402               |     449
    3. RSI

    '''
    bollingerSentiment = 0
    bollingerRange = 30

    '''
    sentiment :
    bollingerRange for strong buy
    -bollingerRange for strong sell
    '''

    latest20DaySMA=sma20[-idx]
    latestUpperLevel = bollingerBands['boll_up'].iloc[-idx]
    latestLowerLevel = bollingerBands['boll_down'].iloc[-idx]
    latestUpperLevel = bollingerBands['boll_up'].iloc[-idx]
    latestLowerLevel = bollingerBands['boll_down'].iloc[-idx]
    current_price = stock['close'].iloc[-idx]

    # checking if current price has touched or crossed either bollinger level
    if(current_price <= latestLowerLevel):
        bollingerSentiment = bollingerRange
    elif(current_price >= latestUpperLevel):
        bollingerSentiment = -bollingerRange
    elif(current_price == latest20DaySMA):
        bollingerSentiment = 0
    elif (current_price > latest20DaySMA) and (latestUpperLevel != latest20DaySMA):
        bollingerSentiment = bollingerRange*(float(current_price - latest20DaySMA)/(latestUpperLevel - latest20DaySMA))
    elif (latestLowerLevel != latest20DaySMA):
        bollingerSentiment = -bollingerRange*(float(current_price - latest20DaySMA)/(latestLowerLevel - latest20DaySMA))

    '''
    # checking for convergence or divergence pattern
    for datapoint in bollingerBands:
    upperLevel = datapoint['Upper Bollinger level']
    lowerLevel = datapoint['Lower Bollinger level']
    midLevel = datapoint['20-Period SMA']
    difference_pattern.append(upperLevel - lowerLevel)
    '''

    #RSI

    # rsiRange = 100 - bollingerRange
    rsiSentiment = 0
    rsi = rsi_df_lib['rsi'].iloc[-idx]
    if(rsi <= 30 and rsi >= 25):
        rsiSentiment = 50
    elif(rsi <= 25  and  rsi >= 20):
        rsiSentiment = 55
    elif(rsi <= 20 and rsi >= 15):
        rsiSentiment = 60
    elif(rsi <= 15 and rsi >= 10):
        rsiSentiment = 65
    elif(rsi <= 10):
        rsiSentiment = 70
    elif(rsi <= 75 and rsi >= 70):
        rsiSentiment = -50
    elif(rsi <= 80 and rsi >= 75):
        rsiSentiment = -55
    elif(rsi <= 85 and rsi >= 80):
        rsiSentiment = -60
    elif(rsi <= 90 and rsi >= 85):
        rsiSentiment = -65
    elif(rsi >= 90):
        rsiSentiment = -70
    else:
        rsiSentiment = -1 * (2.5*(rsi-30) - 50)
    '''
    rsi : 30------x------70
    sent: 50------y------(50)

    so

    (x-30)/40 = (y+50)/100

    where answer = -y
    '''
    finalSentiment = bollingerSentiment + rsiSentiment
  # returning value between -100 to 100:  -100 = strong sell, 100 = strong buy
  # ratio of weightage for Bollinger : RSI :: 30 : 70
    return finalSentiment

# 2: RSI + MACD
def rsi_and_macd(stock,rsi_df_lib,macd_df_lib,idx):

    '''
    variables received :
    1. current price
    2. macd line value
    3. signal line value
    4. rsi

    '''
    macdRange = 30
    macdSentiment = 0
    current_price = stock['close'].iloc[-idx]
    macdLineValue = macd_df_lib['macd'].iloc[-idx]
    signalLineValue = macd_df_lib['signal'].iloc[-idx]
    previousMACDLineValue = macd_df_lib['macd'].iloc[-idx]
    previousSignalLineValue = macd_df_lib['signal'].iloc[-idx]
    if macdLineValue > signalLineValue :
        macdSentiment = macdRange
    elif macdLineValue < signalLineValue :
        macdSentiment = -macdRange


    # incase of crossing line, strong trend reversal
    elif macdLineValue == signalLineValue :
        if previousMACDLineValue > previousSignalLineValue:
            macdSentiment = -macdRange
        else:
            macdSentiment = macdRange

    # RSI
    # rsiRange = 70
    rsi = rsi_df_lib['rsi'].iloc[-idx]
    rsiSentiment = 0

    if(rsi <= 30 and rsi >= 25):
        rsiSentiment = 45
    elif(rsi <= 25 and rsi >= 20):
        rsiSentiment = 50
    elif(rsi <= 20 and rsi >= 15):
        rsiSentiment = 60
    elif(rsi <= 15 and rsi >= 10):
        rsiSentiment = 65
    elif(rsi <= 10):
        rsiSentiment = 70
    elif(rsi <= 75 and rsi >= 70):
        rsiSentiment = -45
    elif(rsi <= 80 and rsi >= 75):
        rsiSentiment = -50
    elif(rsi <= 85 and rsi >= 80):
        rsiSentiment = -60
    elif(rsi <= 90 and rsi >= 85):
        rsiSentiment = -65
    elif(rsi >= 90):
        rsiSentiment = -70
    else:
      rsiSentiment = -1 * (2.25*(rsi-30) - 45)

    '''
    rsi : 30------x------70
    sent: 45------y------(-45)

    so

    (x-30)/40 = (y+45)/90

    where answer = -y
    '''
    finalSentiment = macdSentiment + rsiSentiment
    # returning value between -100 to 100:  -100 = strong sell, 100 = strong buy
    # ratio of weightage for MACD : RSI :: 30 : 70

    return finalSentiment

# 3: RSI + ADX
def adx_and_rsi(adx_df,rsi_df_lib,idx):
  rsi=rsi_df_lib['rsi'].iloc[-idx]
  adx=adx_df.iloc[-idx]
  if(rsi<20):
    result=10
  elif(rsi>80):
    result=-10
  else:
    result=10-1/3*(rsi-20)
  result=result*10
  scale=adx/75
  if scale>1:
    scale=1
  result=result*scale
  return result

# 4: MACD + ADX
def adx_and_macd(adx_df,macd_df_lib,idx):
  if(macd_df_lib['macd'].iloc[-1] > macd_df_lib['signal'].iloc[-idx]):
    result=1
  elif(macd_df_lib['macd'].iloc[-1] < macd_df_lib['signal'].iloc[-idx]):
    result=-1
  else:
    result=0
  adx=adx_df.iloc[-idx]
  scale=adx/0.75
  if scale>100:
    scale=100
  result=result*scale
  return result

# 5: MACD + BOLLINGER
def macd_and_bollinger(stock, MACD, bollingerBands,sma20,idx):

  '''
    stock dataframe
    MACD : Dataframe consisting of columns macd, signal and hist=macd-signal
    bollingerBands
  '''
  bollingerRange = 30
  bollingerSentiment = 0
  latest20DaySMA = sma20[-idx]
  latestUpperLevel = bollingerBands['boll_up'].iloc[-idx]
  latestLowerLevel = bollingerBands['boll_down'].iloc[-idx]
  current_price = stock['close'].iloc[-idx]

  if(current_price <= latestLowerLevel):
    bollingerSentiment = bollingerRange
  elif(current_price >= latestUpperLevel):
    bollingerSentiment = -bollingerRange
  elif(current_price == latest20DaySMA):
    bollingerSentiment = 0
  elif (current_price > latest20DaySMA) and (latestUpperLevel != latest20DaySMA):
      bollingerSentiment = bollingerRange*(float(current_price - latest20DaySMA)/(latestUpperLevel - latest20DaySMA))
  elif (latestLowerLevel != latest20DaySMA):
      bollingerSentiment = -bollingerRange*(float(current_price - latest20DaySMA)/(latestLowerLevel - latest20DaySMA))

  macd_trend = get_macd_trend(MACD,idx)
  '''
    BollingerSentiment : -30----x----30
    Macd_trend : {-1,1}
  '''
  weight = 0.4
  res = weight*macd_trend*100 + (1-weight)*bollingerSentiment*(10/3)
  return res

# 6: SMA200 + RSI
def sma200_and_rsi(stock,rsi_df_lib,sma200,idx):
  sma_slope = get_sma_slope(sma200, 50,idx)
  sma_range = 20
  smaSentiment = 0
  if(sma_slope>5):
    smaSentiment = 20
  if(sma_slope<-5):
    smaSentiment = -20
  else:
    smaSentiment = 4*sma_slope
  rsiSentiment = 0
  rsiRange = 20
  rsi=rsi_df_lib['rsi'].iloc[-idx]
  if(rsi<20):
    rsiSentiment = rsiRange
  if(rsi>80):
    rsiSentiment = -rsiRange
  else:
    rsiSentiment = rsiRange - (2*rsiRange)*(rsi-20)/(60)
  weight = 0.3
  res = weight*smaSentiment*5 + (1-weight)*rsiSentiment*5
  return res;



# ATR values teklls the volatility in market. If current ATR value is towards the lowest of its tiome period then it shows that a breakout may occur.
# Remember that ATR value does not tell the direction of trend. Hence, we need to use it carefully.
# in str_analysis(), we find the ratio of current value of atr to the range in time period. This gives us the value of volatility.
# lesser the atr_sentiment, higher are the chances of breakout.
# in the next function, we check for the trend for last 20 days.

#   ATR_RESULT     |    SMA trend   |  final return value
#     100          |      down(-1)  |     -100 => value going downward but breakout expected => buy
#     100          |      up(1)     |      100 => value going   upward but breakout expected => sell
#     80           |      down(-1)  |     -80  => value going downward but less chances of breakout expected => somewhat buy
#     80           |      up(1)     |      80  => value going   upward but less chances of breakout expected => somewhat sell

# else no inference



def atr_analysis(stock,atr,idx):
  min_atr = 1000
  max_atr = -1000
  for i in range(14):
    min_atr = min(min_atr,atr.iloc[-i-idx])
    max_atr = max(max_atr,atr.iloc[-i-idx])

  current_atr = atr.iloc[-idx]
  current_difference_from_lowest = current_atr - min_atr
  max_difference = max_atr - min_atr

  atr_sentiment = (current_difference_from_lowest/max_difference) * 5
  atr_result = 5
  if atr_sentiment <= 1:
    atr_result = 100
  elif atr_sentiment <= 1:
    atr_result = 80
  else:
    atr_result = 0
  return atr_result

#7:
def stoc_rsi_and_bollinger(stock,sma20,bollingerBands,stochRSI_df_lib,idx):
  rsi = stochRSI_df_lib['fast_K'].iloc[-idx]
  rsiSentiment = 0

  if(rsi <= 30 and rsi >= 25):
      rsiSentiment = 45
  elif(rsi <= 25 and rsi >= 20):
      rsiSentiment = 50
  elif(rsi <= 20 and rsi >= 15):
      rsiSentiment = 60
  elif(rsi <= 15 and rsi >= 10):
      rsiSentiment = 65
  elif(rsi <= 10):
      rsiSentiment = 70
  elif(rsi <= 75 and rsi >= 70):
      rsiSentiment = -45
  elif(rsi <= 80 and rsi >= 75):
      rsiSentiment = -50
  elif(rsi <= 85 and rsi >= 80):
      rsiSentiment = -60
  elif(rsi <= 90 and rsi >= 85):
      rsiSentiment = -65
  elif(rsi >= 90):
      rsiSentiment = -70
  else:
    rsiSentiment = -1 * (2.25*(rsi-30) - 45)

  bollingerRange = 30
  bollingerSentiment = 0
  latest20DaySMA = sma20[-idx]
  latestUpperLevel = bollingerBands['boll_up'].iloc[-idx]
  latestLowerLevel = bollingerBands['boll_down'].iloc[-idx]
  current_price = stock['close'].iloc[-idx]

  if(current_price <= latestLowerLevel):
    bollingerSentiment = bollingerRange
  elif(current_price >= latestUpperLevel):
    bollingerSentiment = -bollingerRange
  elif(current_price == latest20DaySMA):
    bollingerSentiment = 0
  elif (current_price > latest20DaySMA) and (latestUpperLevel != latest20DaySMA):
    bollingerSentiment = bollingerRange*(float(current_price - latest20DaySMA)/(latestUpperLevel - latest20DaySMA))
  elif (latestLowerLevel != latest20DaySMA):
    bollingerSentiment = -bollingerRange*(float(current_price - latest20DaySMA)/(latestLowerLevel - latest20DaySMA))
  weight = 0.7
  final_sentiment = float(weight*rsiSentiment*(10/7)) +  float((1-weight)*bollingerSentiment*(10/3))
  return final_sentiment

#8:
def stoc_rsi_and_macd(stock,macd,stochRSI_df_lib,idx):
    macd_trend = get_macd_trend(macd,idx)
    rsi = stochRSI_df_lib['fast_K'].iloc[-idx]
    rsiSentiment = 0

    if(rsi <= 30 and rsi >= 25):
      rsiSentiment = 45
    elif(rsi <= 25 and rsi >= 20):
      rsiSentiment = 50
    elif(rsi <= 20 and rsi >= 15):
      rsiSentiment = 60
    elif(rsi <= 15 and rsi >= 10):
      rsiSentiment = 65
    elif(rsi <= 10):
      rsiSentiment = 70
    elif(rsi <= 75 and rsi >= 70):
      rsiSentiment = -45
    elif(rsi <= 80 and rsi >= 75):
      rsiSentiment = -50
    elif(rsi <= 85 and rsi >= 80):
      rsiSentiment = -60
    elif(rsi <= 90 and rsi >= 85):
      rsiSentiment = -65
    elif(rsi >= 90):
      rsiSentiment = -70
    else:
      rsiSentiment = -1 * (2.25*(rsi-30) - 45)

    weight = 0.75
    final_sentiment = int(rsiSentiment*10/7*weight)+ int(macd_trend*100*(1-weight))
    return final_sentiment


# we are calculating stoic_rsi + 200 EMA here
# we already calculated rsi + 200 SMA

def get_ema_slope(ema,period,idx):
  slope = (ema.iloc[-idx] - ema.iloc[-idx-period]) / period
  return slope

#9:
def stoc_rsi_200ema(stock,stochRSI_df_lib,ema200,idx):

    rsi = stochRSI_df_lib['fast_K'].iloc[-idx]
    rsiSentiment = 0
    if(rsi <= 30 and rsi >= 25):
      rsiSentiment = 45
    elif(rsi <= 25 and rsi >= 20):
      rsiSentiment = 50
    elif(rsi <= 20 and rsi >= 15):
      rsiSentiment = 60
    elif(rsi <= 15 and rsi >= 10):
      rsiSentiment = 65
    elif(rsi <= 10):
      rsiSentiment = 70
    elif(rsi <= 75 and rsi >= 70):
      rsiSentiment = -45
    elif(rsi <= 80 and rsi >= 75):
      rsiSentiment = -50
    elif(rsi <= 85 and rsi >= 80):
      rsiSentiment = -60
    elif(rsi <= 90 and rsi >= 85):
      rsiSentiment = -65
    elif(rsi >= 90):
      rsiSentiment = -70
    else:
      rsiSentiment = -1 * (2.25*(rsi-30) - 45)

    ema_slope = get_ema_slope(ema200, 50,idx)
    ema_range = 30
    emaSentiment = 0
    if(ema_slope>5):
      emaSentiment = 30
    elif(ema_slope<5):
      emaSentiment = -30
    else:
      emaSentiment = 6*ema_slope

    final_sentiment = rsiSentiment + emaSentiment
    # ratio :              70      +      30

    return final_sentiment


# 10:
def adx_and_stoc_rsi(adx_df,stoc_rsi_df_lib,idx):
  rsi=stoc_rsi_df_lib['fast_K'].iloc[-idx]
  adx=adx_df.iloc[-idx]
  if(rsi<20):
    result=10
  elif(rsi>80):
    result=-10
  else:
    result=10-1/3*(rsi-20)
  result=result*10
  scale=adx/75
  if scale>1:
    scale=1
  result=result*scale
  return result


# 11:

def atr_and_50SMA(stock,atr,sma20,idx):
  atr_result = atr_analysis(stock,atr,idx)
  if sma20[-idx] > sma20[-idx-1]:
    atr_result = atr_result * -1
  else:
    atr_result = atr_result* 1
  return atr_result


# 12:

def sma200_and_sma50(stock,sma50,sma200,idx):
  slope50=get_sma_slope(sma50,5,idx)
  slope200=get_sma_slope(sma200,5,idx)
  res=0
  if(sma200[-1-idx]>sma50[-1-idx] and sma200[-2-idx]<sma50[-2-idx]):
    res=-1
  elif(sma200[-1-idx]<sma50[-1-idx] and sma200[-2-idx]>sma50[-2-idx]):
    res=1
  if(slope50>1):
    slope50=1
  if(slope50<-1):
    slope50=-1
  if(slope200>1):
    slope200=1
  if(slope50<-1):
    slope50=-1
  if(res==-1):
    res=res*(slope200-slope50)
  else:
    res=res*(slope50-slope200)
  res=res*50
  return res

#13:

  # The A/D line is used to help assess price trends and potentially spot forthcoming reversals.
  # If a security’s price is in a downtrend while the A/D line is in an uptrend, then the
  # indicator shows there may be buying pressure and the security’s price may reverse to the upside.
  # Conversely, if a security’s price is in an uptrend while the A/D line is in a downtrend, then
  # the indicator shows there may be selling pressure, or higher distribution.
  # This warns that the price may be due for a decline.


  # find slope => steeper the slope, A strongly rising A/D line confirms a strongly rising price.
  # Similarly, if the price is falling and the A/D is also falling, then there is still plenty of
  # distribution and prices are likely to continue to decline.

def get_adl_slope(adl,period, start):
  slope = (adl.iloc[-start] - adl.iloc[-start-period]) / period
  return slope


def adl_rsi(stock,adl_data,stochRSI_df_lib,idx):
  period=5
  adl_sentiment = 0
  sma_data = get_sma(stock,period)
  adl_slope = get_adl_slope(adl_data, period,idx)
  past_adl_slope = get_adl_slope(adl_data, period, idx+period)
  sma_slope = get_sma_slope(sma_data,period,idx)

  if adl_data.iloc[-idx] == 0:
    adl_sentiment = 0

  elif adl_slope > 0 and sma_slope < 0 :
    if adl_slope > past_adl_slope:
      adl_sentiment = 40
    else:
      adl_sentiment = 20

  elif adl_slope < 0 and sma_slope > 0 :
    if adl_slope > past_adl_slope:
      adl_sentiment = -40
    else:
      adl_sentiment = -20


  elif adl_slope > past_adl_slope:
    if adl_slope < 0:
      adl_sentiment = -30
    elif adl_slope > 0:
      adl_sentiment = 30


  rsi = stochRSI_df_lib['fast_K'].iloc[-idx]
  rsiSentiment = 0
  if(rsi <= 30 and rsi >= 25):
      rsiSentiment = 40
  elif(rsi <= 25 and rsi >= 20):
      rsiSentiment = 45
  elif(rsi <= 20 and rsi >= 15):
      rsiSentiment = 50
  elif(rsi <= 15 and rsi >= 10):
      rsiSentiment = 55
  elif(rsi <= 10):
      rsiSentiment = 60
  elif(rsi <= 75 and rsi >= 70):
      rsiSentiment = -40
  elif(rsi <= 80 and rsi >= 75):
      rsiSentiment = -45
  elif(rsi <= 85 and rsi >= 80):
      rsiSentiment = -50
  elif(rsi <= 90 and rsi >= 85):
      rsiSentiment = -55
  elif(rsi >= 90):
      rsiSentiment = -60
  else:
    rsiSentiment = -1 * (2*(rsi-30) - 40)

  final_sentiment = rsiSentiment + adl_sentiment
    # ratio :              60      +      40
  return final_sentiment

#14:
def get_obv_slope(obv,period, start):
  slope = (obv.iloc[-start] - obv.iloc[-start-period]) / period
  return slope

def obv_ema(stock,idx):
  ema20=get_ema(stock,20)
  obv=get_obv(stock)
  ema_slope = get_ema_slope(ema20, 14,idx)
  obv_slope = get_obv_slope(obv, 14, idx)
  sentiment = 0
  if ema_slope > 0.5 and obv_slope > 0.5:
    sentiment = 100
  elif ema_slope > 0 and obv_slope > 0:
    sentiment = 50
  elif ema_slope < -0.5 and obv_slope < -0.5:
    sentiment = -100
  elif ema_slope < 0 and obv_slope < 0:
    sentiment = -50
  return sentiment

def obv_ema_rsi(stock,rsi,idx):
  obv_ema_sentiment = obv_ema(stock,idx)
  rsi=rsi['rsi'].iloc[-idx]
  rsiSentiment = 0
  if(rsi <= 30 and rsi >= 25):
      rsiSentiment = 10
  elif(rsi <= 25 and rsi >= 20):
      rsiSentiment = 20
  elif(rsi <= 20 and rsi >= 15):
      rsiSentiment = 30
  elif(rsi <= 15 and rsi >= 10):
      rsiSentiment = 40
  elif(rsi <= 10):
      rsiSentiment = 50
  elif(rsi <= 75 and rsi >= 70):
      rsiSentiment = -10
  elif(rsi <= 80 and rsi >= 75):
      rsiSentiment = -20
  elif(rsi <= 85 and rsi >= 80):
      rsiSentiment = -30
  elif(rsi <= 90 and rsi >= 85):
      rsiSentiment = -40
  elif(rsi >= 90):
      rsiSentiment = -50
  else:
    rsiSentiment = -1 * ((rsi-30)/2 - 10)


  '''
    rsi : 30------x------70
    sent: 10------y------(-10)

    so

    (x-30)/40 = (y+10)/20

    where answer = -y
    '''

  return ((obv_ema_sentiment + rsiSentiment)*2)/3

#15:
def vwap_sentiment(stock,idx):
  '''
    price      : dataframe of stock prices at 5 minute intervals throught the day
    vwap       : dataframe of vwap values at 5 minute intervals for the current day
  '''
  vwap = get_vwap(stock)
  vwap_sentiment = 0
  price = stock['close'].iloc[-idx]
  if vwap[-idx] > price:
    if vwap[-idx] > 1.2*price:
      vwap_sentiment = -100
    else:
      vwap_sentiment = -(vwap[-idx] - price)/((1.2 - 1)*price)*100
  elif vwap[-idx] < price :
    if vwap[-idx] < 0.8*price :
      vwap_sentiment = 100
    else:
      vwap_sentiment = (vwap[-idx] - price)/((0.8 - 1)*price)*100
  return vwap_sentiment

def finalPred(data,bollinger,rsi,macd,adx,atr,adl,sma200,sma50,sma20,stoc_rsi,ema200,idx):
  r1=rsi_and_bollinger(data,bollinger,rsi,sma20,idx)
  r2=rsi_and_macd(data,rsi,macd,idx)
  r3=adx_and_rsi(adx,rsi,idx)
  r4=adx_and_macd(adx,macd,idx)
  r5=macd_and_bollinger(data,macd,bollinger,sma20,idx)
  r6=sma200_and_rsi(data,rsi,sma200,idx)
  r7=atr_and_50SMA(data,atr,sma20,idx)
  r8=sma200_and_sma50(data,sma50,sma200,idx)
  r9=adx_and_stoc_rsi(adx,stoc_rsi,idx)
  r10=stoc_rsi_and_bollinger(data,sma20,bollinger,stoc_rsi,idx)
  r11=stoc_rsi_and_macd(data,macd,stoc_rsi,idx)
  r12=stoc_rsi_200ema(data,stoc_rsi,ema200,idx)
  r13=adl_rsi(data,adl,stoc_rsi,idx)
  r14=obv_ema_rsi(data,rsi,idx)
  r15=vwap_sentiment(data,idx)
  result=(r1+r2+r3+r4+r5+r6+r7+r8+r9+r10+r11+r12+r13+r14+r15)/15
  return result

def get_pred(data):
    rsi = get_rsi(data,14)
    macd = get_macd(data)
    sma200=get_sma(data,200)
    sma20=get_sma(data,20)
    sma50=get_sma(data,50)
    adx=get_adx(data)
    bollinger=get_bollinger_bands(data)
    atr=get_atr(data)
    stoc_rsi=get_stochRSI(data)
    ema200=get_ema(data,200)
    adl=get_ad(data)
    signal=finalPred(data,bollinger,rsi,macd,adx,atr,adl,sma200,sma50,sma20,stoc_rsi,ema200,1)
    return signal

if __name__ == '__main__':
    get_pred(sys.argv[1])