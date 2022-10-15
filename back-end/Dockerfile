FROM python:3

WORKDIR /app
COPY requirements.txt ./
COPY ./src/ ./

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

CMD ["python3", "-u", "main.py"]