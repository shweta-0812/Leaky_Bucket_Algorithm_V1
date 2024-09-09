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

# Queue names
queue_names = [
    "P1_primary", "P1_secondary", "P1_tertiary",
    "P2_primary", "P2_secondary", "P2_tertiary",
    "P3_primary", "P3_secondary", "P3_tertiary"
]


# Initialize all queues with empty lists (optional, for clarity)
async def initialize_queues():
    for queue in queue_names:
        await redis_client.delete(queue)  # Clear existing data for fresh start


@app.on_event("startup")
async def startup_event():
    await initialize_queues()


@app.get("/")
def read_root():
    return {"status": "ok"}


# API to push jobs to Redis queue
@app.post("/enqueue")
async def enqueue_job(job: JobSchema) -> Dict:
    queue_name = f"{job.job_priority}_primary"
    queue_length = await redis_client.llen(queue_name)

    # Check if bucket (queue) is full
    if queue_length >= BUCKET_CAPACITY:
        raise HTTPException(status_code=429, detail="Queue is full. Please try again later.")

    # Convert to JSON string for redis client
    job_json_str = job.json()
    await redis_client.rpush(queue_name, job_json_str)

    return {"status": "success", "job": "Message enqueued successfully"}
