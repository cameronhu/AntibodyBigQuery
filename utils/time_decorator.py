import time


def timing_decorator(func):

    def wrapped_func(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, *kwargs)
        end_time = time.perf_counter()

        print(f"Function {func.__name__!r} executed in {(end_time-start_time):.4f}s")

        return result

    return wrapped_func
