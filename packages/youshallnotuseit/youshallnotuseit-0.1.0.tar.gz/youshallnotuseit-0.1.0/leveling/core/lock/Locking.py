from typing import Any

from .Locked import *
from ..overrider import overrideBI, writeBI


class __Cover:
    placeholder: Any
    __locked = {}

    @classmethod
    def lock(cls, name: str) -> None:
        cls.__locked[name] = overrideBI(name, cls.placeholder)

    @classmethod
    def unlock(cls, name: str) -> None:
        writeBI(name, cls.__locked[name])
        del cls.__locked[name]


class FunctionCover(__Cover):
    placeholder = LockedFunction


class ClassCover(__Cover):
    placeholder = LockedClass
