#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import requests
from core.config import settings


def get_rank_rune(championId: int, position: str):
    """
    获取排位模式英雄符文
    """
    data = requests.get(settings.OPGG_RANK_RUNE_URL.format(championId, position)).json()
    return data['data']['rune_pages'][0]['builds'][0]


def get_nor_rune(championId: int, mode: str):
    """
    获取普通模式英雄符文
    """
    data = requests.get(settings.OPGG_NOR_RUNE_URL.format(mode, championId)).json()
    return data['data']['rune_pages'][0]['builds'][0]


def get_champ_position(championId: int) -> str:
    """
    获取英雄常用位置
    """
    data = requests.get(settings.OPGG_DATA_URL).json()
    for champion in data['data']:
        if champion['id'] == championId:
            if len(champion['positions']) > 0:
                position = champion['positions'][0]['name']
            else:
                position = 'mid'
            return position
