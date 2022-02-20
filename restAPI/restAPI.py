import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests

access_key = 'kZEmXq2ZhtYtifIxGuJquVxASfvvJv88sJwXQJxD'
secret_key = 'wHumZzesU4S9PU6AhaDdPhZVuNMjmmcQa4bqCTmf'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

def getBalance():
    res = requests.get('https://api.upbit.com/v1/accounts', headers=headers)
    return res.json()

def getInfo(ticker_list):
    url = "https://api.upbit.com/v1/ticker?markets=" + ticker_list
    res = requests.request("GET", url, headers=headers)
    return res.json()

def getUpbitItem():
    url = "https://api.upbit.com/v1/market/all"
    res = requests.request("GET", url, headers=headers)
    return res.json()

def getTicker():
    ret = getUpbitItem()
    tickerList = []
    for item in ret:
        tickerList.append(item["market"])
    return tickerList

def getAllInfo():
    tickerList = getTicker()
    str_ticker = ','.join(tickerList)
    ret = getInfo(str_ticker)
    return ret

def getAllPrice():
    infoList = getAllInfo()
    ret = {}
    for item in infoList:
        ret[item["market"]] = item["trade_price"]
    return ret
    
if __name__ == "__main__":
#    print(getAllInfo())
    print(getAllPrice()) 
