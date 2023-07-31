#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
import urllib3
import requests
from typing import Any
from utils.config import config
from utils.common import async_timeit
from core.config import settings
from .enums import ROUTE, msgType
from typing import Dict

# 禁用警告
urllib3.disable_warnings()


class Base:
    def __init__(self) -> None:
        self._wllp = None
        self._cache = {}
        self._info = {}

    @property
    def valid(self) -> bool:
        return self._wllp is not None

    def get(self, key: str):
        if key not in self._cache:
            return None
        else:
            return self._cache[key]

    def set(self, key: str, value: Any):
        self._cache[key] = value

    async def close(self) -> None:
        if self._wllp is not None:
            self._wllp.close()

    @property
    def state(self):
        """
        获取当前状态
        """
        return self._wllp.rest_alive

    @property
    async def environment(self) -> str:
        """
        获取当前大区
        """
        if (env := self.get('environment')) is not None:
            return env

        req = await (await self._wllp.request("GET", ROUTE.environment)).json()
        env = req['environment']
        self.set('environment', env)
        return env

    async def available_bots(self) -> Dict[str, str]:
        """
        获取可用机器人
        """
        datas = await self._wllp.request("GET", "/lol-lobby/v2/lobby/custom/available-bots")
        bots = {bot["name"]: bot["id"] for bot in await datas.json()}
        return bots

    async def add_bot_by_id(self, championId: int, difficulty: str, teamId: str):
        """
        通过英雄ID添加机器人
        """
        bot = {
            "championId": championId,
            "botDifficulty": difficulty,
            "teamId": teamId
        }
        await self._wllp.request("POST", ROUTE.lobby_bot.value, data=bot)

    async def add_bot_by_name(self, championName: str, difficulty: str, teamId: str):
        """
        通过英雄名添加机器人
        """
        championId = await self.available_bots[championName]
        await self.add_bot_by_id(championId, difficulty, teamId)

    async def create_lobby(self, gameMode: str, mapId: int, lobbyName: str, teamSize: int) -> None:
        """
        创建自定义训练营
        """
        custom = {
            "customGameLobby": {
                "configuration": {
                    "gameMode": gameMode,
                    "gameMutator": "",
                    "gameServerRegion": "",
                    "mapId": mapId,
                    "mutators": {
                        "id": 1
                    },
                    "spectatorPolicy": "AllAllowed",
                    "teamSize": teamSize,
                },
                "lobbyName": lobbyName,
                "lobbyPassword": "",
            },
            "isCustom": True,
        }
        await self._wllp.request("POST", ROUTE.lobby.value, data=custom)

    async def accept(self) -> None:
        """
        接受对局请求
        """
        return await self._wllp.request("POST", ROUTE.accept_game)

    async def decline(self) -> None:
        """
        拒绝对局请求
        """
        await self._wllp.request("POST", ROUTE.decline_game)

    async def reconnect(self) -> None:
        """
        重新连接
        """
        await self._wllp.request("POST", ROUTE.reconnect_game)

    async def play_again(self):
        """
        再来一局
        """
        await self._wllp.request("GET", ROUTE.play_again)

    async def drop_avatar_box(self):
        """
        取下头像框
        """
        data = {
            'preferredBannerType': 'lastSeasonHighestRank',
            'preferredCrestType': 'prestige',
            'selectedPrestigeCrest': 0,
        }
        await self._wllp.request("PUT", ROUTE.regalia, data=data)

    async def drop_medal(self):
        """
        取下头衔勋章
        """
        data = {
            'challengeIds': [],
            'title': '',
        }
        # await

    async def set_name(self, new_name: str):
        """
        修改客户名用户名
        """
        data = {
            "name": new_name
        }
        await self._wllp.request("PUT", ROUTE.me, data=data)

    async def set_challenge_crystal_level(self, level: str):
        """
        修改阶位（不知道叫什么）
        """
        data = {
            "lol": {
                "challengeCrystalLevel": level
            }
        }
        await self._wllp.request("PUT", ROUTE.me, data=data)

    async def set_challenge_token(self, tokens: str):
        """
        修改勋章
        """
        data = {
            "lol": {
                "challengeTokensSelected": tokens
            }
        }
        await self._wllp.request("PUT", ROUTE.me, data=data)

    async def set_rank(self, rtier, rdivision, rqueue) -> None:
        """
        修改段位信息
        """
        data = {
            "lol": {
                "rankedLeagueQueue": rqueue,
                "rankedLeagueTier": rtier,
                "rankedLeagueDivision": rdivision
            }
        }
        await self._wllp.request("PUT", ROUTE.me, data=data)

    async def get_current_champ(self) -> str:
        """
        获取选中的英雄
        """
        return await self._wllp.request("GET", ROUTE.current_champion)

    async def grant_authority(self, summonerId: int) -> None:
        """
        赋予房间权限
        """
        await self._wllp.request("POST", ROUTE.promote.format(summonerId))

    async def search_match(self) -> None:
        """
        寻找对局
        """
        return await self._wllp.request("POST", ROUTE.search)

    async def cancel_search(self):
        """
        取消寻找对局
        """
        return await self._wllp.request("DELETE", ROUTE.search)

    async def invite(self, summonerId: int) -> None:
        """
        邀请玩家
        """
        data = [
            {"toSummonerId": summonerId}
        ]
        await self._wllp.request("POST", ROUTE.invite, data=data)

    async def revoke_invite(self, summonerId: int) -> None:
        """
        取消邀请
        """
        data = [
            {"toSummonerId": summonerId}
        ]
        await self._wllp.request("POST", ROUTE.revoke_invite, data=data)

    async def kick(self, summonerId: int) -> None:
        """
        踢人
        """
        await self._wllp.request("POST", ROUTE.kick.format(summonerId))

    async def switch_team(self):
        """
        切换队伍
        """
        return await self._wllp.request("POST", ROUTE.switch)

    async def set_sign(self, msg: str) -> None:
        """
        设置签名
        """
        data = {"statusMessage": msg}
        return await self._wllp.request("PUT", ROUTE.me, data=data)

    async def set_status(self, status: str):
        """
        设置状态
         * "chat"->在线
         * "away"->离开
         * "dnd"->游戏中
         * "offline"->离线
         * "mobile"->手机在线
        """
        data = {
            "availability": status
        }
        return await self._wllp.request("PUT", ROUTE.me, data=data)

    async def get_me(self):
        """获取个人信息"""
        return await (await self._wllp.request("GET", ROUTE.me)).json()

    async def current_summoner_info(self) -> str:
        """
        获取自己的召唤师信息
        """
        return await (await self._wllp.request('GET', ROUTE.current_summoner)).json()

    async def current_summoner_profile(self) -> str:
        """
        获取自己的召唤师详细信息
        """
        return await (await self._wllp.request('GET', ROUTE.current_summoner_profile)).json()

    async def get_online_time(self) -> float:
        """
        获取游戏时间
        """
        return (await self._wllp.request("GET", ROUTE.allgamedata)).json()['gameData']['gameTime']

    async def get_background_skin(self, heroId: int):
        """
        获取英雄皮肤
        """
        return await self._wllp.request("GET", ROUTE.champion_skin.format(heroId))

    async def msg_to_frient(self, summonerName: str, msg: str):
        """
        好友发消息
        """
        data = {
            "summonerName": summonerName,
            "msg": msg
        }
        await self._wllp.request("POST", ROUTE.chat_frient, data=data)

    async def get_team_division(self) -> str:
        """
        判断是红方还是蓝方
        """
        return (await self._wllp.request("GET", ROUTE.notification)).json()['mapSide']

    async def get_frient_list(self, refresh: bool = False) -> str:
        """
        获取好友列表
        """
        if refresh or (friends := self.get('friends')) is None:
            friends = (await self._wllp.request("GET", ROUTE.friend_list)).json()
            self.set("friends", friends)
        return friends

    async def get_info_by_name(self, summonerName: str) -> str:
        """
        用户名查找玩家
        """
        return await (await self._wllp.request("GET", ROUTE.summoner_by_name.format(summonerName))).json()

    async def get_info_by_id(self, summonerId: str) -> str:
        """
        id查找玩家
        """
        return await (await self._wllp.request("GET", ROUTE.summoner.format(summonerId))).json()

    async def get_info_by_puuid(self, puuid: str):
        """
        puuid查找玩家
        """
        return await (await self._wllp.request("GET", ROUTE.summoner_by_puuid.format(puuid))).json()

    async def get_profile_by_puuid(self, puuid: str):
        """
        puuid查找玩家概要信息
        """
        return await (await self._wllp.request("GET", ROUTE.summoner_profile_by_puuid.format(puuid))).json()

    async def get_rank(self, puuid: str):
        """
        查找段位
        """
        return await (await self._wllp.request("GET", ROUTE.rank.format(puuid))).json()

        # TODO: queues = data['queues']
        # rankInfo = RankInfo(queues[0]['tier'], queues[0]['division'], queues[0]['wins'], queues[0]['losses'],
        #                     queues[1]['tier'], queues[1]['division'], queues[1]['wins'], queues[1]['losses'],
        #                     data['highestPreviousSeasonEndTier'], data['highestPreviousSeasonEndDivision'])

    async def get_my_rank_List(self):
        """
        获得我的对局记录
        """
        return await (await self._wllp.request("GET", ROUTE.match_current_summoner)).json()

    async def get_rank_list_by_id(self, beginIdx: int, endIndex: int, summonerId: str):
        """
        通过id查找对局记录
        """
        return await (
            await self._wllp.request("GET", ROUTE.match_list_by_id.format(summonerId, beginIdx, endIndex))).json()

    @async_timeit
    async def get_rank_list_by_puuid(self, beginIdx: int, endIndex: int, puuid: str):
        """
        通过puuid查找对局记录
        """
        return await (
            await self._wllp.request("GET", ROUTE.match_list_by_puuid.format(puuid, beginIdx, endIndex))).json()

    async def get_rank_team(self) -> str:
        """
        获取对局双方信息
        """
        return (await self._wllp.request("GET", ROUTE.session)).json()

    async def set_position(self, first: str, second: str) -> None:
        """
        预选位:Position[first]
        """
        position = {
            "firstPreference": first,
            "secondPreference": second
        }
        await self._wllp.request("PUT", ROUTE.position, data=position)

    async def get_match(self, gameId: str) -> str:
        """
        通过游戏ID获取对局标准信息
        """
        return await (await self._wllp.request("GET", ROUTE.match_detail.format(gameId))).json()

    async def get_match_mode(self) -> int:
        """
        获得游戏模式
        430 匹配 420 单双排位 440灵活 450 大乱斗 云顶匹配 1090  云顶排位 1100 云顶狂暴 1130 云顶双人作战 1160
        """
        data = await (await self._wllp.request("GET", ROUTE.session)).json()
        if not data:
            return 0
        return data['gameData']['queue']['id'] if data['gameData']['queue']['id'] >= 0 else 430

    async def champ_select(self, championId: int, actionId: int, patchType: str) -> None:
        """
        选择禁用英雄
        """
        confirm = config['autoBanPick']['confirmSelect']
        data = {
            "completed": confirm,
            "type": patchType,
            "championId": championId
        }
        return await (await self._wllp.request("PATCH", ROUTE.bp_champion.format(actionId), data=data)).json()

    async def champ_swap(self, championId: int):
        """
        交换英雄
        """
        return await (await self._wllp.request("POST", ROUTE.swap_champion.format(championId)))

    """
     * @param skinId 皮肤id,长度5位
     *               比如:其中 13006，这个ID分为两部分 13 和 006,
     *               13是英雄id,6是皮肤id(不足3位,前面补0)
     */
    """

    async def set_background_skin(self, skinId: int):
        """
        生涯设置背景皮肤
        """
        data = {
            "backgroundSkinId": skinId
        }
        print(data)
        return await self._wllp.request("PUT", ROUTE.current_summoner_profile, data=data)

    async def reroll(self) -> None:
        """
        随机英雄
        """
        await self._wllp("POST", ROUTE.reroll)

    async def spectator_launch_by_name(self, summonerName: str, gameQueueType: str) -> None:
        """
        吊起观战
        """
        data = {
            'allowObserveMode': 'ALL',
            'dropInSpectateGameId': summonerName,
            'gameQueueType': gameQueueType
        }
        await self._wllp.request("POST", ROUTE.spectate, data=data)

    async def gameover_complaint(self, gameId: int, offenses: str, comment: str, summonerId: int):
        """
        游戏结束投诉玩家
        可选值为AFK（离开）、NEGATIVE_ATTITUDE（消极态度）、VERBAL_ABUSE（语言辱骂）、INTENTIONAL_FEEDING（蓄意送人头）、ASSISTING_ENEMY（协助敌方）、INAPPROPRIATE_NAME（不恰当的召唤师名字）、SPAMMING（刷屏）、OTHER（其他）
        """
        data = {
            "gameId": gameId,
            "offenses": offenses,
            "comment": comment,
            "reportedSummonerId": summonerId,
        }

        return await (await self._wllp.request("POST", ROUTE.complaint, data=data)).json()

    async def get_match_ids(self, puuid: str):
        """
        获取最近游戏id
        """
        return await (await self._wllp.request("GET", ROUTE.match_ids.format(puuid))).json()

    async def send_dialog_msg(self, msgContent: str, msgType: str):
        """
        发送客户端对话 (content疑似固定，不能自定义)
        """
        data = {
            "msgBody": [
                msgContent
            ],
            "msgType": msgType
        }
        return await self._wllp.request("POST", ROUTE.dialog_message, data=data)

    async def get_pickable(self):
        """
        获取可选英雄
        """
        return await (await self._wllp.request("GET", ROUTE.pickable)).json()

    async def get_bannable(self):
        """
        获取可禁英雄
        """
        return await (await self._wllp.request("GET", ROUTE.bannable)).json()

    async def get_conversations_id(self):
        """
        获取当前 房间号
        """
        for _ in range(settings.CONVERSATION_RETRY_TIME):
            data = await (await self._wllp.request("GET", ROUTE.conversations)).json()
            if data:
                for i in data:
                    # 并且存在"type": "championSelect"的房间
                    if i['type'] == 'championSelect':
                        return i['id']
            await asyncio.sleep(settings.CONVERSATION_RETRY_DELAY_SECOND)

    async def get_chatroom_summonerIds(self) -> list:
        """
        获取选人时房间队友的summonerId
        """
        cId = await self.get_conversations_id()
        data = await (await self._wllp.request('GET', ROUTE.conversation_msg.format(cId))).json()
        ids = []
        for msg in data:
            ids.append(msg['fromSummonerId'])
        return list(set(ids))

    @async_timeit
    async def get_summonerName_ingame(self):
        """
        获得对局中召唤师名字(分ORDER和CHAOS两个队伍)
        """
        session_url = "https://127.0.0.1:2999/liveclientdata/playerlist"
        try:
            playerlist = requests.get(session_url, verify=False).json()
            if isinstance(playerlist, list):
                temp = []
                for player in playerlist:
                    temp.append({
                        "summonerName": player['summonerName'],
                        "team": player['team'],
                        "isBot": player['isBot']
                    })
                return temp
            else:
                return None
        except Exception as e:
            print(e)
            return None

    async def get_champion_mastery(self, summonerId: str, limit: int):
        """
        获取英雄熟练度
        """
        return await (await self._wllp.request('GET', ROUTE.collection.format(summonerId, limit))).json()

    async def send_msg_champselect(self, type: str, msg: str):
        """
        选英雄期间发送消息
        """
        cId = await self.get_conversations_id()
        summoner = await self.current_summoner_info()
        data = {}
        if type == msgType.ALL.value:
            data = {
                'body': msg,
                'fromId': str(summoner['summonerId']),
                'fromSummonerId': summoner['summonerId'],
                'isHistorical': False,
                type: 'chat',
            }
        else:
            data = {
                'body': msg,
                'type': 'celebration'
            }
        await self._wllp.request('POST', ROUTE.conversation_msg.format(cId), data=data)

    async def createLobby(self, queueId: int):
        """
        创建模式
        """
        data = {
            'queueId': queueId
        }
        await self._wllp.request('POST', ROUTE.lobby, data=data)

    async def send_notification(self, title: str, details: str) -> None:
        """
        发送客户端消息
        """
        data = {
            'backgroundUrl': '',
            'created': '',
            'critical': True,
            'data': {
                'details': details,
                'title': title,
            },
            'detailKey': 'pre_translated_details',
            'dismissible': True,
            'expires': '',
            'iconUrl': '',
            'id': 0,
            'source': '',
            'state': 'toast',
            'titleKey': 'pre_translated_title',
            'type': 'ranked_summary',
        }
        await self._wllp.request('POST', ROUTE.notification, data=data)

    async def get_me_chat(self):
        """
        获取当前玩家聊天信息
        """
        return await (await self._wllp.request("GET", ROUTE.me)).json()

    async def put_me_chat(self, info: dict):
        """
        修改当前玩家聊天信息
        """
        await self._wllp.request("PUT", ROUTE.me, data=info)

    async def get_all_runes(self):
        """
        获取所有符文配置
        """
        return await (await self._wllp.request("GET", ROUTE.rune))

    async def set_rune(self, rune):
        """
        应用一套符文配置
        """
        await self._wllp.request("POST", ROUTE.rune, data=rune)

    async def delete_rune(self, runeId: int):
        """
        删除一套符文配置
        """
        await self._wllp.request("DELETE", ROUTE.rune + f'/{runeId}')

    async def quit_select_champ(self):
        """
        强制秒退
        """
        return await (await self._wllp.request('POST',
                                               '/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","quitV2",""]',
                                               data=None)).json()

    async def update_icon(self, profileIconId: int):
        """
        更新召唤师头像
        """
        data = {
            "icon": profileIconId
        }
        return await self._wllp.request("PUT", ROUTE.me, data=data)

    async def get_friend_record(self):
        """
        获得列表好友信息(加好友时间，昵称，老朋友)
        """
        return await (await self._wllp.request("GET", ROUTE.friend_record)).json()

    async def get_chat_settings(self):
        """
        获得聊天设置
        """
        return await (await self._wllp.request("GET", ROUTE.chat_setting)).json()

    async def get_setting(self):
        """
        获取设置
        """
        return await (await self._wllp.request("GET", ROUTE.settings)).json()

    async def set_setting(self, new_setting: dict):
        """
        修改设置
        """
        return await self._wllp.request("PATCH", ROUTE.settings, data=new_setting)

    async def get_input_setting(self):
        """
        获取输入设置
        """
        return await (await self._wllp.request("GET", ROUTE.input_settings)).json()

    async def set_input_setting(self, new_input_setting: dict):
        """
        修改输入设置
        """
        return await self._wllp.request("PATCH", ROUTE.input_settings, data=new_input_setting)

    async def get_input_setting_schema(self):
        """
        获取输入设置模式
        """
        return await (await self._wllp.request("GET", ROUTE.input_settings_schema)).json()

    async def get_setting_schema(self):
        """
        获取设置模式
        """
        return await (await self._wllp.request("GET", ROUTE.settings_schema)).json()

    async def refresh_loot(self):
        """
        刷新战利品接口
        """
        return await self._wllp.request("POST", ROUTE.refresh_loot)

    async def get_loot(self):
        """
        获取战利品信息
        """
        return await (await self._wllp.request("GET", ROUTE.loot_map)).json()

    async def dissolve(self, recipeName: str, lootId: str, repeat):
        """
        分解战利品
        """
        data = [lootId]
        return await (await self._wllp.request("POST", ROUTE.dissolve.format(recipeName, repeat), data=data)).json()

    async def get_end_data(self):
        """
        获得游戏结束信息
        """
        return await (await self._wllp.request("GET", ROUTE.eog)).json()

    async def get_skins(self, championId: int):
        """
        获取英雄皮肤信息
        """
        res = await (await self._wllp.request("GET", ROUTE.champion_skin.format(championId))).json()
        return res['skins']