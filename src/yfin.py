import yfinance as yf
import pandas as pd
import os

cwd = os.getcwd()
directory = os.path.dirname(cwd)

tickers = ["^GSPC", "^DJI", "^IXIC", "^NYA", "^XAX", "^BUK100P", "^RUT", "^VIX", "^FTSE", "^GDAXI", "^FCHI", "^STOXX50E", "^N100", "^BFX", "IMOEX.ME",
           "^N225", "HSI", "000001.SS", "399001.SZ", "^STI", "^AXJO", "^AORD", "^BSESN", "^JKSE", "^KLSE", "^NZ50", "^KS11", "^TWII", "^GSPTSE", "^BVSP",
           "^MXX", "^IPSA", "^MERV", "^TA125.TA", "^JN0U.JO"]

def query_yahoo():
  for ticker in tickers:
      index = yf.Ticker(ticker) # getting ticker object
      df = index.history(period="max") # accessing historical data for given ticker
      if df.empty: # no data for this ticker
          continue
      else: # save historical data to .csv
          ticker = ticker.replace("^", "")
          df.to_csv(os.path.join(directory, 'data', f'ticker_{ticker}.csv'))
