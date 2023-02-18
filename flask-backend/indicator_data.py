import yfinance as yf
import talib as tb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys


def get_indicator_data(name, interval, period):
    ticker=yf.Ticker(name)
    data=ticker.history(period=period, interval=interval)
    return data

if __name__ == "__main__":
    print(get_indicator_data(sys.argv[1]))
