from ctypes import *
import sys
import time

class LampSmartProAPI():

    def __init__(self):
        self._so_file = "/config/custom_components/lampsmartpro/liblampify.so"
        self._libLamp = CDLL(self._so_file)

    def turn_on(self):
        ret = self._libLamp.decodeCommand(b"q", b"on")
        return ret

    def turn_off(self):
        ret = self._libLamp.decodeCommand(b"q", b"off")
        return ret

    def setup(self):
        ret = self._libLamp.decodeCommand(b"q", b"setup")
        return ret

    def cold(self, level):
        ret = self._libLamp.decodeCommand(b"q", b"cold", str(level).encode())
        return ret

    def warm(self, level):
        ret = self._libLamp.decodeCommand(b"q", b"warm", str(level).encode())
        return ret

    def dual(self, level):
        ret = self._libLamp.decodeCommand(b"q", b"dual", str(level).encode())
        return ret


def main():
    api = LampSmartProAPI()
    api.setup()
    api.turn_on()
    api.turn_off()
