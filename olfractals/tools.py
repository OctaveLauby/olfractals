""""Convenient tools for python object handling"""
from time import sleep, time


def wait_until(predicate, freq=0.1, timeout=5, raise_err=True):
    """Wait until predicate return True"""
    start = time()
    while not predicate():
        if time() - start > timeout:
            if raise_err:
                raise TimeoutError(
                    "Predicate did not come True before timeout"
                )
            return False
        sleep(freq)
    return True
