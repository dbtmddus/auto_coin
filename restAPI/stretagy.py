import time
import pyupbit
import datetime
from restAPI import getBalance,getBalance_unit,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice,getOneTick,getCandleDay

units = ['BTC', 'KRW', 'USDT']

# 자동매매 시작
print("잔고 :", getBalance())
dic = getAllPrice()
preDic = dic

def strategy1_soaringBuy():
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            diff = ((price-prePrice)/price)*100
            unit = market.split('-')[0] 
            if diff > 8:
                amount  = getBalance_unit(unit)/3 #매수금액
                oneTick = getOneTick(market)
                if ((price-prePrice) > oneTick*2.1):
                    ret = buyMarketPrice(market, amount)   #시장가 매수
                    print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%", "oneTick:", "%.20f" %oneTick, unit, "amount:", amount, ")" )
        else:
            print("new market!" , market)

def getBalance_market():
    balance_list = getBalance()
    market_list = []
    for item in balance_list:
        currency = item['currency']
        market = ""
        unit = ""
        if (currency != 'BTC') and (currency != 'KRW') and (currency != 'USDT'):
            for unit_candi in units:
                market_candi = unit_candi + '-' + currency
                if market_candi in dic:
                    market = market_candi
                    unit = unit_candi
                    market_list.append(market)
                    break
    return market_list

def strategy1_soaringSell():
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
                    
def strategy2_VolatilityBreakout():
    t = datetime.datetime.now()
    if (t.hour == 0) and (t.minute == 0):   # Sell
        sellAll_BTC_USDT()

    else :  #Buy
        market = 'KRW-BTC'
        k = 0.2

        candleInfo = getCandleDay(market, '2').json()
        today = candleInfo[0]
        yesterday = candleInfo[-1]

        range = (float(yesterday['high_price']) - float(yesterday['low_price'])) * k
        targetPrice = today['opening_price'] + range
        price = dic[market]

        print("buy check.. (market:" , market ,", current price:" , price , ", k:" , k, "target price:", targetPrice)
        if (price >= targetPrice):
            amount  = getBalance_unit('KRW')/3 #매수금액
            ret = buyMarketPrice(market, amount)   #시장가 매수
            print("buy! (market:" , market ,", current price:" , price , ", k:" , k, "target price:", targetPrice)

while True:
    try:
        #pre work
        dic = getAllPrice()

        strategy2_VolatilityBreakout()

        #finish work
        preDic = dic
        time.sleep(0.3)
    except Exception as e:
        print(e)
        time.sleep(1)