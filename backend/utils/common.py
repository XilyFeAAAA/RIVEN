import functools

import pytz
import json
import time
import aiofiles
from pathlib import Path
from datetime import datetime


def transformDate(date: str):
    # 将字符串转换为 datetime 对象，注意 UTC 时间的时区是 'Z'
    utc_time = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    # 将 UTC 时间转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = utc_time.replace(tzinfo=pytz.utc).astimezone(beijing_tz)
    # 提取出月份和日期
    return beijing_time.strftime('%m-%d')


async def save_setting(path: Path, data: dict):
    async with aiofiles.open(path, 'w') as f:
        await f.write(json.dumps(data))


async def read_setting(path: Path):
    async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
        content = await f.read()
    return json.loads(content)


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


def async_timeit(async_func):
    @functools.wraps(async_func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        res = await async_func(*args, **kwargs)
        end = time.time()
        print(f"{async_func.__name__} is executed for {end - start}s")
        return res

    return wrapper


def get_gamemode_byQueue(queue) -> str:
    if queue == 420 or queue == 430 or queue == 440: return 'rank'
    if queue == 450: return 'aram'
    if queue == 900 or queue == 1010 or queue == 1900: return 'urf'
    return 'rank'


def check_teamup(team):
    """
    组队检测
    """
    arr1 = []
    arr2 = []
    for i in range(len(team)):
        for j in range(i + 1, len(team)):
            overlap = list(set(team[i]['gameIds']) & set(team[j]['gameIds']))
            if len(overlap) >= 2:
                if team[i]['summonerName'] not in arr1 and team[j]['summonerName'] not in arr1:
                    if len(arr1) == 0:
                        if team[i]['summonerName'] not in arr1:
                            arr1.append(team[i]['summonerName'])
                        if team[j]['summonerName'] not in arr1:
                            arr1.append(team[j]['summonerName'])
                    else:
                        if team[i]['summonerName'] not in arr2:
                            arr2.append(team[i]['summonerName'])
                        if team[j]['summonerName'] not in arr2:
                            arr2.append(team[j]['summonerName'])
                if team[i]['summonerName'] in arr1 or team[j]['summonerName'] in arr1:
                    if team[i]['summonerName'] not in arr1:
                        arr1.append(team[i]['summonerName'])
                    if team[j]['summonerName'] not in arr1:
                        arr1.append(team[j]['summonerName'])
    if len(arr1) == 1:
        arr1 = []
    if len(arr2) == 1:
        arr2 = []
    print(arr1, arr2)
    return arr1, arr2
