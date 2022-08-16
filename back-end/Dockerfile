FROM python:3

RUN apt-get update
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src/ ./

CMD ["python3", "main.py"]