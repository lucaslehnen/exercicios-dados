from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from rediscluster import RedisCluster

import os


db_host = os.getenv("REDIS_HOST", "redis")
db_port = os.getenv("REDIS_PORT", "6379")

app =  FastAPI()

redis = RedisCluster(host=db_host, port=db_port, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
async def root():
  global redis
  redis.incr("count")
  count = redis.get("count")

  return f""""
      <html>
      <title>Teste API</title>
      <body>
        <h1>Count: {count}</h1>
      </body>
      </html>
      """

@app.get("/healthz")
async def health():
  return {
    "message": "ok"
  }