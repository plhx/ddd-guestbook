import abc
import typing

import flask

from core.models.post import *
from presentations.color import *


class IHTTPResponse(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = None
        self.status = None
        self.headers = None


class HTTPResponse(IHTTPResponse):
    def __init__(self, data: typing.Union[bytes, str, dict], status: int,
        headers: typing.Dict[str, str]):
        if not isinstance(data, (bytes, str, dict)):
            raise TypeError()
        if not isinstance(status, int):
            raise TypeError()
        if not isinstance(headers, dict):
            raise TypeError()
        super().__init__()
        self.data = data
        self.status = status
        self.headers = headers


class RenderHTMLResponse(IHTTPResponse):
    def __init__(self, path: str):
        if not isinstance(path, str):
            raise TypeError()
        self.data = path


class GuestbookResponse(IHTTPResponse):
    def __init__(self, posts: typing.List[SavedPost], status: int):
        if not isinstance(posts, (list, tuple)):
            raise TypeError()
        super().__init__()
        self.data = posts
        self.status = status


class IHTTPResponseConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert(self, response: IHTTPResponse):
        raise NotImplementedError()


class FlaskResponseConverter(IHTTPResponseConverter):
    def convert(self, response: IHTTPResponse):
        if isinstance(response, HTTPResponse):
            return flask.make_response(
                response.data,
                response.status,
                headers=headers
            )
        elif isinstance(response, RenderHTMLResponse):
            return flask.render_template(response.data)
        elif isinstance(response, GuestbookResponse):
            posts = []
            converter = RemoteAddressColorConverter()
            for post in response.data:
                posts.append({
                    'id': post.post_id.value,
                    'name': post.name.value,
                    'message': post.message.value,
                    'timestamp': post.timestamp.value,
                    'color': converter.convert(post.remote_addr).hex
                })
            return flask.make_response({'posts': posts}, response.status)
        raise TypeError()
