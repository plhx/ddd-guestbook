import abc
import typing

from models.commands import *
from models.entities import *


class IGuestbookService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, command: IGuestbookCommand) -> typing.List[SavedPost]:
        raise NotImplementedError()

    @abc.abstractmethod
    def post(self, command: IGuestbookCommand) -> typing.List[SavedPost]:
        raise NotImplementedError()
