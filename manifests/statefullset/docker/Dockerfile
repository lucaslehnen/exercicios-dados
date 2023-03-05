FROM alpine:3.17.0

RUN apk add --no-cache python3 py3-pip

RUN pip3 install --no-cache-dir fastapi==0.87.0 uvicorn==0.20.0 redis-py-cluster==2.1.3

EXPOSE 8000

COPY ./src /app

CMD [ "uvicorn", "app.api:app", "--host", "0.0.0.0" ]