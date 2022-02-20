import pyupbit

access = "kZEmXq2ZhtYtifIxGuJquVxASfvvJv88sJwXQJxD"
secret  = "wHumZzesU4S9PU6AhaDdPhZVuNMjmmcQa4bqCTmf"
upbit = pyupbit.Upbit(access, secret)

print (upbit.get_balance("KRW-BTC"))
print (upbit.get_balance("KRW"))