"""
- time_ns for Python before 3.7
- Elapsed context manager
- pretty_ns to represent time elapsed in human lovable form

Usage:
>>> start = time_ns()
>>> import time
>>> time.sleep(0.0000001)
>>> pretty_ns((start + 100) - start)
'0.1 mks'

>>> with Timer() as timer:
...     import time
...     time.sleep(0.0000001)
...     timer.pretty.endswith('s')
...     timer.ns > 0
True
True

"""
from typing import Any, Optional

time_ns = None  # for Python3.7+ this is function from system library time


# for earlier Python versions this is emulation of the Python3.7 time_ns


def pretty_ns(elapsed_ns: int, fixed_units: Optional[str] = None) -> str:
    dividers = {
        "us": 1,
        "mks": 1000,
        "ms": 1000,
        "sec": 1000,
        "minutes": 60,
        "hours": 60,
        "days": 24,
    }
    result: float = elapsed_ns
    for unit, divider in dividers.items():
        result /= divider
        if result < 100 or unit.lower() == fixed_units:
            return f"{result:.1f} {unit}"
        result = round(result)
    return f"{result:.1f} {dividers['days']}"


def emul_time_ns() -> int:
    return int(perf_counter() * 10 ** 9)


class Timer:
    def __init__(self) -> None:
        pass

    def __enter__(self) -> "Timer":
        self.start = time_ns()  # type: ignore
        return self

    def __exit__(self, *args: Any) -> None:
        pass

    @property
    def ns(self) -> int:
        return time_ns() - self.start  # type: ignore

    @property
    def pretty(self) -> str:
        return pretty_ns(self.ns)


import time

try:
    time_ns = time.time_ns
except AttributeError:
    from time import perf_counter

    time_ns = emul_time_ns

if __name__ == "__main__":
    import doctest

    doctest.testmod()
