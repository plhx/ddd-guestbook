import abc
import typing

from core.models.entity import *


class IGuestbookCommand(metaclass=abc.ABCMeta):
    pass


class IGuestbookGetCommand(IGuestbookCommand):
    def __init__(self):
        self.count = None


class GuestbookGetCommand(IGuestbookGetCommand):
    def __init__(self, count: int):
        if not isinstance(count, int):
            raise TypeError()
        super().__init__()
        self.count = min(max(count, 1), 100)


class InvalidGuestbookAddCommandValue(Exception):
    pass


class IGuestbookAddCommand(IGuestbookCommand):
    def __init__(self):
        self.name = None
        self.message = None
        self.timestamp = None
        self.remote_addr = None


class GuestbookAddCommand(IGuestbookAddCommand):
    def __init__(self, name: Name, message: Message, timestamp: Timestamp,
        remote_addr: RemoteAddress):
        if not isinstance(name, Name):
            raise TypeError()
        if not isinstance(message, Message):
            raise TypeError()
        if not isinstance(timestamp, Timestamp):
            raise TypeError()
        if not isinstance(remote_addr, RemoteAddress):
            raise TypeError()
        super().__init__()
        self.name = name
        self.message = message
        self.timestamp = timestamp
        self.remote_addr = remote_addr
