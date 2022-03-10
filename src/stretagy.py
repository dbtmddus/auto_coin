import time
import pyupbit
import datetime
import pandas as pd
from fbprophet import Prophet
from restAPI import *
from backtesting import *

dic = getAllPrice()
preDic = dic
predicted_close_price = 0

def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    learningSize = '200'
    json = getCandleMin("KRW-BTC", '60', learningSize).json()
    json.reverse()
    for item in json:
        item['candle_date_time_kst'] = pd.Timestamp(item['candle_date_time_kst'])

    temp_df = pd.DataFrame(json)
    df = pd.DataFrame()
    df['index'] = temp_df['candle_date_time_kst']
    df['trade_price'] = temp_df['trade_price']
    df['ds'] = df['index']
    df['y'] = df['trade_price']
    data = df[['ds','y']]

#    print ('data:', data)
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue
    print ('predict : ', predicted_close_price)

def checkSoaringBuy( threshold ):
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            diff = ((price-prePrice)/price)*100
            unit = market.split('-')[0] 
            #print("buy check.. (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%")
            if diff > threshold:
                amount  = getBalance_unit(unit)/3 #매수금액
                oneTick = getOneTick(market)
                if ((price-prePrice) > oneTick*2.1):
                    ret = buyMarketPrice(market, amount)   #시장가 매수
                    print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%", "oneTick:", "%.20f" %oneTick, unit, "amount:", amount, ")" )
        else:
            print("new market!" , market)

def checkSoaringSell():
    market_list = getBalance_market()

    for market in market_list:
        unit = market.split('-')[0]
        currency = market.split('-')[1]
        if (currency != 'BTC') and (currency != 'KRW') and (currency != 'USDT'):
            prePrice = preDic[market]
            price = dic[market]
            diff = ((price-prePrice)/price)*100 
            if ( diff < -0.5 ):
                ret = sellMarketPrice(market, None)   #전량 시장가 매도
                if (ret != None):
                    print("sell! (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%)")

def strategy1_Soaring():
    checkSoaringBuy(8)
    checkSoaringSell()

def strategy2_VolatilityBreakout():
    t = datetime.datetime.now()
    if (t.hour == 9) and (t.minute == 00):   # Sell
        print ('Sell all.  time:', t.hour, "/", t.minute)
        sellAll_BTC_USDT()
        time.sleep(60)
        strategy2_VolatilityBreakout.k = getBestK()
    else :                                  #Buy
        market = 'KRW-BTC'
        
        candleInfo = getCandleDay(market, '2').json()
        today = candleInfo[0]
        yesterday = candleInfo[-1]

        range = (float(yesterday['high_price']) - float(yesterday['low_price'])) * strategy2_VolatilityBreakout.k
        targetPrice = today['opening_price'] + range
        price = dic[market]

        #print("buy check.. (market:" , market ,", current price:" , price , ", k:" , strategy2_VolatilityBreakout.k, "target price:", targetPrice)
        if (price >= targetPrice):
            if (predicted_close_price > price):
                amount  = getBalance_unit('KRW') #매수금액
                if (amount > 10000):
                    ret = buyMarketPrice(market, amount)   #시장가 매수
                    print("buy! (market:" , market ,", current price:" , price 
                        , ", k:" , strategy2_VolatilityBreakout.k, "target price:", targetPrice
                        , ", predicted:", predicted_close_price, ", amount", amount)
strategy2_VolatilityBreakout.k  = getBestK()

