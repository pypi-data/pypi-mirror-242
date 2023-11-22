from typing import NoReturn

from ..error.BuiltinLockedError import BuiltinLockedError
from ...lang import lang


__all__ = [
    "LockedFunction",
    "LockedClass",
    "LockedSingleton"
]


def LockedFunction(*args, **kwargs) -> NoReturn:
    """
        This Function is LOCKED. No information available now
        这个函数被锁住了，没有可用的信息
        """
    raise BuiltinLockedError(lang["locked.function"])


class LockedClass:
    """
    This Class is LOCKED. No information available now
    这个类型被锁住了，没有可用的信息
    """

    def __init__(self, *args, **kwargs) -> NoReturn:
        raise BuiltinLockedError(lang["locked.class"])


class LockedSingletonType:
    """
    This Object is LOCKED. No information available now
    这个对象被锁住了，没有可用的信息
    """

    def __str__(self) -> NoReturn:
        raise BuiltinLockedError(lang["locked.class"])

    __repr__ = __str__


LockedSingleton = LockedSingletonType()
