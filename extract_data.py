import pandas as pd
import numpy as np
import matplotlib

from app.Technical_indicators import  rsi
from app.config import FILE_LOCATION


def data_preprocess(FILE_LOCATION):
    price=pd.read_csv(FILE_LOCATION,index_col=False)
    price.sort_values(by=['symbol','datetime'],inplace=True)
    price['change_in_price']=price['close'].diff()
    mask=price['symbol'] !=price['symbol'].shift(1)
    price['change_in_price']=np.where(mask==True,np.nan,price['change_in_price'])
    rsi(price)



