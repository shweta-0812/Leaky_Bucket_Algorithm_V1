TIME_QUANTUM = 2  # ms
SCHEDULER_CAPACITY = 4


class RoundRobinScheduler:
    def __init__(self, processes, time_quantum):
        self.execution_time = 0
        self.time_quantum = time_quantum
        self.processes = processes
        self.scheduling_queue = list(processes)

    def execute(self):
        while len(self.scheduling_queue):
            process_id, burst_time = self.scheduling_queue.pop(0)
            if burst_time > self.time_quantum:
                self.execution_time += self.time_quantum
                remaining_exec_time = burst_time - self.time_quantum
                if remaining_exec_time > 0:
                    self.scheduling_queue.append((process_id, remaining_exec_time))
            else:
                self.execution_time += burst_time

        print(f"Total time taken for all processes: {self.execution_time} units.")


def main():
    processes = [(1, 5), (2, 8), (3, 3)]  # (process_id, burst_time in ms)

    rr_scheduler = RoundRobinScheduler(processes, TIME_QUANTUM)

    rr_scheduler.execute()


if __name__ == "__main__":
    main()
