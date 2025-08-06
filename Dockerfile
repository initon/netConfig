FROM python:3.11-alpine

RUN apk add --no-cache tzdata && \
    rm -rf /var/cache/apk/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ENV TZ="Europe/Moscow"
CMD ["python", "main.py"]