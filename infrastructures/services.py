import typing

from infrastructures.commands import *
from models.entities import *
from models.repositories import *
from models.services import *


class DefaultGuestbookService(IGuestbookService):
    def __init__(self, repository: IGuestbookRepository):
        if not isinstance(repository, IGuestbookRepository):
            raise TypeError()
        self.repository = repository

    def get(self, command: GuestbookGetCommand) -> typing.List[SavedPost]:
        return self.repository.get(command.count)

    def post(self, command: GuestbookPostCommand) -> SavedPost:
        post = Post(
            command.name,
            command.message,
            command.timestamp,
            command.remoteaddr
        )
        return self.repository.post(post)
