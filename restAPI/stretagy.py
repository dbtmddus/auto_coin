import time
import pyupbit
import datetime
from restAPI import getBalance,getBalance_unit,getInfo,getAllInfo,getAllPrice,buyMarketPrice,sellMarketPrice,getOneTick

def getAmount(market): # 매수 1회 금액
    unit = market.split('-')[0]
    return getBalance_unit('KRW')/3

def checkBuyCondition():
    for market in dic:
        if market in preDic:
            prePrice = preDic[market]
            price = dic[market]
            change = ((price-prePrice)/price)*100 
            if ( change > 4 ) and ( (price-prePrice) > getOneTick(market) ):
                ret = buyMarketPrice(market, getAmount())   #잔액의 일부로 시장가 매수
                print("buy! (market:" , market ,", " , prePrice , "->" , price , " " , change , "%)")
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
                prePrice = preDic[market]
                price = dic[market]
                change = ((price-prePrice)/price)*100 
                if ( change < -1 ):
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