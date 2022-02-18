import requests

url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC%2C%20BTC-ETH"
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers)
print(response.text)