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