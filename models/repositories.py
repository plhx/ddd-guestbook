import abc
import sqlite3
import typing

import models.entities


class IGuestbookRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, count: int) -> [models.entities.Post]:
        raise NotImplementedError()

    @abc.abstractmethod
    def post(self, post: models.entities.Post) -> models.entities.SavedPost:
        raise NotImplementedError()
