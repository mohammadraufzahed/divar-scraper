FROM python:3.9-alpine
RUN apk update && \
    apk upgrade && \
    apk add alpine-sdk bash firefox libpq-dev

WORKDIR /usr/src/app
VOLUME [ "/output" ]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV DATABASE_HOST=127.0.0.1
ENV DATABASE_PORT=8080
ENV DATABASE_USER=divar_scraper
ENV DATABASE_PASSWORD=divar_scraper
ENV DATABASE_NAME=divar_scraper
COPY . .
COPY binary/ ./binary/
CMD [ "bash" ]