import time
import pyupbit
import datetime
from restAPI import getBalance,getInfo

def checkBuy():
    print("checkBuy")

def checkSell():
    print("checkSell")

# 자동매매 시작
getBalance()
while True:
    try:
        checkBuy()
        checkSell()
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)