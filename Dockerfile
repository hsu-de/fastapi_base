FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# 安裝nc用於確認mysql準備完成後再啟動伺服器
RUN apt-get update
RUN apt-get install netcat-traditional

# CMD ["uvicorn", "app.main:app" , "--reload", "--host", "0.0.0.0", "--port", "8000"]