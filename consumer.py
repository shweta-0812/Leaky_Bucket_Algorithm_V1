import redis
import asyncio
import time
import json
from concurrent.futures import ThreadPoolExecutor
from object_schema import JobSchema, JobType

REDIS_HOST = "localhost"
REDIS_PORT = 6379
QUEUE_NAME = "message_queue"
BUCKET_CAPACITY = 10
LEAK_RATE = 2

PROCESSED_JOB_LOG_FILE = "processed_job.log"

# Sync Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Create a ThreadPoolExecutor for handling CPU-bound tasks in sync workers
executor = ThreadPoolExecutor(max_workers=5)


async def async_worker(data):
    """
    Process an I/O-bound task asynchronously.
    """
    # Simulate I/O operation
    with open(PROCESSED_JOB_LOG_FILE, "a") as log_file:
        await asyncio.sleep(2)  # Simulating an I/O operation
        log_file.write(f"{data}\n")

    log_message(f"Async worker processed I/O-bound job with data: {data}")


def sync_worker(data):
    """
    Process a CPU-bound task synchronously.
    """
    # Simulate a CPU-bound task
    time.sleep(2)
    result = []
    for x in range(1, 100):
        compute = (x ** 1) + (x ** 2) + (x ** 3) + (x ** 4) + (x ** 5) + (x ** 6) + (x ** 7) + (x ** 8) + (x ** 9) + \
                  (x ** 10) + (x ** 11) + (x ** 12) + (x ** 13) + (x ** 14) + (x ** 15) + (x ** 16) + (x ** 17) + \
                  (x ** 18) + (x ** 19) + (x ** 20) + (x ** 21) + (x ** 22) + (x ** 23) + (x ** 24) + (x ** 25) + \
                  (x ** 26) + (x ** 27) + (x ** 28) + (x ** 29) + (x ** 30) + (x ** 31) + (x ** 32) + (x ** 33) + \
                  (x ** 34) + (x ** 35) + (x ** 36) + (x ** 37) + (x ** 38) + (x ** 39) + (x ** 40) + (x ** 41) + \
                  (x ** 42) + (x ** 43) + (x ** 44) + (x ** 45) + (x ** 46) + (x ** 47) + (x ** 48) + (x ** 49) + \
                  (x ** 50) + (x ** 51) + (x ** 52) + (x ** 53) + (x ** 54) + (x ** 55) + (x ** 56) + (x ** 57) + \
                  (x ** 58) + (x ** 59) + (x ** 60) + (x ** 61) + (x ** 62) + (x ** 63) + (x ** 64) + (x ** 65) + \
                  (x ** 66) + (x ** 67) + (x ** 68) + (x ** 69) + (x ** 70) + (x ** 71) + (x ** 72) + (x ** 73) + \
                  (x ** 74) + (x ** 75) + (x ** 76) + (x ** 77) + (x ** 78) + (x ** 79) + (x ** 80) + (x ** 81) + \
                  (x ** 82) + (x ** 83) + (x ** 84) + (x ** 85) + (x ** 86) + (x ** 87) + (x ** 88) + (x ** 89) + \
                  (x ** 90) + (x ** 91) + (x ** 92) + (x ** 93) + (x ** 94) + (x ** 95) + (x ** 96) + (x ** 97) + \
                  (x ** 98) + (x ** 99)
        result.append(compute)
    answer = 0
    for r in result:
        answer += r

    log_message(f"Sync worker processed CPU-bound job with data: {data} and answer: {answer}")


async def dispatch_job(job: JobSchema):
    """
    Dispatch job to the appropriate worker based on its type.
    """
    job_type = job["job_type"]
    data = job["data"]

    if job_type == JobType.IO_BASED.value:
        await async_worker(data)
    elif job_type == JobType.CPU_BASED.value:
        # Submit the sync task to the ThreadPoolExecutor
        await asyncio.get_event_loop().run_in_executor(executor, sync_worker, data)
    else:
        log_message(f"Unknown job type: {job_type}")


def log_message(message):
    """
    Log the processed message to a file.
    """
    with open(PROCESSED_JOB_LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")
    print(message)


async def consumer():
    """
    Long-running consumer process to consume messages from the Redis queue.
    """
    while True:
        # Check if there are messages in the queue
        message = redis_client.lpop(QUEUE_NAME)
        if message:
            job = json.loads(message)  # Decode the JSON message
            await dispatch_job(job)
        else:
            print("No messages to process. Waiting...")

        # Control the leak rate
        await asyncio.sleep(1 / LEAK_RATE)


if __name__ == "__main__":
    # Start the consumer loop in it's dedicated event loop
    asyncio.run(consumer())
