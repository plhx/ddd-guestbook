import abc
import sqlite3
import typing

import models.entities


class IGuestbookRepositoryContext(metaclass=abc.ABCMeta):
    pass


class GuestbookRepositoryMemoryContext(IGuestbookRepositoryContext):
    pass


class GuestbookRepositoryDatabaseContext(IGuestbookRepositoryContext):
    def __init__(self, path: str):
        if not isinstance(path, str):
            raise TypeError()
        self.path = path


class IGuestbookRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, count: int) -> [models.entities.Post]:
        raise NotImplementedError()

    @abc.abstractmethod
    def post(self, post: models.entities.Post) -> models.entities.SavedPost:
        raise NotImplementedError()


class GuestbookMemoryRepository(IGuestbookRepository):
    def __init__(self, context: IGuestbookRepositoryContext):
        self.posts = []

    def get(self, count: int) -> [models.entities.SavedPost]:
        if count < 0:
            raise ValueError()
        return self.posts[-count:]

    def post(self, post: models.entities.Post) -> models.entities.SavedPost:
        id = self.posts[-1].id + 1 if self.posts else 0
        saved_post = models.entities.SavedPost.frompost(post, id)
        self.posts.append(saved_post)
        return saved_post


class GuestbookSQLiteRepository(IGuestbookRepository):
    def __init__(self, context: IGuestbookRepositoryContext):
        if not isinstance(context, IGuestbookRepositoryContext):
            raise TypeError()
        self.context = context
        with sqlite3.connect(self.context.path) as con:
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS guestbook (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [message] TEXT NOT NULL,
                [timestamp] REAL NOT NULL,
                [remoteaddr] TEXT
            )''')
            con.commit()

    def get(self, count: int) -> typing.List[models.entities.SavedPost]:
        with sqlite3.connect(self.context.path) as con:
            cur = con.cursor()
            cur.execute(
                '''SELECT [id], [name], [message], [timestamp], [remoteaddr]
                    FROM guestbook ORDER BY [id] DESC LIMIT ?''',
                (count,)
            )
            result = []
            for row in cur.fetchall():
                result.append(models.entities.SavedPost(*row))
            return result

    def post(self, post: models.entities.Post) -> models.entities.SavedPost:
        with sqlite3.connect(self.context.path) as con:
            cur = con.cursor()
            try:
                cur.execute(
                    '''INSERT INTO guestbook
                        (name, message, timestamp, remoteaddr) VALUES
                        (?, ?, ?, ?)''',
                    (post.name, post.message, post.timestamp, post.remoteaddr)
                )
                cur.execute(
                    '''SELECT [id], [name], [message], [timestamp], [remoteaddr]
                        FROM guestbook ORDER BY [id] DESC LIMIT 1'''
                )
            except sqlite3.Error:
                con.rollback()
            else:
                con.commit()
                return models.entities.SavedPost(*cur.fetchone())
