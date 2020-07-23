import abc
import typing

from core.models.post import *


class IGuestbookRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, count: int) -> typing.List[SavedPost]:
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self, post: Post) -> None:
        raise NotImplementedError()
