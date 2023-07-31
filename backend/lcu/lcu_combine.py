#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
import json
from typing import Dict
from ordered_set import OrderedSet
from .lcu_base import Base
from collections import Counter, defaultdict
from utils.common import transformDate, async_timeit, get_gamemode_byQueue, check_teamup
from utils.config import config
from utils.opgg import get_rank_rune, get_nor_rune, get_champ_position
from core.config import settings
from .enums import gameMode


class lcu_combine(Base):

    async def banpick_roll(self, data: dict):
        """大乱斗抢英雄"""
        if config['autoBanPick']['roll']['enable'] and not self.champ_lock:
            prefers = OrderedSet(config['autoBanPick']['roll']['swap'])
            # 判断当前英雄是否为偏爱英雄
            for summoner in data['myTeam']:
                if summoner['summonerId'] == self._info['summonerId'] and summoner['championId'] in prefers:
                    return
            bench = OrderedSet([champion['championId'] for champion in data['benchChampions']])
            # 得到偏爱英雄与可选英雄交集
            for championId in prefers.intersection(bench):
                res = await self.champ_swap(championId)
                if res is None:
                    self.champ_lock = True  # 选完英雄锁定
                    return

    @async_timeit
    async def loot_dissolve(self):
        """
        智能分解战利品
        """
        tot_blue = tot_orange = 0
        loots: Dict[str, dict] = await self.get_loot()
        for loot_name, loot in loots.items():
            # 种类是需要 且 开启分解
            if loot['type'] not in config['loot'] or not config['loot'][loot['type']]['enable']:
                continue
            curSetting = config['loot'][loot['type']]
            # 不分解未拥有 且 未拥有
            if curSetting['sellNotOwned'] and loot['itemStatus'] == 'NONE':
                continue
            # 价格过低
            if curSetting['sellMinValue'] > loot['disenchantValue']:
                continue
            # 保留代币所需 且 代币存在
            if curSetting.get('isRemainForToken', False):
                token6 = f"CHAMPION_TOKEN_{loot['storeItemId']}-21"
                token7 = f"CHAMPION_TOKEN_{loot['storeItemId']}-21"
                # 判断存不存在这种英雄的代币,存在则不处理
                if token6 in loots or token7 in loots:
                    continue
            # 保留一个
            if curSetting['isRemainOne']:
                count = max(loot['count'] - 1, 1)
            else:
                count = loot['count']
            res = await self.dissolve(loot['type'] + '_disenchant', loot['lootId'], count)
            if "errorCode" in res:
                print(f"分解{loot_name} 数量{count} 失败")
            else:
                # ws发送分解成功消息
                print(f"分解{loot_name} 数量{count} 成功")
                if loot['displayCategories'] == 'CHAMPION':
                    tot_blue += loot['disenchantValue'] * count
                else:
                    tot_orange += loot['disenchantValue'] * count

    async def auto_rune(self, data: json):
        """自动配置符文"""
        if not config['autoUseRune'] or self.rune_lock:
            return
        championId = data['data']
        mode = get_gamemode_byQueue(await self.get_current_queue())
        if mode == 'rank':
            position = get_champ_position(championId)
            rune = get_rank_rune(championId, position)
        else:
            rune = get_nor_rune(championId, mode)
        perk_ids = rune['primary_rune_ids'] + rune['secondary_rune_ids'] + rune['stat_mod_ids']
        new_rune = {
            "name": "OP.GG",
            "order": rune['id'],
            "primaryStyleId": rune['primary_page_id'],
            "subStyleId": rune['secondary_page_id'],
            "selectedPerkIds": perk_ids,
            "current": True
        }
        all_runes = await self.get_all_runes()
        await self.delete_rune(all_runes[0]['id'])
        await self.set_rune(new_rune)
        self.rune_lock = True
        return await self.send_remarks(f"[RIVEN英雄联盟助手]已配置符文", "SELF")

    async def banpick_classic(self, data: json):
        """
        经典模式BP
        """
        if self.champ_lock:
            return
        cellId: int = None
        position: str = None
        for order in data['myTeam']:
            if order['summonerId'] == self._info['summonerId']:
                cellId = order['cellId']
                position = order['assignedPosition']
                break
        actions = data['actions']
        # 如果当前为BAN_PICK阶段则进入
        if data['timer']['phase'] == 'BAN_PICK':
            """
            进入条件：
            1.position为空 => 匹配模式
            2.配置文件打开pick
            """
            if not position and config['autoBanPick']['pick']['enable']:
                position = 'normal'
                for action in actions[0]:
                    if action['actorCellId'] == cellId:
                        pickActionId = action['id']
                        if not action['completed'] and action['isInProgress']:
                            # 取pickable和picks的交集
                            pickable = OrderedSet(await self.get_pickable())
                            picks = OrderedSet(config['autoBanPick']['pick'][position])
                            for pick in picks.intersection(pickable):
                                res = await self.champ_select(pick, pickActionId, 'pick')
                                if res is None:
                                    # 无返回值则选择成功
                                    self.champ_lock = True  # 选完英雄锁定
                                    break
                            return
            else:
                """
                actions[0]是ban的action
                actions[2:]是pick的action
                """
                for index, actionItem in enumerate(actions):
                    if index == 0 and config['autoBanPick']['ban']['enable']:
                        for action in actionItem[index]:
                            if action['actorCellId'] == cellId:
                                banActionId = action['id']
                                # isInProgress 和 not completed 才能banpick
                                if not action['completed'] and action['isInProgress']:
                                    # 取bannable和bans的交集
                                    bannable = OrderedSet(await self.get_bannable())
                                    bans = OrderedSet(config['autoBanPick']['ban'][position])
                                    for ban in bans.intersection(bannable):
                                        res = await self.champ_select(ban, banActionId, 'ban')
                                        if res is None:
                                            # 通过是否报错判断有没有交换成功
                                            print(f"[排位模式] 禁用英雄championId={ban}")
                                            break
                                    # 如果是BAN环节，就算没有ban成功也return
                                    return
                    elif index >= 2 and config['autoBanPick']['pick']['enable']:
                        for action in actionItem[index]:
                            if action['actorCellId'] == cellId:
                                pickActionId = action['id']
                                if not action['completed'] and action['isInProgress']:
                                    # 取pickable和picks的交集
                                    pickable = OrderedSet(await self.get_pickable())
                                    picks = OrderedSet(config['autoBanPick']['pick'][position])
                                    for pick in picks.intersection(pickable):
                                        res: dict = await self.champ_select(pick, pickActionId, 'pick')
                                        if res is None:
                                            # 通过是否报错判断有没有交换成功
                                            self.champ_lock = True  # 选完英雄锁定
                                            print(f"[排位模式] 选中英雄championId={pick}")
                                            break
                                    return

    @async_timeit
    async def get_rencent_20_data(self, puuid: str) -> dict:
        """
        获取近20场数据[(championId, win, lose,  rate , kda)]
        """
        res_1 = {}  # 英雄数据
        res_2 = {
            'total': 0,
            'win': 0,
            'lose': 0,
            'kill': 0,
            'assist': 0,
            'death': 0,
            'kda': 0,
            'gameIds': []
        }  # 对局数据
        res_3 = {
            'totalDamageDealt': [],
            'totalDamageTaken': [],
            'lane': {
                'TOP': 0,
                'JUNGLE': 0,
                'MIDDLE': 0,
                'ADC': 0,
                'SUPPORT': 0
            }
        }
        matches = (await self.get_rank_list_by_puuid(beginIdx=0, endIndex=19, puuid=puuid))['games']['games']
        for match in matches:
            if match['gameMode'] == gameMode.PRACTICE.value:
                continue
            data = match['participants'][0]
            time = transformDate(match['gameCreationDate'])
            championId = data['championId']
            kill = data['stats']['kills']
            assist = data['stats']['assists']
            death = data['stats']['deaths']
            kda = (kill + assist) / max(1, death)
            win = data['stats']['win']
            res_2['kill'] += kill
            res_2['assist'] += assist
            res_2['death'] += death
            res_2['win' if win else 'lose'] += 1
            res_2['total'] += 1
            res_2['gameIds'].append(match['gameId'])
            if championId in res_1:
                res_1[championId]['kda'] += kda
                res_1[championId]['win' if win else 'lose'] += 1
            else:
                res_1[championId] = {
                    'win': 1 if win else 0,
                    'lose': 1 if not win else 0,
                    'rate': 0,
                    'kda': kda
                }
            res_3['totalDamageDealt'].append(data['stats']['totalDamageDealt'])
            res_3['totalDamageTaken'].append(data['stats']['totalDamageTaken'])
            if data['timeline']['lane'] == 'BOTTOM':
                res_3['lane']['ADC' if data['timeline']['role'] == 'CARRY' else 'SUPPORT'] += 1
            elif data['timeline']['lane'] != 'NONE':
                res_3['lane'][data['timeline']['lane']] += 1
        # 计算kda和rate
        for championId in res_1.keys():
            number = max(res_1[championId]['win'] + res_1[championId]['lose'], 1)
            res_1[championId]['rate'] = res_1[championId]['win'] / number
            res_1[championId]['kda'] /= number
        res_2['kda'] = (res_2['kill'] + res_2['assist']) / max(res_2['death'], 1)
        res_2['rate'] = res_2['win'] / max(res_2['total'], 1)
        return [res_1, res_2, res_3]

    @async_timeit
    async def get_rank_summary(self, puuid: str) -> dict:
        """
        获得段位概要 （当前赛季单双排，当前赛季灵活组排， 最高段位）
        """
        data = await self.get_rank(puuid)
        queues = data['queues']
        return {
            'RANKED_FLEX_SR': {
                'tier': queues[0]['tier'],
                'division': queues[0]['division'],
                'win': queues[0]['wins'],
                'loss': queues[0]['losses'],
                'rate': queues[0]['wins'] / max(queues[0]['losses'] + queues[0]['wins'], 1)
            },
            'RANKED_SOLO_5x5': {
                'tier': queues[1]['tier'],
                'division': queues[1]['division'],
                'win': queues[1]['wins'],
                'loss': queues[1]['losses'],
                'rate': queues[0]['wins'] / max(queues[1]['losses'] + queues[1]['wins'], 1)
            },
            'Highest_Rank': {
                'tier': data['highestPreviousSeasonEndTier'],
                'division': data['highestPreviousSeasonEndDivision']
            }
        }

    async def get_teammate_info(self):
        """
        获得选择英雄时队友信息
        """
        summonerIds = await self.get_chatroom_summonerIds()
        players = []
        teamup= []
        for summonerId in summonerIds:
            summonerInfo = {} if summonerId == 0 else await self.get_info_by_id(summonerId)
            temp = await self.handle_player_detail(summonerInfo)
            players.append(temp)
            teamup.append({
                'summonerName': temp['summonerName'],
                'gameIds': temp['match']['gameIds']
            })
        teamup = check_teamup(teamup)
        return players, teamup

    async def get_players_info(self):
        """
        获得对局时全部召唤师信息
        """
        players = None
        # temp存数据， team存组队信息
        temp = {
            "ORDER": [],
            "CHAOS": []
        }
        team = {
            "ORDER": [],
            "CHAOS": []
        }
        for i in range(settings.GET_PLAYERLIST_RETRY_TIMES):
            players = await self.get_summonerName_ingame()
            if players is not None:
                break
            await asyncio.sleep(settings.GET_PLAYERLIST_INTERVAL)
        if players is None:
            return
        for player in players:
            if player['isBot']:
                continue
            summonerInfo = await self.get_info_by_name(player['summonerName'])
            # handle_player_detail 在这里加入gameIds
            player_info = await self.handle_player_detail(summonerInfo)
            temp[player['team']].append(player_info)
            team[player['team']].append({
                'summonerName': player_info['summonerName'],
                'gameIds': player_info['match']['gameIds']
            })
        team["ORDER"] = check_teamup(team["ORDER"])
        team["CHAOS"] = check_teamup(team["CHAOS"])
        return temp, team

    async def auto_report(self):
        """
        自动举报玩家
        """
        end = await self.get_end_data()
        for team in end['teams']:
            for player in team['players']:
                if player['summonerId'] != self._info['summonerId']:
                    print(await self.gameover_complaint(end['gameId'], "Negative Attitude, Verbal Abuse", "逃跑",
                                                        player['summonerId']))

    @async_timeit
    async def handle_match_detail(self, gameId: int):
        current_game = await self.get_match(gameId)
        analysis = {
            'summoners': {
                "max": {},
                "each": [{} for i in current_game['participants']],
            },
            'teams': [
                {
                    'totalInfo': defaultdict(int),
                    'maxInfo': defaultdict(int),
                    'summonerIdx': [],
                },
                {
                    'totalInfo': defaultdict(int),
                    'maxInfo': defaultdict(int),
                    'summonerIdx': [],
                },
            ],
        }
        for i, participant in enumerate(current_game['participants']):
            # 计算雷达图
            analysis['summoners']['each'][i]['Kda'] = round(
                (participant['stats']['kills'] + participant['stats']['assists']) / max(participant['stats']['deaths'],
                                                                                        1), 1)
            analysis['summoners']['max']['Kda'] = max(analysis['summoners']['max'].get('Kda', 0),
                                                      analysis['summoners']['each'][i]['Kda'])
            analysis['summoners']['each'][i]['DamageMinDealt'] = round(
                participant['stats']['totalDamageDealt'] / current_game['gameDuration'] * 60, 1)
            analysis['summoners']['max']['DamageMinDealt'] = max(analysis['summoners']['max'].get('DamageMinDealt', 0),
                                                                 analysis['summoners']['each'][i]['DamageMinDealt'])
            analysis['summoners']['each'][i]['DamageMinTaken'] = round(
                participant['stats']['totalDamageTaken'] / current_game['gameDuration'] * 60, 1)
            analysis['summoners']['max']['DamageMinTaken'] = max(analysis['summoners']['max'].get('DamageMinTaken', 0),
                                                                 analysis['summoners']['each'][i]['DamageMinTaken'])
            analysis['summoners']['each'][i]['DamageConversion'] = round(
                participant['stats']['totalDamageDealt'] / participant['stats']['goldEarned'])
            analysis['summoners']['max']['DamageConversion'] = max(
                analysis['summoners']['max'].get('DamageConversion', 0),
                analysis['summoners']['each'][i]['DamageConversion'])
            analysis['summoners']['each'][i]['GoldMinEarned'] = round(
                participant['stats']['goldEarned'] / current_game['gameDuration'] * 60, 1)
            analysis['summoners']['max']['GoldMinEarned'] = max(analysis['summoners']['max'].get('GoldMinEarned', 0),
                                                                analysis['summoners']['each'][i]['GoldMinEarned'])
            analysis['summoners']['each'][i]['Survivbility'] = round(100 / max(participant['stats']['deaths'], 1), 1)
            analysis['summoners']['max']['Survivbility'] = max(analysis['summoners']['max'].get('Survivbility', 0),
                                                               analysis['summoners']['each'][i]['Survivbility'])
            team_id = participant['teamId']
            analysis['teams'][team_id // 100 - 1]['summonerIdx'].append(i)
            # 计算队伍总数据
            for key, value in participant['stats'].items():
                analysis['teams'][team_id // 100 - 1]['totalInfo'][key] += value
                analysis['teams'][team_id // 100 - 1]['maxInfo'][key] = max(value,
                                                                            analysis['teams'][team_id // 100 - 1][
                                                                                'maxInfo'][key])
        analysis['teams'][0].update(current_game['teams'][0])
        analysis['teams'][0]['totalInfo'] = dict(analysis['teams'][0]['totalInfo'])
        analysis['teams'][0]['maxInfo'] = dict(analysis['teams'][0]['maxInfo'])
        # 不一定有两个队伍
        if len(current_game['teams']) > 1:
            analysis['teams'][1].update(current_game['teams'][1])
            analysis['teams'][1]['totalInfo'] = dict(analysis['teams'][1]['totalInfo'])
            analysis['teams'][0]['maxInfo'] = dict(analysis['teams'][0]['maxInfo'])
        return [current_game, analysis]

    async def handle_player_detail(self, summonerInfo: dict):
        """
        处理召唤师信息
        """
        temp = {}
        isBot = summonerInfo == {}
        temp['summonerId'] = 0 if isBot else summonerInfo['summonerId']
        temp['position'] = 'UNKNOWN'
        temp['summonerName'] = 'BOT' if isBot else summonerInfo['displayName']
        temp['profileIconId'] = 29 if isBot else summonerInfo['profileIconId']
        temp['match'] = {
            "source": 0,
            "kda": 0,
            "rate": 0,
            "gameIds": []
        }
        if not isBot:
            games = (await self.get_rank_list_by_puuid(0, 30, summonerInfo['puuid']))['games']['games']
            games = list(filter(lambda x: x['queueId'] in [420, 430, 440], games))
            temp["match"]["games"] = games[:7]
            temp["rank"] = (await self.get_rank(summonerInfo['puuid']))
            if not games:
                return temp
            temp['champions'] = [championId for championId, count in
                                 Counter(game['participants'][0]['championId'] for game in games).most_common(3)]
            temp['position'] = Counter(filter(lambda lane: lane != 'None',
                                              (game['participants'][0]['timeline']['lane'] for game in
                                               games))).most_common(1)[0][0]

            kill = assist = death = killingSprees = win = 0
            # 计算kda数据
            for game in games:
                win += game['participants'][0]['stats']['win']
                killingSprees += game['participants'][0]['stats']['killingSprees']
                kill += game['participants'][0]['stats']['kills']
                assist += game['participants'][0]['stats']['assists']
                death += game['participants'][0]['stats']['deaths']
                temp['match']['gameIds'].append(game['gameId'])
            temp['match']['kda'] = (kill + assist) / max(death, 1)
            temp['match']['rate'] = win / len(games)
            temp['match']['source'] = (temp['match']['kda'] * 10 * 0.4 + temp['match'][
                'rate'] * 100 * 0.4 + killingSprees * 0.2) * 10
        return temp

    async def create_55practice(self):
        """
        创建5v5训练营
        """
        return await self.create_lobby('PRACTICETOOL', 11, "LUX:自定义5V5训练营", 5)

    async def create_aram(self):
        """
        创建大乱斗
        """
        return await self.create_lobby('ARAM', 12, "LUX:自定义极地大乱斗", 5)

    async def send_remarks(self, msg: str, type: str):
        """
        发送牛马评分
        （前端判断发送逻辑）
        """
        return await self.send_msg_champselect(type, msg)


















