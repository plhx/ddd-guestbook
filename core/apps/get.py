import abc
from core.models import *


class IGuestbookGetUseCase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, command: IGuestbookGetCommand) -> None:
        raise NotImplementedError()


class GuestbookGetUseCase(IGuestbookGetUseCase):
    def __init__(self, repository: IGuestbookRepository):
        self.repository = repository

    def execute(self, command: IGuestbookGetCommand) -> typing.List[SavedPost]:
        return self.repository.get(command.count)
