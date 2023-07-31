#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
import willump
from ws import ws
from utils.config import config
from lcu.lcu_combine import lcu_combine


class Lcu(lcu_combine):
    def __init__(self):
        super().__init__()
        self.events = {
            '/lol-summoner/v1/': self.summoner_subscription,
            '/lol-gameflow/v1/gameflow-phase': self.gameflow_subscription,
            '/lol-champ-select/v1/session': self.champselect_subscription
        }

    async def run(self) -> bool:
        self._wllp = await willump.start()
        self._info = await self.current_summoner_info()
        all_events_subscription = await self._wllp.subscribe("OnJsonApiEvent", default_handler=self.default_handler)
        for endpoint, handler in self.events.items():
            self._wllp.subscription_filter_endpoint(all_events_subscription, endpoint, handler=handler)
        return self._wllp is None

    async def default_handler(self, data):
        # print(data)
        pass

    async def gameflow_subscription(self, data):
        await ws.broadcast(data)
        if data['data'] == 'ReadyCheck':
            """自动接受对局"""
            if config['autoAccept']['enable']:
                await asyncio.sleep(config['autoAccept']['delay'])
                await self.accept()
        elif data['data'] == 'InProgress':
            pass
        elif data['data'] == 'EndOfGame':
            """举报"""
            await self.auto_report()

    @staticmethod
    async def summoner_subscription(data):
        """这个事件处理游戏状态"""
        await ws.broadcast(data)

    async def champselect_subscription(self, data):
        """
        处理BANPICK
        INFO: 如果benchEnabled为真即为摇筛模式
              否则为正常bp
        """
        if data['data']['benchEnabled']:
            await self.banpick_roll(data['data'])
        else:
            await self.banpick_classic(data['data'])

lcu = Lcu()