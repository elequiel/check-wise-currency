FROM --platform=$BUILDPLATFORM python:alpine3.19
RUN apk update && apk upgrade

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ARG TELEGRAM_API_KEY=defaultValue
ARG CHAT_ID=defaultValue
ARG SOURCE_CURRENCY=defaultValue
ARG TARGET_CURRENCY=defaultValue

ENTRYPOINT [ "python3", "main.py" ]