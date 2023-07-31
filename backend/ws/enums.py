#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from enum import Enum


class WebSocketMessageType(Enum):
    CONNECT = 1
    DISCONNECT = 2
    MESSAGE = 3
