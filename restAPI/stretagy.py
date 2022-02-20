import time
import pyupbit
import datetime
from restAPI import getBalance,getBalanceKRW,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice

preDic = {}
dic = {}

def checkBuy():
    print("checkBuy")
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            change = ((price-prePrice)/price)*100 
#            print("check! (market:" , market ,", " , prePrice , "->" , price , " " , change , ")")
            if ( change > 0.5 ):
                print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , change , "%)")
                buyMarketPrice(market, getBalanceKRW()/2)   #잔액의 절반액수로 시장가 매수
        else:
            print("new market!" , market)

def checkSell():
    print("checkSell")
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            change = ((price-prePrice)/price)*100 
            if ( change < -0.5 ):
                print("sell! (market:" , market ,", " , prePrice , "->" , price , " " , change , "%)")
                sellMarketPrice(market, None)   #전량 시장가 매도
        else:
            print("error : no item!" , market)

# 자동매매 시작
getBalance()
dic = getAllPrice()
preDic = dic
while True:
    try:
        #pre work
        dic = getAllPrice()
        #print(dic)

        #check buy&sell
        checkBuy()
        checkSell()

        #finish work
        preDic = dic
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)