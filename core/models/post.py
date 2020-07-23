import datetime
import ipaddress
import typing

from core.models.entity import *


class Post:
    def __init__(self, name: Name, message: Message, timestamp: Timestamp,
        remote_addr: RemoteAddress):
        if not isinstance(name, Name):
            raise TypeError()
        if not isinstance(message, Message):
            raise TypeError()
        if not isinstance(timestamp, Timestamp):
            raise TypeError()
        if not isinstance(remote_addr, RemoteAddress):
            raise TypeError()
        self.name = name
        self.message = message
        self.timestamp = timestamp
        self.remote_addr = remote_addr


class SavedPost(Post):
    def __init__(self, post_id: PostId, name: Name, message: Message,
        timestamp: Timestamp, remote_addr: RemoteAddress):
        if not isinstance(post_id, PostId):
            raise TypeError()
        super().__init__(name, message, timestamp, remote_addr)
        self.post_id = post_id

    @classmethod
    def frompost(cls, post: Post, post_id: PostId) -> 'SavedPost':
        return cls(
            post_id,
            post.name,
            post.message,
            post.timestamp,
            post.remote_addr
        )
