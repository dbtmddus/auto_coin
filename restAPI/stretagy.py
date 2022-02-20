import time
import pyupbit
import datetime
from restAPI import getBalance,getInfo,getAllInfo,getAllPrice

preDic = {}
dic = {}

def checkBuy():
    print("checkBuy")
    for ticker in dic:
        if ticker in preDic:
            prePrice = preDic[ticker]
            price = dic[ticker]
            change = (price-prePrice)/price 
#            print("check! (ticker:" , ticker ,", " , prePrice , "->" , price , " " , change , ")")
            if ( change > 0.001 ):
                print("buy! (ticker:" , ticker ,", " , prePrice , "->" , price , " " , change , ")")
        else:
            print("new ticker!" , ticker)

def checkSell():
    print("checkSell")
    for ticker in dic:
        if ticker in preDic:
            prePrice = preDic[ticker]
            price = dic[ticker]
            change = (price-prePrice)/price 
            if ( change < -0.001 ):
                print("sell! (ticker:" , ticker ,", " , prePrice , "->" , price , " " , change , ")")
        else:
            print("error : no item!" , ticker)

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