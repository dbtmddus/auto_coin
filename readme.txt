구조 설명
- /src 디렉토리 : 실제 동작 코드
restAPI.py : 업비트를 통해 data를 주고 받는 기능 구현
stretagy.py : 매수&매도 조건 전략 구현
backtesting.py : 과거 data기반으로 전략 보정
main.py : 실제 실행 모듈

- /etc 디렉토리 : 동작과 무관한 개인용 참고 코드


환경설정

4GB이상 RAM 필요 (AWS t2.medium 이상)
sudo apt update
sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime       #time API값을 한국시간으로 설정
sudo apt install python3-pip
pip3 install pyupbit
pip3 install schedule
pip3 install pystan==2.19.1.1
pip3 install convertdate
pip3 install fbprophet


개인 메모

push완료된 git commit수정시
git commit -amend
git push --force https://github.com/dbtmddus/auto_coin master