import abc
import typing

import flask

from core.models.post import *


class IGuestbookResponse(metaclass=abc.ABCMeta):
    def __init__(self):
        self.status = None


class GuestbookEmptyResponse(IGuestbookResponse):
    def __init__(self, status: int):
        if not isinstance(status, int):
            raise TypeError()
        super().__init__()
        self.status = status


class GuestbookGetResponse(IGuestbookResponse):
    def __init__(self, posts: typing.List[SavedPost], status: int):
        if not isinstance(posts, (list, tuple)):
            raise TypeError()
        super().__init__()
        self.posts = posts
        self.status = status


class GuestbookAddResponse(IGuestbookResponse):
    def __init__(self, post: SavedPost, status: int):
        if not isinstance(post, SavedPost):
            raise TypeError()
        super().__init__()
        self.post = post
        self.status = status


class IGuestbookResponseConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert(self, response: IGuestbookResponse) -> typing.Any:
        raise NotImplementedError()


class GuestbookFlaskResponseConverter(IGuestbookResponseConverter):
    def convert(self, response: IGuestbookResponse) -> flask.Response:
        if isinstance(response, GuestbookEmptyResponse):
            return flask.make_response({}, response.status)
        elif isinstance(response, GuestbookGetResponse):
            posts = []
            for post in response.posts:
                posts.append({
                    'id': post.post_id.value,
                    'name': post.name.value,
                    'message': post.message.value,
                    'timestamp': post.timestamp.value
                })
            return flask.make_response({'posts': posts}, response.status)
        elif isinstance(response, GuestbookAddResponse):
            return flask.make_response(
                {'posts': [{
                    'id': response.post.post_id.value,
                    'name': response.post.name.value,
                    'message': response.post.message.value,
                    'timestamp': response.post.timestamp.value,
                    'remote_addr': response.post.remote_addr.value
                }]},
                response.status
            )
        raise TypeError()
