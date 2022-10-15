*환경설정
-4GB이상 RAM 필요 (AWS 기준 t2.medium 이상, prophet lib 최소 요구사항)
-업비트 API사용을 위해, server의 ip를 업비트 my page의 ip whitelist 추가
-docker 설치 (아래 command 실행)
sudo apt install docker.io  : docker 설치
sudo snap install docker    : docker종속성 pakage설치
sudo docker run hello-world   : 동작확인용 hello world image 다운&실행


*실행방법 (위 환경설정 완료 후)
sudo docker-compose up : 실행


*구조 설명
- ./back-end : 자동매매 back-end
restAPI.py : 업비트를 통해 data를 주고 받는 기능 구현
stretagy.py : 매수&매도 조건 전략 구현
backtesting.py : 과거 data기반으로 전략 보정
main.py : 실제 실행 모듈

- ./front-end : 현재 미개발 (향후 거래 기록 등 db 확인할 수 있도록 추가 예정)
- ./etc : 개인용 참고 코드(동작과 무관)