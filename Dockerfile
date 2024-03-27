FROM python:3.8-alpine

RUN pip install pyrogram

COPY . /app

ENTRYPOINT ["python", "app/main.py"]