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
    print(res.json())

def getInfo(ticker):
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC%2C%20" + ticker
    res = requests.request("GET", url, headers=headers)
    print(res.text)

getBalance()
getInfo("BTC-ETH")