from typing import Any

__all__ = [
    "readBI",
    "writeBI",
    "overrideBI"
]

__BI = __builtins__


def readBI(name: str) -> Any:
    global __BI
    if isinstance(__BI, dict):
        return __BI[name]
    else:
        return getattr(__BI, name)


def writeBI(name: str, value: Any) -> None:
    global __BI
    if isinstance(__BI, dict):
        __BI[name] = value
    else:
        setattr(__BI, name, value)


def overrideBI(name: str, value: Any) -> Any:
    global __BI
    old = readBI(name)
    writeBI(name, value)
    return old
