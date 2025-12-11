"""
Decorators for other modules.

Functions
---------
timer
    Measure the elapsed time of the decorated function.
"""

import functools
import time


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(
            f"\n=======================================\n"
            f"Finished {func.__name__}() in {run_time:.4f} secs\n"
            f"=======================================\n"
        )
        return value
    return wrapper
