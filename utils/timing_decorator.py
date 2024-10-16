import time


def timing_decorator(func):
    def wrapped_func(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        print(f"Function {func.__name__!r} executed in {elapsed_time:.4f}s")

        # Return both the result and the elapsed time
        return result, elapsed_time

    return wrapped_func
