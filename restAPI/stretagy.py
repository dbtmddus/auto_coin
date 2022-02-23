import time
import pyupbit
import datetime
from restAPI import getBalance,getBalance_unit,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice,getOneTick

# 자동매매 시작
print("잔고 :", getBalance())
dic = getAllPrice()
preDic = dic

def checkBuyCondition():
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            diff = ((price-prePrice)/price)*100
            unit = market.split('-')[0] 
            if diff > 4:
                amount  = getBalance_unit(unit)/3 #매수금액
                oneTick = getOneTick(market)
                if (price-prePrice) > oneTick:
                    ret = buyMarketPrice(market, amount)   #시장가 매수
                    print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%", "oneTick:", "%.20f" %oneTick, unit, "amount:", amount, ")" )
        else:
            print("new market!" , market)

units = ['BTC', 'KRW', 'USDT']

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

def checkSellCondition():
    market_list = getBalance_market()

    for market in market_list:
        unit = market.split('-')[0]
        currency = market.split('-')[1]
        if (currency != 'BTC') and (currency != 'KRW') and (currency != 'USDT'):
            prePrice = preDic[market]
            price = dic[market]
            diff = ((price-prePrice)/price)*100 
            if ( diff < -0.01 ):
                ret = sellMarketPrice(market, None)   #전량 시장가 매도
                if (ret != None):
                    print("sell! (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%)")
while True:
    try:
        #pre work
        dic = getAllPrice()

        #check buy&sell
#        checkBuyCondition()
        checkSellCondition()

        #finish work
        preDic = dic
        time.sleep(0.5)
    except Exception as e:
        print(e)
        time.sleep(1)