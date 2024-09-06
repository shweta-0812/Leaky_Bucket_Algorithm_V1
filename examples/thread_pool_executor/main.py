import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


def cpu_bound_task(n):
    # Simulate a CPU-bound task
    print(f"Starting CPU-bound task {n}")
    time.sleep(2)  # Simulate computation time

    print(f"Completed CPU-bound task {n}")


async def io_bound_task(n):
    # Simulate an I/O-bound task
    print(f"Starting I/O-bound task {n}")
    await asyncio.sleep(1)  # Simulate I/O delay

    print(f"Completed I/O-bound task {n}")


async def concurrent_main():
    start_time = time.time()

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Schedule CPU-bound tasks in the ThreadPoolExecutor
        loop = asyncio.get_running_loop()
        for i in range(3):
            loop.run_in_executor(executor, cpu_bound_task, i)

        # Run I/O-bound tasks concurrently
        io_tasks = [io_bound_task(i) for i in range(3)]
        await asyncio.gather(*io_tasks)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


async def main():
    start_time = time.time()
    # Run CPU-bound tasks synchronously
    for i in range(3):
        cpu_bound_task(i)

    # Run I/O-bound tasks concurrently
    io_tasks = [io_bound_task(i) for i in range(3)]
    await asyncio.gather(*io_tasks)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


asyncio.run(concurrent_main())
# asyncio.run(main())
