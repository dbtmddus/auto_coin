import time
import pyupbit
import datetime
from restAPI import getBalance,getBalanceKRW,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice

def checkBuy():
    print("checkBuy")
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            change = ((price-prePrice)/price)*100 
            if ( change > 0.5 ):
                ret = buyMarketPrice(market, getBalanceKRW()/10)   #잔액의 일부로 시장가 매수
                print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , change , "%)")
        else:
            print("new market!" , market)

def checkSell():
    print("checkSell")
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            change = ((price-prePrice)/price)*100 
            if ( change < -0.2 ):
                ret = sellMarketPrice(market, None)   #전량 시장가 매도
                if (ret != None):
                    print("sell! (market:" , market ,", " , prePrice , "->" , price , " " , change , "%)")
        else:
            print("error : no item!" , market)

# 자동매매 시작
print(getBalance())
dic = getAllPrice()
preDic = dic

while True:
    try:
        #pre work
        dic = getAllPrice()

        #check buy&sell
        checkBuy()
        checkSell()

        #finish work
        preDic = dic
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)