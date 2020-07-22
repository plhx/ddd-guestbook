import abc
import typing

import flask


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
