import sqlite3

from core.models.entity import *
from core.models.post import *
from core.models.repository import *
from infrastructures.context import *


class GuestbookMemoryRepository(IGuestbookRepository):
    def __init__(self, context: IGuestbookRepositoryContext):
        self.posts = []

    def get(self, count: int) -> [SavedPost]:
        if count < 0:
            raise ValueError()
        return self.posts[-count:]

    def add(self, post: Post) -> SavedPost:
        if self.posts:
            post_id = self.posts[-1].post_id + 1
        else:
            post_id = PostId(0)
        saved_post = SavedPost.frompost(post, post_id)
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
                [post_id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [message] TEXT NOT NULL,
                [timestamp] REAL NOT NULL,
                [remote_addr] TEXT
            )''')
            con.commit()

    def get(self, count: int) -> typing.List[SavedPost]:
        with sqlite3.connect(self.context.path) as con:
            cur = con.cursor()
            cur.execute(
                '''SELECT [post_id], [name], [message], [timestamp], [remote_addr]
                    FROM guestbook ORDER BY [post_id] DESC LIMIT ?''',
                (count,)
            )
            result = []
            for post_id, name, message, timestamp, remote_addr in cur.fetchall():
                saved_post = SavedPost(
                    PostId(post_id),
                    Name(name),
                    Message(message),
                    Timestamp(timestamp),
                    RemoteAddress(remote_addr)
                )
                result.append(saved_post)
            return result

    def add(self, post: Post) -> SavedPost:
        with sqlite3.connect(self.context.path) as con:
            cur = con.cursor()
            try:
                cur.execute(
                    '''INSERT INTO guestbook
                        (name, message, timestamp, remote_addr) VALUES
                        (?, ?, ?, ?)''',
                    (
                        post.name.value,
                        post.message.value,
                        post.timestamp.value,
                        post.remote_addr.value
                    )
                )
                cur.execute(
                    '''SELECT [post_id], [name], [message], [timestamp],
                        [remote_addr] FROM
                        guestbook ORDER BY [post_id] DESC LIMIT 1'''
                )
            except sqlite3.Error:
                con.rollback()
                raise
            else:
                con.commit()
                post_id, name, message, timestamp, remote_addr = cur.fetchone()
                return SavedPost(
                    PostId(post_id),
                    Name(name),
                    Message(message),
                    Timestamp(timestamp),
                    RemoteAddress(remote_addr)
                )
