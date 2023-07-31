#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from fastapi import WebSocket
import json


class Ws:
    def __init__(self):
        self._ws: WebSocket = None

    def connect(self, ws: WebSocket):
        if self._ws is not None:
            return
        self._ws = ws

    def disconnect(self):
        self._ws = None

    async def broadcast(self, message: dict):
        """
        向前端广播消息
        """
        if self._ws is None:
            return
        await self._ws.send_json(message)
ws = Ws()
