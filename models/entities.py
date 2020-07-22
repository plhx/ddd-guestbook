import datetime
import ipaddress
import typing


class InvalidPostValueException(Exception):
    pass


class InvalidPostIdException(InvalidPostValueException):
    pass


class InvalidPostNameException(InvalidPostValueException):
    pass


class InvalidPostMessageException(InvalidPostValueException):
    pass


class InvalidPostTimestampException(InvalidPostValueException):
    pass


class Post:
    def __init__(self, name: str, message: str, timestamp: int,
        remoteaddr: typing.Union[int, str, None]):
        if not isinstance(name, str):
            raise TypeError()
        if not 0 < len(name) <= 32:
            raise InvalidPostNameException()
        if not isinstance(message, str):
            raise TypeError()
        if not 0 < len(message) <= 1024:
            raise InvalidPostMessageException()
        if not isinstance(timestamp, (int, float)):
            raise TypeError()
        if timestamp < 0:
            raise InvalidPostTimestampException()
        if remoteaddr is not None:
            remoteaddr = ipaddress.ip_address(remoteaddr).exploded
        self.name = name
        self.message = message
        self.timestamp = timestamp
        self.remoteaddr = remoteaddr


class SavedPost(Post):
    def __init__(self, id: int, name: str, message: str,
        timestamp: int, remoteaddr: typing.Union[int, str, None]):
        super().__init__(name, message, timestamp, remoteaddr)
        if not isinstance(id, int):
            raise InvalidPostIdException()
        self.id = id

    @classmethod
    def frompost(cls, post: Post, id: int) -> 'SavedPost':
        return cls(
            id,
            post.name,
            post.message,
            post.timestamp,
            post.remoteaddr
        )
