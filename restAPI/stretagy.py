import time
import pyupbit
import datetime
from restAPI import getBalance,getBalance_unit,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice,getOneTick

def checkBuyCondition():
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            diff = ((price-prePrice)/price)*100
            unit = market.split('-')[0] 
            if diff > 4:
                amount  = getBalance_unit(unit) #매수금액
                oneTick = getOneTick(market)
                if (price-prePrice) > oneTick:
                    ret = buyMarketPrice(market, amount)   #잔액의 일부로 시장가 매수
                    print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%", "oneTick:", "%.20f" %oneTick, "amount:", amount, ")" )
        else:
            print("new market!" , market)

def checkSellCondition():
    #잔고 list
    balance_list = getBalance()
    balance_market_list = []
    for item in balance_list:
        market = item['unit_currency'] + '-' + item['currency']
        balance_market_list.append(market)

    for market in dic:
        if market in preDic:
            if market in balance_market_list:
                if (market != 'KRW-BTC') and (market != 'BTC-USDT'):
                    prePrice = preDic[market]
                    price = dic[market]
                    diff = ((price-prePrice)/price)*100 
                    if ( diff < -0.01 ):
                        ret = sellMarketPrice(market, None)   #전량 시장가 매도
                        if (ret != None):
                            print("sell! (market:" , market ,", " , prePrice , "->" , price , " " , diff , "%)")
        else:
            print("error : no item!" , market)
        
# 자동매매 시작
print("잔고 :", getBalance())
dic = getAllPrice()
preDic = dic

while True:
    try:
        #pre work
        dic = getAllPrice()

        #check buy&sell
        checkBuyCondition()
        checkSellCondition()

        #finish work
        preDic = dic
        time.sleep(0.5)
    except Exception as e:
        print(e)
        time.sleep(1)