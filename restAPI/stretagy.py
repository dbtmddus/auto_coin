import time
import pyupbit
import datetime
from restAPI import getBalance,getBalanceKRW,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice

def checkBuyCondition():
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            change = ((price-prePrice)/price)*100 
            if ( change > 7 ):
                ret = buyMarketPrice(market, getBalanceKRW()/2)   #잔액의 일부로 시장가 매수
                print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , change , "%)")
        else:
            print("new market!" , market)

def checkSellCondition():
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            change = ((price-prePrice)/price)*100 
            if ( change < -2 ):
                ret = sellMarketPrice(market, None)   #전량 시장가 매도
                if (ret != None):
                    print("sell! (market:" , market ,", " , prePrice , "->" , price , " " , change , "%)")
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