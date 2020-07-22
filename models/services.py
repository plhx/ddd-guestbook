import abc
import typing

import models.entities
import models.repositories


class IGuestbookCommand(metaclass=abc.ABCMeta):
    pass


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


class IGuestbookService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, command: GuestbookGetCommand) \
        -> typing.List[models.entities.SavedPost]:
        raise NotImplementedError()

    @abc.abstractmethod
    def post(self, command: GuestbookPostCommand) \
        -> typing.List[models.entities.SavedPost]:
        raise NotImplementedError()


class DefaultGuestbookService(IGuestbookService):
    def __init__(self, repository: models.repositories.IGuestbookRepository):
        if not isinstance(repository, \
            models.repositories.IGuestbookRepository):
            raise TypeError()
        self.repository = repository

    def get(self, command: GuestbookGetCommand) \
        -> typing.List[models.entities.SavedPost]:
        return self.repository.get(command.count)

    def post(self, command: GuestbookPostCommand) -> models.entities.SavedPost:
        post = models.entities.Post(
            command.name,
            command.message,
            command.timestamp,
            command.remoteaddr
        )
        return self.repository.post(post)
