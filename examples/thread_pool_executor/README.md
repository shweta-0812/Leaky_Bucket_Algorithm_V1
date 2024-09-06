## Role of ThreadPoolExecutor in Handling CPU-Bound Tasks (our consumer.py of leaky_bucket_algo example)

### Concurrency Model in Python:

Python’s asyncio library is designed for handling I/O-bound tasks efficiently using asynchronous programming. However, it doesn't provide true parallelism for CPU-bound tasks due to the Global Interpreter Lock (GIL) in CPython.

For CPU-bound tasks (e.g., image processing, machine learning computations), if these tasks are run in the same thread as the event loop, they will block the loop and halt the execution of other tasks.

### Using ThreadPoolExecutor:

- The ThreadPoolExecutor allows you to offload CPU-bound tasks to a pool of threads. 
- This enables these tasks to run in parallel threads, bypassing the GIL's constraints to some extent. 
- By using ThreadPoolExecutor, you can keep the event loop running for other tasks, especially I/O-bound ones, while CPU-bound tasks are processed in separate threads.
- In our context, this is crucial because it ensures that the consumer can handle both types of tasks (CPU-bound and I/O-bound) concurrently without one blocking the other.

### If not using ThreadPoolExecutor:
If you don't use ThreadPoolExecutor and run CPU-bound tasks directly in the main thread or event loop, they will block the loop and degrade performance. The application will appear unresponsive during the execution of these tasks.

#### How to run:
1. Go to the project directory and make sure to run `poetry init` to initialise poetry and setup a python virtual env using `pyenv` module to install `python 3.12.3`.

2. Run `poetry shell` to activate the virtual env for first and second window.

3. Run `poetry install` in first and second window.

4. Go to `examples/thread_pool_examples`. 

5. To test running async and sync jobs concurrently: 
   1. In file main.py, uncomment line of code `asyncio.run(concurrent_main())` and comment line of code `asyncio.run(main())` and save file.
   2. Run the file in terminal `python3 main.py`.

6. To test running async and sync jobs concurrently: 
   1. In file main.py, uncomment line of code `asyncio.run(main())` and comment line of code `asyncio.run(concurrent_main())` and save file.
   2. Run the file in terminal `python3 main.py`.
