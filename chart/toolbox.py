import functools
import timeit

def timer(function):
    """Show runtime after execution"""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        function(*args)
        stop = timeit.default_timer()
        print(f'TIme: {stop - start}')
    return wrapper

