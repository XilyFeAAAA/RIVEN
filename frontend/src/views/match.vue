<template>
    <div class="px-8 pb-2 w-full h-full overflow-hidden">
        <div class="w-full h-full flex flex-col" ref="container">
            <div class="w-full h-12 rounded-lg shadow my-4 px-4 flex items-center">
                <template v-if="summoner">
                    <div>
                        <profileImg
                            class="rounded-full"
                            width="35"
                            :profileIconId="summoner.profileIconId"
                        />
                    </div>
                    <div class="mx-5">
                        <span>{{ summoner.displayName }}</span>
                    </div>
                </template>
            </div>
            <div class="cp-height w-full flex">
                <div class="h-full w-[256px] flex flex-col rounded-lg shadow">
                    <div class="w-full flex-1 overflow-y-auto non-scroll-bar min-w-[250px]">
                        <div
                            v-for="(game, idx) in games"
                            :key="game"
                            class="item select-none cursor-pointer h-[86px] w-full px-5 flex items-center justify-center"
                            :style="itemStyle(game.gameId)"
                            @click="onSelectGame(game.gameId)"
                        >
                            <div class="flex justify-between items-center w-full h-14">
                                <div class="h-full flex items-center">
                                    <championImg
                                        class="rounded-md"
                                        width="50"
                                        :championId="game.participants[0].championId"
                                    />
                                </div>
                                <div class="h-full flex flex-col justify-between">
                                    <div
                                        class="flex justify-center items-center w-[73px] py-[2px] rounded-sm"
                                        :style="{
                                            backgroundColor: game.participants[0].stats.win
                                                ? '#ecf2ff'
                                                : '#fbebeb',
                                        }"
                                    >
                                        <span
                                            class="font-bold text-red-400"
                                            :style="{
                                                color: !game.participants[0].stats.win
                                                    ? 'rgba(248,133,133)'
                                                    : '#5383e8',
                                            }"
                                            >{{ game.participants[0].stats.kills }}-{{
                                                game.participants[0].stats.deaths
                                            }}-{{ game.participants[0].stats.assists }}</span
                                        >
                                    </div>
                                    <div class="flex justify-center">
                                        <span class="font-bold text-gray-400 text-sm">
                                            {{ webConfig.queue[game.queueId] }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex flex-col h-full">
                                    <div class="flex px-4 py-[2px] rounded-sm bg-[#fdf1e1]">
                                        <span class="font-bold text-orange-500">
                                            {{ formatMMDD(game.gameCreationDate) }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="h-12 flex justify-evenly items-center">
                        <div
                            class="h-10 w-10 flex justify-center items-center rounded-full cursor-pointer hover:bg-slate-100 active:bg-slate-200"
                            @click="pageDown"
                        >
                            <span class="mdi mdi-chevron-left text-2xl"></span>
                        </div>
                        <div class="h-7 w-7">
                            <div
                                class="border border-solid h-full w-full flex justify-center items-center rounded-md"
                            >
                                <span class="text-slate-600 select-none">{{ page }}</span>
                            </div>
                        </div>
                        <div
                            class="h-10 w-10 flex justify-center items-center rounded-full cursor-pointer hover:bg-slate-100 active:bg-slate-200"
                            @click="pageUp"
                        >
                            <span class="mdi mdi-chevron-right text-2xl"></span>
                        </div>
                    </div>
                </div>
                <div class="ml-3 px-8 py-3 h-full flex flex-col flex-1 rounded-lg shadow">
                    <template v-if="current_game_detail && current_game && !onloading">
                        <div class="w-full flex justify-between items-center">
                            <div class="w-full flex items-center select-none max-w-[750px]">
                                <div class="flex-auto">
                                    <div class="flex justify-center">
                                        <span class="text-gray-400 font-bold">对局日期</span>
                                    </div>
                                    <div class="flex justify-center py-1">
                                        <span class="text-sm tracking-wider">
                                            {{ formatMMDD(current_game.gameCreationDate) }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex-auto">
                                    <div class="flex justify-center">
                                        <span class="text-gray-400 font-bold">对局类型</span>
                                    </div>
                                    <div class="flex justify-center py-1">
                                        <span class="text-sm tracking-wider">
                                            {{ webConfig.queue[current_game.queueId] }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex-auto">
                                    <div class="flex justify-center">
                                        <span class="text-gray-400 font-bold">开始时间</span>
                                    </div>
                                    <div class="flex justify-center py-1">
                                        <span class="text-sm tracking-wider">
                                            {{ formatHHMM(current_game.gameCreationDate) }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex-auto">
                                    <div class="flex justify-center">
                                        <span class="text-gray-400 font-bold">对局时间</span>
                                    </div>
                                    <div class="flex justify-center py-1">
                                        <span class="text-sm tracking-wider">
                                            {{ formatDuration(current_game.gameDuration) }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex-auto">
                                    <div class="flex justify-center">
                                        <span class="text-gray-400 font-bold">双方比分</span>
                                    </div>
                                    <div class="flex justify-center py-1">
                                        <span class="text-sm tracking-wider">
                                            {{ current_game_detail.teams[0].totalInfo.kills }}:{{
                                                current_game_detail.teams[1].totalInfo.kills
                                            }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex-auto">
                                    <div class="flex justify-center">
                                        <span class="text-gray-400 font-bold">经济差距</span>
                                    </div>
                                    <div class="flex justify-center py-1">
                                        <span class="text-sm tracking-wider">
                                            {{
                                                Math.abs(
                                                    current_game_detail.teams[0].totalInfo
                                                        .goldEarned -
                                                        current_game_detail.teams[1].totalInfo
                                                            .goldEarned,
                                                )
                                            }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex-auto"></div>
                            </div>
                            <div class="flex">
                                <div @click="panelId = 1">
                                    <span class="tab-item" :class="{ active: panelId === 1 }"
                                        >基础</span
                                    >
                                </div>
                                <div class="ml-5" @click="panelId = 2">
                                    <span class="tab-item" :class="{ active: panelId === 2 }"
                                        >高阶数据</span
                                    >
                                </div>
                                <div class="ml-5" @click="panelId = 3">
                                    <span class="tab-item" :class="{ active: panelId === 3 }"
                                        >对位数据</span
                                    >
                                </div>
                            </div>
                        </div>
                        <div
                            v-show="panelId == 1"
                            class="w-full flex-1 flex flex-col non-scroll-bar overflow-y-auto"
                        >
                            <div
                                v-for="(team, teamIdx) in current_game.teams"
                                :key="teamIdx"
                                class="half-panel w-full bg-gradient-to-t from-white"
                                :class="
                                    team.win === 'Win'
                                        ? 'tb-win to-blue-100'
                                        : 'tb-fail to-rose-100'
                                "
                            >
                                <table>
                                    <thead class="w-full">
                                        <tr class="text-left">
                                            <th class="w-[7%]">
                                                <span class="title font-bold text-xl">
                                                    {{ team.win === 'Win' ? '胜' : '败' }}方</span
                                                >
                                            </th>
                                            <th class="w-[1.9%]"></th>
                                            <th class="w-[1.9%]"></th>
                                            <th class="w-[20%]">
                                                <div class="flex items-center">
                                                    <span class="mdi mdi-sword-cross mr-2"></span>
                                                    <div>
                                                        <span>
                                                            {{
                                                                current_game_detail.teams[teamIdx]
                                                                    .totalInfo.kills
                                                            }}:{{
                                                                current_game_detail.teams[teamIdx]
                                                                    .totalInfo.deaths
                                                            }}:{{
                                                                current_game_detail.teams[teamIdx]
                                                                    .totalInfo.assists
                                                            }}
                                                        </span>
                                                    </div>
                                                    <el-popover
                                                        v-if="
                                                            current_game.teams[teamIdx].bans
                                                                .length != 0
                                                        "
                                                        placement="top"
                                                        width="auto"
                                                        trigger="hover"
                                                    >
                                                        <template #reference>
                                                            <div
                                                                class="ml-5 cursor-pointer bg-[#464646] w-10 h-[18px] rounded-[2px] flex justify-center items-center"
                                                            >
                                                                <span
                                                                    class="text-xs text-white font-bold"
                                                                    >BAN</span
                                                                >
                                                            </div>
                                                        </template>
                                                        <div
                                                            class="flex items-center justify-evenly"
                                                        >
                                                            <championImg
                                                                v-for="ban in current_game.teams[
                                                                    teamIdx
                                                                ].bans"
                                                                width="35"
                                                                class="mx-1"
                                                                :key="ban.championId"
                                                                :championId="ban.championId"
                                                            />
                                                        </div>
                                                    </el-popover>
                                                </div>
                                            </th>
                                            <th class="w-[230px]"></th>
                                            <th>KDA</th>
                                            <th class="w-[10.54%]">金钱</th>
                                            <th class="w-[10.54%]">伤害</th>
                                            <th class="w-[10.54%]">评分</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr
                                            v-for="summonerIdx in current_game_detail.teams[teamIdx]
                                                .summonerIdx"
                                            :key="summonerIdx"
                                            :class="{
                                                me:
                                                    current_game.participantIdentities[summonerIdx]
                                                        .player.puuid == puuid,
                                            }"
                                        >
                                            <td class="flex justify-center items-center">
                                                <championImg
                                                    width="35"
                                                    :championId="
                                                        current_game.participants[summonerIdx]
                                                            .championId
                                                    "
                                                />
                                            </td>
                                            <td>
                                                <div class="h-full flex flex-col justify-evenly">
                                                    <spellImg
                                                        width="20"
                                                        :spellId="
                                                            current_game.participants[summonerIdx]
                                                                .spell1Id
                                                        "
                                                    />
                                                    <spellImg
                                                        width="20"
                                                        :spellId="
                                                            current_game.participants[summonerIdx]
                                                                .spell2Id
                                                        "
                                                    />
                                                </div>
                                            </td>
                                            <td>
                                                <div class="h-full flex flex-col justify-evenly">
                                                    <runeImg
                                                        width="20"
                                                        :runeId="
                                                            current_game.participants[summonerIdx]
                                                                .stats.perkPrimaryStyle
                                                        "
                                                    />
                                                    <runeImg
                                                        width="20"
                                                        :runeId="
                                                            current_game.participants[summonerIdx]
                                                                .stats.perkSubStyle
                                                        "
                                                    />
                                                </div>
                                            </td>
                                            <td class="px-2">
                                                <div class="flex flex-col">
                                                    <div class="text-left">
                                                        <span
                                                            class="cursor-pointer hover:underline"
                                                            @click="
                                                                jumpSummoner(
                                                                    current_game
                                                                        .participantIdentities[
                                                                        summonerIdx
                                                                    ].player.summonerId,
                                                                )
                                                            "
                                                        >
                                                            {{
                                                                current_game.participantIdentities[
                                                                    summonerIdx
                                                                ].player.summonerName
                                                            }}
                                                        </span>
                                                    </div>
                                                </div>
                                            </td>

                                            <td>
                                                <div class="flex items-center">
                                                    <itemImg
                                                        v-for="i in [0, 1, 2, 3, 4, 5, 6]"
                                                        :key="i"
                                                        class="mr-1 rounded-sm"
                                                        width="30"
                                                        :itemId="
                                                            current_game.participants[summonerIdx]
                                                                .stats['item' + i]
                                                        "
                                                    />
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <span
                                                        >{{
                                                            current_game.participants[summonerIdx]
                                                                .stats.kills
                                                        }}
                                                        /
                                                        {{
                                                            current_game.participants[summonerIdx]
                                                                .stats.deaths
                                                        }}
                                                        /
                                                        {{
                                                            current_game.participants[summonerIdx]
                                                                .stats.assists
                                                        }}</span
                                                    >
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <span>{{
                                                        current_game.participants[summonerIdx].stats
                                                            .goldEarned
                                                    }}</span>
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <span>{{
                                                        current_game.participants[summonerIdx].stats
                                                            .totalDamageDealtToChampions
                                                    }}</span>
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <span>{{
                                                        calculateKDA(
                                                            current_game.participants[summonerIdx]
                                                                .stats.kills,
                                                            current_game.participants[summonerIdx]
                                                                .stats.assists,
                                                            current_game.participants[summonerIdx]
                                                                .stats.deaths,
                                                        )
                                                    }}</span>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div v-if="panelId == 2" class="w-full flex-1 flex pt-2 overflow-y-auto">
                            <div class="h-full flex-1 pr-10">
                                <div
                                    v-for="(team, teamIdx) in current_game.teams"
                                    :key="teamIdx"
                                    class="half-panel w-full bg-gradient-to-t from-white"
                                    :class="
                                        team.win === 'Win'
                                            ? 'tb-win to-blue-100'
                                            : 'tb-fail to-rose-100'
                                    "
                                >
                                    <table>
                                        <thead>
                                            <tr>
                                                <th class="w-1/3 px-4">
                                                    <div class="text-left text-sm text-gray-700">
                                                        {{
                                                            fields.find(
                                                                (field) =>
                                                                    field.label === current_field,
                                                            ).text
                                                        }}
                                                    </div>
                                                </th>
                                                <th></th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr
                                                v-for="summonerIdx in current_game_detail.teams[
                                                    teamIdx
                                                ].summonerIdx"
                                                :key="summonerIdx"
                                            >
                                                <td>
                                                    <div class="flex item-center">
                                                        <championImg
                                                            width="35"
                                                            class="mx-3"
                                                            :championId="
                                                                current_game.participants[
                                                                    summonerIdx
                                                                ].championId
                                                            "
                                                        />
                                                        <div
                                                            class="cursor-pointer hover:underline ml-3 leading-[35px]"
                                                            @click="
                                                                jumpSummoner(
                                                                    current_game
                                                                        .participantIdentities[
                                                                        summonerIdx
                                                                    ].player.summonerId,
                                                                )
                                                            "
                                                        >
                                                            {{
                                                                current_game.participantIdentities[
                                                                    summonerIdx
                                                                ].player.summonerName
                                                            }}
                                                        </div>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="flex items-center">
                                                        <div
                                                            class="bar mr-3"
                                                            :style="{
                                                                width: calcWidth(
                                                                    summonerIdx,
                                                                    teamIdx,
                                                                ),
                                                            }"
                                                        ></div>
                                                        {{
                                                            formatNumber(
                                                                current_game.participants[
                                                                    summonerIdx
                                                                ].stats[current_field],
                                                            )
                                                        }}
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div class="h-full min-w-[200px] max-w-[200px] scroll overflow-y-auto">
                                <el-radio-group v-model="current_field" class="w-full">
                                    <el-radio
                                        v-for="(field, idx) in fields"
                                        :key="idx"
                                        :label="field.label"
                                        class="w-full"
                                        >{{ field.text }}</el-radio
                                    >
                                </el-radio-group>
                            </div>
                        </div>
                        <div v-if="panelId == 3" class="w-full flex-1 flex flex-col">
                            <template v-if="teamNumber === 2">
                                <div class="pt-3 w-full">
                                    <div class="relative overflow-hidden">
                                        <div class="w-full h-9 flex">
                                            <div
                                                class="w-1/2 h-full px-4"
                                                :style="{
                                                    backgroundColor:
                                                        current_game.teams[0].win == 'Win'
                                                            ? '#44b7c6'
                                                            : '#da5f5f',
                                                }"
                                            >
                                                <span class="leading-9 text-white font-bold">
                                                    {{
                                                        current_game.teams[0].win == 'Win'
                                                            ? '胜'
                                                            : '败'
                                                    }}方
                                                </span>
                                            </div>
                                            <div
                                                class="w-1/2 h-full px-4 leading-9 text-right"
                                                :style="{
                                                    backgroundColor:
                                                        current_game.teams[1].win == 'Win'
                                                            ? '#44b7c6'
                                                            : '#da5f5f',
                                                }"
                                            >
                                                <span class="leading-9 text-white font-bold">
                                                    {{
                                                        current_game.teams[1].win == 'Win'
                                                            ? '胜'
                                                            : '败'
                                                    }}方
                                                </span>
                                            </div>
                                        </div>
                                        <div class="w-full h-[270px] flex">
                                            <div
                                                class="h-full w-1/2 bg-cover bg-center"
                                                :style="{
                                                    backgroundImage: championBg(
                                                        selected_team0_summonerIdx,
                                                    ),
                                                }"
                                            ></div>
                                            <div
                                                class="h-full w-1/2 bg-cover bg-center"
                                                :style="{
                                                    backgroundImage: championBg(
                                                        selected_team1_summonerIdx,
                                                    ),
                                                }"
                                            ></div>
                                        </div>
                                        <div class="absolute bottom-0 w-full h-9 leading-9 flex">
                                            <div
                                                class="h-full w-1/2 bg-opacity-40 bg-gray-700 flex items-center"
                                            >
                                                <el-popover
                                                    placement="top"
                                                    :width="
                                                        current_game_detail.teams[0].summonerIdx
                                                            .length * 65
                                                    "
                                                    trigger="click"
                                                >
                                                    <template #reference>
                                                        <div class="h-full">
                                                            <span
                                                                class="mdi mdi-swap-horizontal text-white text-xl mx-4 cursor-pointer"
                                                            ></span>
                                                        </div>
                                                    </template>
                                                    <div class="flex items-center justify-evenly">
                                                        <championImg
                                                            v-for="idx in current_game_detail
                                                                .teams[0].summonerIdx"
                                                            :key="idx"
                                                            :championId="
                                                                current_game.participants[idx]
                                                                    .championId
                                                            "
                                                            width="55"
                                                            class="mx-1 cursor-pointer"
                                                            @click="
                                                                selected_team0_summonerIdx = idx
                                                            "
                                                        />
                                                    </div>
                                                </el-popover>
                                                <span class="text-white">
                                                    {{
                                                        current_game.participantIdentities[
                                                            selected_team0_summonerIdx
                                                        ].player.summonerName
                                                    }}
                                                </span>
                                            </div>
                                            <div
                                                class="h-full w-1/2 bg-opacity-40 bg-gray-700 flex justify-end items-center"
                                            >
                                                <span class="text-white">
                                                    {{
                                                        current_game.participantIdentities[
                                                            selected_team1_summonerIdx
                                                        ].player.summonerName
                                                    }}
                                                </span>
                                                <el-popover
                                                    placement="top"
                                                    :width="
                                                        current_game_detail.teams[1].summonerIdx
                                                            .length * 65
                                                    "
                                                    trigger="click"
                                                >
                                                    <template #reference>
                                                        <div class="h-full">
                                                            <span
                                                                class="mdi mdi-swap-horizontal text-white text-xl mx-4 cursor-pointer"
                                                            ></span>
                                                        </div>
                                                    </template>
                                                    <div class="flex items-center justify-evenly">
                                                        <championImg
                                                            v-for="idx in current_game_detail
                                                                .teams[1].summonerIdx"
                                                            :key="idx"
                                                            :championId="
                                                                current_game.participants[idx]
                                                                    .championId
                                                            "
                                                            width="55"
                                                            class="mx-1 cursor-pointer"
                                                            @click="
                                                                selected_team1_summonerIdx = idx
                                                            "
                                                        />
                                                    </div>
                                                </el-popover>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="w-full flex-1 flex">
                                    <div class="h-full w-[43%] flex flex-col justify-end">
                                        <div
                                            v-for="(compare, idx) in compares"
                                            :key="idx"
                                            class="w-full h-1/6 max-h-12 flex justify-end items-center"
                                        >
                                            <span class="mx-3">
                                                {{
                                                    formatNumber(
                                                        current_game_detail.summoners.each[
                                                            selected_team0_summonerIdx
                                                        ][compare.label],
                                                    )
                                                }}</span
                                            >
                                            <div class="relative h-5 w-5/6 bg-[#d6d6d6] text-right">
                                                <div
                                                    class="absolute right-0 h-full w-1/2"
                                                    :style="{
                                                        backgroundColor:
                                                            current_game.teams[0].win === 'Win'
                                                                ? '#48b7c8'
                                                                : '#dc6a6a',
                                                        width: `${
                                                            (current_game_detail.summoners.each[
                                                                selected_team0_summonerIdx
                                                            ][compare.label] /
                                                                current_game_detail.summoners.max[
                                                                    compare.label
                                                                ]) *
                                                            100
                                                        }%`,
                                                    }"
                                                ></div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="h-full w-[14%] flex flex-col justify-end">
                                        <div
                                            v-for="(compare, idx) in compares"
                                            :key="idx"
                                            class="h-1/6 max-h-12 flex justify-center items-center"
                                        >
                                            <span class="text-sm">{{ compare.text }}</span>
                                        </div>
                                    </div>
                                    <div class="h-full w-[43%] flex flex-col justify-end">
                                        <div
                                            v-for="(compare, idx) in compares"
                                            :key="idx"
                                            class="w-full h-1/6 max-h-12 flex justify-start items-center"
                                        >
                                            <div class="relative h-5 w-5/6 bg-[#d6d6d6] text-right">
                                                <div
                                                    class="absolute left-0 h-full w-1/2"
                                                    :style="{
                                                        backgroundColor:
                                                            current_game.teams[1].win === 'Win'
                                                                ? '#48b7c8'
                                                                : '#dc6a6a',
                                                        width: `${
                                                            (current_game_detail.summoners.each[
                                                                selected_team1_summonerIdx
                                                            ][compare.label] /
                                                                current_game_detail.summoners.max[
                                                                    compare.label
                                                                ]) *
                                                            100
                                                        }%`,
                                                    }"
                                                ></div>
                                            </div>
                                            <span class="mx-3">
                                                {{
                                                    formatNumber(
                                                        current_game_detail.summoners.each[
                                                            selected_team1_summonerIdx
                                                        ][compare.label],
                                                    )
                                                }}</span
                                            >
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </template>
                    <template v-else-if="onloading">
                        <div class="w-full h-full flex justify-center items-center">
                            <bullfrog></bullfrog>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, watch, nextTick } from 'vue'
import { bullfrog } from '@/components/loaders'
import { useRoute, useRouter } from 'vue-router'
import { formatMMDD, formatHHMM, formatDuration, calculateKDA, formatNumber } from '@/utils/common'
import axios from 'axios'
import webConfig from '@/global.config'
import { championImg, spellImg, runeImg, itemImg, profileImg } from '@/components/icons'
// route
const route = useRoute()
const router = useRouter()
// refs
const fields = [
    { type: 'radio', text: '对英雄的总伤害', label: 'totalDamageDealtToChampions' },
    { type: 'radio', text: '对英雄的物理伤害', label: 'physicalDamageDealtToChampions' },
    { type: 'radio', text: '对英雄的魔法伤害', label: 'magicDamageDealtToChampions' },
    { type: 'radio', text: '对英雄的真实伤害', label: 'trueDamageDealtToChampions' },
    { type: 'radio', text: '总造成物理伤害', label: 'physicalDamageDealt' },
    { type: 'radio', text: '总造成魔法伤害', label: 'magicDamageDealt' },
    { type: 'radio', text: '输出治疗效果', label: 'totalHeal' },
    { type: 'radio', text: '承受伤害', label: 'totalDamageTaken' },
    { type: 'radio', text: '承受物理伤害', label: 'physicalDamageTaken' },
    { type: 'radio', text: '承受魔法伤害', label: 'magicalDamageTaken' },
    { type: 'radio', text: '承受的真实伤害', label: 'trueDamageTaken' },
    { type: 'radio', text: '花费金钱', label: 'goldSpent' },
    { type: 'radio', text: '获得金钱', label: 'goldEarned' },
    { type: 'radio', text: '视野得分', label: 'visionScore' },
    { type: 'radio', text: '放置守卫', label: 'wardsPlaced' },
    { type: 'radio', text: '摧毁守卫', label: 'wardsKilled' },
    { type: 'radio', text: '购买控制守卫', label: 'sightWardsBoughtInGame' },
    { type: 'radio', text: '击杀小兵', label: 'totalMinionsKilled' },
]
const compares = [
    { label: 'Kda', text: 'KDA' },
    { label: 'DamageMinDealt', text: '分均伤害' },
    { label: 'DamageMinTaken', text: '分均承伤' },
    { label: 'DamageConversion', text: '伤害转换' },
    { label: 'GoldMinEarned', text: '分均经济' },
    { label: 'Survivbility', text: '生存能力' },
]
const selected_team0_summonerIdx = ref(0)
const selected_team1_summonerIdx = ref(0)
const limit = 7
const container = ref()
const puuid = ref()
const summoner = ref()
const games = ref()
const onloading = ref(false)
const current_game = ref()
const current_game_detail = ref()
const page = ref(1)
const teamNumber = ref(0)
const panelId = ref()
const current_field = ref()
// functions
const itemStyle = (gameId) => {
    if (current_game.value === null || gameId !== current_game.value.gameId) return ''
    else {
        if (current_game.value.teams[0].win === 'Win')
            return {
                background: 'linear-gradient(to right, #c5d6ec, #fff)',
            }
        else
            return {
                background: 'linear-gradient(to right, #f5e5e6, #fff)',
            }
    }
}
const championBg = (summonerIdx) => {
    return `url(https://game.gtimg.cn/images/lol/act/img/skin/big${current_game.value.participants[summonerIdx].championId}000.jpg)`
}
const pageDown = async () => {
    page.value = Math.max(page.value - 1, 1)
    await getMatches()
}
const pageUp = async () => {
    if (games.value.length !== limit) return
    page.value++
    await getMatches()
}
const getSummonerInfo = async () => {
    const res = await axios.get(`${webConfig.baseUrl}/summoner-bypuuid/${puuid.value}`)
    summoner.value = res.data
}
const getMatches = async () => {
    const beginIdx = limit * (page.value - 1)
    const endIdx = beginIdx + limit - 1
    const res = await axios.get(
        `${webConfig.baseUrl}/get_rank_list/${puuid.value}?beginIdx=${beginIdx}&endIdx=${endIdx}`,
    )
    if (res.data.httpStatus === 400) {
        games.value = []
        return console.log(res.data.message)
    } else games.value = res.data.games.games
}
const onSelectGame = async (gameId) => {
    // onloading.value = true
    console.log('start')
    const res = await axios.get(`${webConfig.baseUrl}/match-detail/${gameId}`)
    panelId.value = 1
    current_game.value = res.data[0]
    teamNumber.value = res.data[0].teams.length
    current_game_detail.value = res.data[1]
    if (teamNumber.value == 2) {
        selected_team1_summonerIdx.value = res.data[1].teams[1].summonerIdx[0]
    }
    console.log('over')
    // nextTick(() => {
    //     onloading.value = false
    // })
}
const jumpSummoner = (summonerId) => {
    router.push('/account/' + summonerId)
}
const calcWidth = (summonerIdx, teamIdx) => {
    const me = current_game.value.participants[summonerIdx].stats[current_field.value]
    const max = current_game_detail.value.teams[teamIdx].maxInfo[current_field.value]
    return `${(80 * me) / max}%`
}
watch(
    () => route.params.puuid,
    async (toPuuid, prevPuuid) => {
        current_field.value = 'totalDamageDealtToChampions'
        games.value = []
        current_game.value = current_game_detail.value = null
        page.value = panelId.value = 1
        puuid.value = toPuuid
        await getSummonerInfo()
        await getMatches()
        if (games.value.length != 0) {
            await onSelectGame(games.value[0].gameId)
        }
    },
    { immediate: true, deep: true },
)
</script>
<style lang="scss" scoped>
* {
    user-select: none;
}
.radar {
    background-color: #f2f5f8;
    box-shadow: 0 0 60px 30px #f2f5f8, 0 0 60px 20px #f2f5f8, 0 0 60px 20px #f2f5f8,
        0 0 80px 10px #f2f5f8;
}
.bar {
    height: 20px;
}
.cp-height {
    height: calc(100% - 80px);
}
.tab-item {
    position: relative;
    white-space: nowrap;
    cursor: pointer;
    &:hover {
        color: #f5d2d5;
        color: #58b0a1;
    }
    &.active {
        color: #4daa9a;
        font-weight: 700;
        &::after {
            position: absolute;
            content: '';
            bottom: -5px;
            left: 50%;
            height: 2px;
            width: 100%;
            transform: translateX(-50%);
            background-color: #4daa9a;
        }
    }
}

.item {
    position: relative;
    // transition: background 0.05s ease-in-out;
    &:hover {
        background: rgb(102, 102, 102, 0.1);
    }
    &:not(:last-child)::after {
        position: absolute;
        content: '';
        left: 50%;
        bottom: 0;
        height: 1px;
        width: 70%;
        background-color: rgba(0, 0, 0, 0.1);
        transform: translateX(-50%);
    }
}
.half-panel {
    height: calc(50vh - 95px);
    table {
        width: 100%;
        thead {
            height: 40px;
            th {
                font-size: 15px;
                text-align: center;
            }
        }
        tbody {
            tr,
            td {
                height: 55px;
                text-align: center;
            }
            tr td:first-child,
            tr td:last-child {
                padding: 0 10px;
            }
        }
    }
    &.tb-win {
        .bar {
            background-color: #45c4d6;
        }
        .title {
            color: #48b7c8;
        }
        tbody tr {
            &.me,
            &:hover {
                background-color: #d0e0f5;
            }
        }
    }
    &.tb-fail {
        .bar {
            background-color: #d95a5a;
        }
        .title {
            color: #dc6a6a;
        }
        tbody tr {
            &.me,
            &:hover {
                background-color: #f7dcdc;
            }
        }
    }
}

.scroll-bar {
    /* 修改滚动条的样式 */
    &::-webkit-scrollbar {
        width: 5px; /* 滚动条宽度 */
    }

    /* 滚动条轨道 */
    &::-webkit-scrollbar-track {
        background-color: transparent; /* 轨道颜色 */
    }

    /* 滚动条滑块 */
    &::-webkit-scrollbar-thumb {
        background-color: #c1c1c1; /* 滑块颜色 */
        border-radius: 5px; /* 滑块圆角 */
    }
}

.non-scroll-bar {
    /* 修改滚动条的样式 */
    &::-webkit-scrollbar {
        width: 0px; /* 滚动条宽度 */
    }

    /* 滚动条轨道 */
    &::-webkit-scrollbar-track {
        background-color: transparent; /* 轨道颜色 */
    }

    /* 滚动条滑块 */
    &::-webkit-scrollbar-thumb {
        width: 0;
    }
}
</style>
