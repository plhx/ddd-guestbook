import abc
import typing

import flask

from core.models.entity import *


class IGuestbookRequest(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def params(self, key: str, default: typing.Any=None) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def data(self, key: str, default: typing.Any=None) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def headers(self, key: str, default: typing.Any=None) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def remote_addr(self) -> RemoteAddress:
        raise NotImplementedError()


class GuestbookFlaskRequest(IGuestbookRequest):
    def params(self, key: str, default: typing.Any=None) -> str:
        if not isinstance(key, str):
            raise TypeError()
        return flask.request.args.get(key, default)

    def data(self, key: str, default: typing.Any=None) -> str:
        if not isinstance(key, str):
            raise TypeError()
        return flask.request.form.get(key, default)

    def headers(self, key: str, default: typing.Any=None) -> str:
        if not isinstance(key, str):
            raise TypeError()
        return flask.request.headers.get(key, default)

    def remote_addr(self) -> RemoteAddress:
        remote_addr = flask.request.headers.get(
            'X-Forwarded-For',
            flask.request.remote_addr
        )
        return RemoteAddress(remote_addr)
