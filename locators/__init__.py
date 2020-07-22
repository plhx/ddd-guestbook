import typing

import models.repositories
import models.services


class GuestbookRepositoryLocator:
    @classmethod
    def resolve(cls, type: str) -> models.repositories.IGuestbookRepository:
        if not isinstance(type, str):
            raise TypeError()
        if type == 'memory':
            return models.repositories.GuestbookMemoryRepository
        elif type == 'sqlite':
            return models.repositories.GuestbookSQLiteRepository
        raise ValueError()


class GuestbookServiceLocator:
    @classmethod
    def resolve(cls, type: str) -> models.services.IGuestbookService:
        if not isinstance(type, str):
            raise TypeError()
        if type == 'default':
            return models.services.DefaultGuestbookService
        raise ValueError()
