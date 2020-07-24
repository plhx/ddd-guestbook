import abc
import colorsys
import ipaddress
import random

from core.models.entity import *


class Color:
    def __init__(self, red: int, green: int, blue: int):
        if not isinstance(red, int):
            raise TypeError()
        if not isinstance(green, int):
            raise TypeError()
        if not isinstance(blue, int):
            raise TypeError()
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)

    @property
    def hex(self):
        return '#{:02x}{:02x}{:02x}'.format(self.red, self.green, self.blue)


class IRemoteAddressColorConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert(self, remote_addr: RemoteAddress) -> Color:
        raise NotImplementedError()


class RemoteAddressColorConverter(IRemoteAddressColorConverter):
    def convert(self, remote_addr: RemoteAddress) -> Color:
        x = int.from_bytes(
            ipaddress.ip_address(remote_addr.value).packed,
            'little'
        )
        r = random.Random(x ^ 0x55555555)
        r, g, b = colorsys.hls_to_rgb(
            r.random(),
            r.random() / 2,
            r.random() / 4 + 0.75
        )
        return Color(int(r * 255), int(g * 255), int(b * 255))
