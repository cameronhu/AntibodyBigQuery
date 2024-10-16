import time

def time(func):

    def wrapped_func(*args, *kwargs):
        start_time = time.time()
        result = func(*args, *kwargs)
        end_time = time.time()

        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')

        return result
    return wrapped_func