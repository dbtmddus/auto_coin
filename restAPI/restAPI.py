import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import inspect

access_key = 'kZEmXq2ZhtYtifIxGuJquVxASfvvJv88sJwXQJxD'
secret_key = 'wHumZzesU4S9PU6AhaDdPhZVuNMjmmcQa4bqCTmf'

payload,jwt_token,authorize_token,headers = 0,0,0,0
units = ['BTC', 'KRW', 'USDT']

def getToken():
    global payload,jwt_token,authorize_token,headers
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

def getTokenQuery(query):
    global headers

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

def getBalance():
    getToken()
    res = requests.get('https://api.upbit.com/v1/accounts', headers=headers)
    return res.json()

def getBalance_unit(unit):
    getToken()
    res = requests.get('https://api.upbit.com/v1/accounts', headers=headers)
    balance = res.json()
    ret = -1
    for ticker in balance:
        if (ticker['currency'] == unit):
            ret = ticker['balance']        
    return float(ret)

def getInfo(ticker_list):
    getToken()
    url = "https://api.upbit.com/v1/ticker?markets=" + ticker_list
    res = requests.request("GET", url, headers=headers)
    return res.json()

def getUpbitItem():
    getToken()
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

    getTokenQuery(query)
    res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
    print("매수주문", market, " / 매수금액:", price, " / code", res.status_code)
    if ( res.status_code >= 400 ):
        print (res.json())
    return res

def sellMarketPrice(market, volume):
    print("sellMarketPrice",market,volume)
    #volume == None 일 때 잔고 전체로 설정
    balance_volume = 0
    ticker = market.split('-')[1]
    balance = getBalance()
    for item in balance:
        if( item['currency'] == ticker ):
            balance_volume = float(item['balance'])
    if (volume == None):
        volume = balance_volume

    if (balance_volume > 0):
        query = {
            'market': market,
            'side': 'ask',
            'volume': str(volume),
    #        'price': str(price),
            'ord_type': 'market',
        }
        
        getTokenQuery(query)
        res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
        print("매도주문", market, " / 갯수", volume, " / code", res.status_code)
        if ( res.status_code >= 400 ):
            print (res.json())
        return res
    else:
        return None
        
def sellAll():
    balance_list = getBalance()
    for item in balance_list:
        if (item['currency'] != 'KRW') and (item['currency'] != 'BTC') and (item['currency'] != 'USDT'):
            for unit in units:
                market = unit + '-' + item['currency']
                sellMarketPrice(market,None)

def sellAll_BTC_USDT():
    balance_list = getBalance()
    for item in balance_list:
        if item['currency'] != 'KRW' :
            for unit in units:
                market = unit + '-' + item['currency']
                sellMarketPrice(market,None)

def getAskBidBalance(market): #호가
    url = "https://api.upbit.com/v1/orderbook?markets="+market
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers)
    if ( res.status_code >= 400 ):
        print (inspect.stack()[0][3], 'error', res.status_code)
    return res

def getOneTick(market):
    gap = 9999999999
    orderBook = getAskBidBalance(market)
    try:
        orderList = orderBook.json()[0]['orderbook_units']
        for item in orderList:
            gap = min(gap, item['ask_price'] - item['bid_price'])
    except Exception as e:
        print(inspect.stack()[0][3], "market:", market, 'error msg:', e)
    return float(gap)

def getCandleMin(market, min, count):
    url = "https://api.upbit.com/v1/candles/minutes/"+min+"?market="+market+"&count="+ count
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers)
    return res
    
def getCandleDay(market, count):    
    url = "https://api.upbit.com/v1/candles/days?market="+market+"&count="+ count
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers)
    return res

if __name__ == "__main__":
    #sellAll()
    print(getCandleDay('KRW-BTC', '3').json())
    