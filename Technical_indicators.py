import pandas as pd
import numpy as np
import matplotlib

from app.model import  closed_groups


def rsi(price):
    up_df,down_df=price[['symbol','change_in_price']].copy(),price[['symbol','change_in_price']].copy()
    up_df.loc['change_in_price']=up_df.loc[(up_df['change_in_price'] <0),'change_in_price']=0
    down_df.loc['change_in_price']=down_df.loc[(down_df['change_in_price'] > 0), 'change_in_price'] = 0
    down_df['change_in_price']=down_df['change_in_price'].abs()
    ewma_up=up_df.groupby('symbol')['change_in_price'].transform(lambda x:x.ewm(span=14).mean())
    ewma_down = down_df.groupby('symbol')['change_in_price'].transform(lambda x: x.ewm(span=14).mean())
    relative_strength=ewma_up/ewma_down
    RSI=100-(100/(1+relative_strength))
    price['up_days'] = up_df['change_in_price']
    price['down_days'] = down_df['change_in_price']
    price['RSI']=RSI
    print(price.head())
    stochastic_oscillator(price)

def stochastic_oscillator(price):
    low_14,high_14=price[['symbol','low']].copy(),price[['symbol','high']].copy()
    low_14=low_14.groupby('symbol')['low'].transform(lambda x:x.rolling(window=14).min())
    high_14=high_14.groupby('symbol')['high'].transform(lambda x:x.rolling(window=14).max())
    k_percent=100 * ((price['close'] - low_14) /(high_14-low_14))
    price['k_percent']=k_percent
    print(price.tail())
    price['high_14']=high_14
    price['low_14']=low_14
    william_r(price)

def william_r(price):
    will_r=-100 * (price['high_14']-price['close'])/(price['high_14']-price['low_14'])
    price['will_r']=will_r
    macd(price)

def macd(price):
    ema_26=price.groupby('symbol')['close'].transform(lambda x:x.ewm(span=26).mean())
    ema_12=price.groupby('symbol')['close'].transform(lambda x: x.ewm(span=12).mean())
    macd=ema_26-ema_12
    ema_9=macd.ewm(span=9).mean()
    price['MACD']=macd
    price['MACD_EMA']=ema_9
    price_of_change(price)


def price_of_change(price):
    price['price_rate_of_change']=price.groupby('symbol')['close'].transform(lambda x:x.pct_change(periods=9).mean())
    closed_groups(price)





