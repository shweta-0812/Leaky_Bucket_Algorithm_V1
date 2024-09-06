### Problem Statement:

### Let's break down the implementation into several steps:

#### Components:
- FastAPI Backend: Handles incoming API requests to push messages to the Redis queue.

- Redis Queue: Serves as the message queue with a fixed size (bucket capacity).

- Leaky Bucket Algorithm: Controls the rate at which messages are processed by the consumer.

- Python Consumer: A long-running process that consumes messages from the Redis queue at a constant rate.

- Logging: Logs the processed message responses to a text file.


#### Implementation Steps:

1. Setup Redis Queue:

- Install Redis server locally or use a managed Redis service.
- Set up a Python environment with Redis, FastAPI, and asyncio dependencies.

2. FastAPI Application:

- Create an API endpoint to enqueue messages to the Redis queue.


3. Consumer Process:

- A Python script that will continuously dequeue and process messages from the Redis queue at a constant rate.

- Implement rate-limiting using the Leaky Bucket algorithm.

4. Logging:
- Log processed messages into a text file for auditing and monitoring.

### Required Libraries:

- fastapi: For building the API server.
- redis-py: Redis client for Python for interacting with Redis ( it supports both sync and async connection ).
- uvicorn: ASGI server for running FastAPI.
- asyncio: For asynchronous message processing.
- python-dotenv: For env var management
- pydantic: For type handling in code
- flake8: to ensure code quality
- setuptools: for redis client


#### How to run:
1.Go to the project directory and make sure to run `poetry init` to initialise poetry and setup a python virtual env using `pyenv` module to install `python 3.12.3`.

2. Open 3 terminal windows and go to the project.

3. Run `poetry shell` to activate the virtual env for first and second window.

4. Run `poetry install` in first and second window.

5. In first window, go to `examples/leaky_bucket_algo` and start the FastAPI server by running `uvicorn main:app --reload`.

6. In second window go to `examples/leaky_bucket_algo` and run the consumer by running `python3 consumer.py`.

7. In third window run the redis server by running `redis-server`.

8. Finally, make the curl request and test the flow: 

`curl --location 'http://127.0.0.1:8000/enqueue' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=WKe0Shk1UUGp7JCrW8Cx6twOv84iTYVS' \
--data '{
        "id": 1,
    "job_priority": 1,
    "job_type": 2,
    "job_publisher": "mobile_app",
    "data": "this is my messasge from mobile app"
}'`
