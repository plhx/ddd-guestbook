import ipaddress
import time


class PostId:
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError()
        if value < 0:
            raise ValueError()
        self.value = value

    def __add__(self, other: int):
        if not isinstance(other, int):
            raise TypeError()
        return self.__class__(self.value + other)


class Name:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError()
        if not 1 <= len(value) <= 32:
            raise ValueError()
        self.value = value


class Message:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError()
        if not 1 <= len(value) <= 1024:
            raise ValueError()
        self.value = value


class Timestamp:
    def __init__(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError()
        if value < 0:
            raise ValueError()
        self.value = float(value)

    @classmethod
    def now(cls):
        return cls(time.time())


class RemoteAddress:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError()
        self.value = ipaddress.ip_address(value).exploded
