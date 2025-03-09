from typing import Union


def pretty_sz(size: Union[int, float]) -> str:
    unit_threshold = 100  # Threshold to switch to next unit
    dividers = {
        "bytes": 1,
        "kb": 1024,
        "mb": 1024,
        "gb": 1024,
        "pb": 1024,
    }
    result = size
    for unit, divider in dividers.items():
        result /= divider
        if result < unit_threshold:
            return f"{result:.1f} {unit}"
        result = round(result)
    return f"{result:.1f} {dividers['pb']}"
