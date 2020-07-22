import typing

from models.commands import *


class GuestbookGetCommand(IGuestbookCommand):
    def __init__(self, count: int):
        self.count = min(max(count, 1), 100)


class GuestbookPostCommand(IGuestbookCommand):
    def __init__(self, name: str, message: str, timestamp: int,
        remoteaddr: typing.Union[int, str, None]):
        self.name = name
        self.message = message
        self.timestamp = timestamp
        self.remoteaddr = remoteaddr
