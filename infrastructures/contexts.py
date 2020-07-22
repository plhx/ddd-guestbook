from models.contexts import *


class GuestbookRepositoryMemoryContext(IGuestbookRepositoryContext):
    pass


class GuestbookRepositoryDatabaseContext(IGuestbookRepositoryContext):
    def __init__(self, path: str):
        if not isinstance(path, str):
            raise TypeError()
        self.path = path
