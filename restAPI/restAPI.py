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
    
def buyMarketPrice(market, price):    
    query = {
        'market': market,
        'side': 'bid',
#        'volume': null,    시장가 매수는 volume 미사용
        'price': str(price),
        'ord_type': 'price',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
    return res.json()

def sellMarketPrice(market, volume):
    ticker = market.split('-')[1]
    if (volume == None):
        balance = getBalance()
        for item in balance:
            if( item['currency'] == ticker ):
                volume = item['balance']
                print("전량 매도", volume)

    query = {
        'market': market,
        'side': 'ask',
        'volume': str(volume),
#        'price': str(price),
        'ord_type': 'market',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
    return res.json()

if __name__ == "__main__":
#    print(buyMarketPrice('KRW-BTC', 10000))
    print(sellMarketPrice('KRW-BTC', None))
    #print(getBalance())
