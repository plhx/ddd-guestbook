import abc
import typing

import flask

import models.entities


class IGuestbookResponse(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def status(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def to_dict(self) -> typing.Dict:
        raise NotImplementedError()

    def flask(self) -> flask.Response:
        return flask.make_response(self.to_dict(), self.status)


class GuestbookNullResponse(IGuestbookResponse):
    def __init__(self, _status: int):
        if not isinstance(_status, int):
            raise TypeError()
        self._status = _status

    @property
    def status(self) -> int:
        return self._status

    def to_dict(self) -> typing.Dict:
        return {}


class GuestbookGetResponse(IGuestbookResponse):
    def __init__(self, posts: typing.List[models.entities.SavedPost],
        _status: int):
        self.posts = posts
        self._status = _status

    @property
    def status(self) -> int:
        return self._status

    def to_dict(self) -> typing.Dict:
        posts = []
        for post in self.posts:
            posts.append({
                'id': post.id,
                'name': post.name,
                'message': post.message,
                'timestamp': post.timestamp,
                #'remoteaddr': post.remoteaddr
            })
        return {'posts': posts}


class GuestbookPostResponse(IGuestbookResponse):
    def __init__(self, post: models.entities.SavedPost, _status: int):
        self.post = post
        self._status = _status

    @property
    def status(self) -> int:
        return self._status

    def to_dict(self) -> typing.Dict:
        return {'posts': [{
            'id': self.post.id,
            'name': self.post.name,
            'message': self.post.message,
            'timestamp': self.post.timestamp,
            'remoteaddr': self.post.remoteaddr
        }]}
