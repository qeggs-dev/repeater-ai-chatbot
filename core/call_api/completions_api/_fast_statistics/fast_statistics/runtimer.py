import time

class Runtimer:
    def __init__(self):
        self.start_time: int = 0
        self.end_time: int | None = None
    
    def start(self):
        self.start_time = time.perf_counter_ns()

    def end(self):
        self.end_time = time.perf_counter_ns()

    def get_time(self):
        if self.end_time is None:
            end_time = time.perf_counter_ns()
        else:
            end_time = self.end_time
        
        return end_time - self.start_time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()