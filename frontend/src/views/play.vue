<template>
    <div class="p-8 w-full h-full overflow-hidden flex justify-center items-center">
        <div class="w-full h-full rounded-lg shadow flex justify-center items-center">
            <div v-if="game == null" class="select-none">
                <div class="text-center text-[#262626] italic text-4xl font-bold">
                    暂未获取到对局信息
                </div>
                <div class="text-[#6b7280] text-xl font-bold py-2 tracking-wide">
                    面板信息将在状态为选择英雄时以及游戏加载中获取
                </div>
            </div>
            <div v-else class="p-8 w-full h-full overflow-y-auto">
                <div
                    v-for="(team, idx) in game.teams"
                    :key="idx"
                    class="w-full h-1/2 flex min-h-[360px]"
                >
                    <div
                        v-for="(summoner, idx2) in team"
                        :key="idx2"
                        class="h-full w-[20%] outline outline-1 outline-gray-400 p-3"
                    >
                        <div class="flex flex-col items-center">
                            <profileImg width="40" :profileIconId="summoner.profileIconId" />
                            <div class="py-1">
                                <span class="text-sm font-bold text-gray-500 cursor-pointer">
                                    {{ summoner.summonerName }}
                                </span>
                            </div>
                        </div>
                        <template v-if="summoner.summonerId !== 0">
                            <div class="flex justify-between items-center">
                                <div>
                                    <span class="text-[15px] font-bold text-gray-700">
                                        单双:
                                        {{
                                            webConfig.rank[
                                                summoner.rank.queueMap['RANKED_SOLO_5x5'].tier ||
                                                    'NA'
                                            ]
                                        }}
                                    </span>
                                </div>
                                <div>
                                    <span class="text-[15px] font-bold text-gray-700">
                                        灵活:
                                        {{
                                            webConfig.rank[
                                                summoner.rank.queueMap['RANKED_FLEX_SR'].tier ||
                                                    'NA'
                                            ]
                                        }}
                                    </span>
                                </div>
                            </div>
                            <div class="flex py-1 justify-between items-center">
                                <div>
                                    <div>
                                        <span class="text-[#d97706] font-bold text-sm">
                                            胜率: {{ (summoner.match.rate * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                    <div>
                                        <span class="text-[#d97706] font-bold text-sm">
                                            KDA: {{ summoner.match.kda.toFixed(2) }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex">
                                    <positionImg
                                        v-if="summoner.position !== 'UNKNOW'"
                                        width="30"
                                        :position="summoner.position"
                                    />
                                    <championImg
                                        v-for="championId in summoner.champions"
                                        :key="championId"
                                        class="ml-1"
                                        width="30"
                                        :championId="championId"
                                    />
                                </div>
                            </div>
                            <div class="h-[55%] overflow-y-auto non-scrollbar">
                                <template v-if="summoner.match.games">
                                    <div
                                        v-for="game in summoner.match.games"
                                        :key="game.gameId"
                                        class="flex justify-between items-center mb-1"
                                    >
                                        <div class="flex">
                                            <championImg
                                                width="25"
                                                :championId="game.participants[0].championId"
                                            />
                                            <div class="flex items-center pl-1">
                                                <span class="font-bold text-sm">
                                                    {{ webConfig.queue[game.queueId] }}
                                                </span>
                                            </div>
                                        </div>
                                        <div class="h-full flex items-center">
                                            <span class="text-[#10b981] font-bold text-sm">
                                                {{ game.participants[0].stats.kills }}/{{
                                                    game.participants[0].stats.deaths
                                                }}/{{ game.participants[0].stats.assists }}
                                            </span>
                                        </div>
                                        <div class="h-full flex items-center">
                                            <span class="font-bold text-sm">
                                                {{ formatMMDD(game.gameCreationDate) }}
                                            </span>
                                        </div>
                                    </div>
                                </template>
                                <template v-else>
                                    <div>
                                        <span class="font-bold text-sm">暂无匹配排位对局</span>
                                    </div>
                                </template>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, watch } from 'vue'
import { profileImg, championImg, positionImg } from '@/components/icons'
import { useGlobalStore } from '@/stores'
import webConfig from '@/global.config'
import { formatMMDD } from '@/utils/common'
// pinia
const useGlobal = useGlobalStore()
// ref
const game = ref(null)
watch(
    () => useGlobal.current_game,
    (toParams, previousParams) => {
        game.value = toParams
    },
    { deep: true, immediate: true },
)
</script>
<style lang="scss" scoped>
* {
    user-select: none;
}
img {
    border-radius: 5px;
}
</style>
