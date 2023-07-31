#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import aiofiles
from core.config import settings


class Config:
    def __init__(self):
        self._data = {}
        self.loads()

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    @property
    def data(self):
        return self._data

    def loads(self):
        with open(settings.CONFIG_PATH, 'r', encoding=settings.CONFIG_CODING) as f:
            self._data = json.load(f)

    async def save(self, new_config: dict):
        """异步保存config"""
        self._data = new_config
        async with aiofiles.open(settings.CONFIG_PATH, 'w') as f:
            await f.write(json.dumps(self._data))

config = Config()