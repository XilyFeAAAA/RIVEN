#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from .enums import *
from time import time


def Connected(_flag: bool = True):
    return {
        'type': WebSocketMessageType.CONNECT.value if _flag else WebSocketMessageType.DISCONNECT.value,
        'timestamp': time()
    }
