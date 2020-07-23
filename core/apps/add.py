import abc

from core.models.command import *
from core.models.repository import *


class IGuestbookAddUseCase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, command: IGuestbookAddCommand) -> None:
        raise NotImplementedError()


class GuestbookAddUseCase(IGuestbookAddUseCase):
    def __init__(self, repository: IGuestbookRepository):
        self.repository = repository

    def execute(self, command: IGuestbookAddCommand) -> SavedPost:
        post = Post(
            command.name,
            command.message,
            command.timestamp,
            command.remote_addr
        )
        return self.repository.add(post)
