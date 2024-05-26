FROM python:3.9-slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ARG TELEGRAM_API_KEY=defaultValue
ARG CHAT_ID=defaultValue
ARG SOURCE_CURRENCY=defaultValue
ARG TARGET_CURRENCY=defaultValue

CMD [ "python3" "main.py" ]