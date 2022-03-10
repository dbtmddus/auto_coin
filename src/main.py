import schedule
import time
import stretagy as st

print("잔고 :", st.getBalance_currency())
st.predict_price("KRW-BTC")
schedule.every(10).minutes.do(lambda: st.predict_price("KRW-BTC"))

while True:
    try:
        #pre work
        st.dic = st.getAllPrice()
        schedule.run_pending()

        #select stretagy
        #st.strategy1_Soaring()
        st.strategy2_VolatilityBreakout()

        #finish work
        st.preDic = st.dic
        time.sleep(0.3)
    except Exception as e:
        print(e)
        time.sleep(1)