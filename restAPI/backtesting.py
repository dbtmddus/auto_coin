import numpy as np
import pandas as pd
from restAPI import getBalance,getBalance_unit,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice,getOneTick,getCandleDay

def get_ror(k=0.5):
    backtestSize = 7
    json = getCandleDay("KRW-BTC", str(backtestSize)).json()
    df = pd.DataFrame(json)

    df['range'] = (df['high_price'] - df['low_price']) * k
    df['target'] = df['opening_price'] + df['range'].shift(1)

    df['ror'] = np.where(df['high_price'] > df['target'],
                         df['trade_price'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[backtestSize-1]
    return ror

for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))