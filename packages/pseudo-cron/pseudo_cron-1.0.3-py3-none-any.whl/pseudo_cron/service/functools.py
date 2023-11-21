import signal

from .exceptions import TimeoutException


def exec_safe(func, timeout):

    def signal_handler(signum, frame):
        raise TimeoutException()

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(timeout)
    try:
        func()
    finally:
        signal.alarm(0)
