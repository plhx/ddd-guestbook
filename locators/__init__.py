import typing

from models.repositories import *
from models.services import *
from infrastructures.repositories import *
from infrastructures.services import *


class GuestbookRepositoryLocator:
    @classmethod
    def resolve(cls, type: str) -> IGuestbookRepository:
        if not isinstance(type, str):
            raise TypeError()
        if type == 'memory':
            return GuestbookMemoryRepository
        elif type == 'sqlite':
            return GuestbookSQLiteRepository
        raise ValueError()


class GuestbookServiceLocator:
    @classmethod
    def resolve(cls, type: str) -> IGuestbookService:
        if not isinstance(type, str):
            raise TypeError()
        if type == 'default':
            return DefaultGuestbookService
        raise ValueError()
