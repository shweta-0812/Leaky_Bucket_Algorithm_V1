import os
import redis.asyncio as aioredis

from typing import Dict
from object_schema import JobSchema
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# initialise FASTAPI app instance
app = FastAPI()

# take environment variables from .env. for fastapi app
load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
QUEUE_NAME = os.getenv("QUEUE_NAME")
BUCKET_CAPACITY = int(os.getenv("BUCKET_CAPACITY"))
LEAK_RATE = int(os.getenv("LEAK_RATE"))

# Connect to Async Redis
redis_client = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")


@app.get("/")
def read_root():
    return {"status": "ok"}


# API to push jobs to Redis queue
@app.post("/enqueue")
async def enqueue_job(job: JobSchema) -> Dict:
    queue_length = await redis_client.llen(QUEUE_NAME)

    # Check if bucket (queue) is full
    if queue_length >= BUCKET_CAPACITY:
        raise HTTPException(status_code=429, detail="Queue is full. Please try again later.")

    # Convert to JSON string for redis client
    job_json_str = job.json()
    await redis_client.rpush(QUEUE_NAME, job_json_str)

    return {"status": "success", "job": "Message enqueued successfully"}
