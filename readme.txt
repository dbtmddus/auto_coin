*구조 설명
- back-end/src : 실제 동작 코드
restAPI.py : 업비트를 통해 data를 주고 받는 기능 구현
stretagy.py : 매수&매도 조건 전략 구현
backtesting.py : 과거 data기반으로 전략 보정
main.py : 실제 실행 모듈

- /etc : 개인용 참고 코드(동작과 무관)


*환경설정

4GB이상 RAM 필요 (AWS t2.medium 이상, prophet 사용에 필요)

sudo apt install docker.io  : docker 설치
sudo snap install docker    : docker종속성 pakage설치
sudo docker run hello-world   : 동작확인용 hello world image 다운&실행

* 업비트 API사용 전에 업비트 my page에서 ip whitelist 설정 필요


*개인 메모

push완료된 git commit수정시
git commit -amend
git push --force https://github.com/dbtmddus/auto_coin master