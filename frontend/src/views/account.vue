<template>
    <div class="px-4 py-2 w-full h-full overflow-y-auto non-scrollbar">
        <div class="relative flex flex-wrap z-10">
            <div
                :style="{ 'background-image': 'url(' + bgUrl + ')' }"
                class="main-info p-10 flex flex-col justify-end w-full h-[420px] overflow-hidden text-white bg-white rounded-lg select-none"
            >
                <div class="bottom z-10 flex">
                    <div class="summonerInfo flex items-center flex-1">
                        <div v-if="summoner" class="summonerAvatar mr-4">
                            <profileImg width="105" :profileIconId="summoner.profileIconId" />
                        </div>
                        <div class="summonerText flex flex-col">
                            <div class="summonerName">
                                <span v-if="summoner" class="text-3xl font-bold">{{
                                    summoner.displayName
                                }}</span>
                                <span
                                    class="rotate mdi mdi-paperclip ml-3 text-2xl text-gray-300 cursor-pointer"
                                    @click="copyText(summoner.displayName)"
                                ></span>
                            </div>
                            <div class="summonerArea mt-2">
                                <span class="text-sm text-[#bfbfc5] mr-3">当前生涯状态</span>
                                <span
                                    v-if="summoner"
                                    class="inline-flex items-center h-5 px-[7px] text-xs rounded-[4px] text-[#f56c6c] bg-[#fef0f0]"
                                    >{{ webConfig.privacy[summoner.privacy] }}</span
                                >
                            </div>
                            <div class="environment mt-3">
                                <div class="glass inline-flex text-xs tracking-wide p-2 rounded-lg">
                                    <span
                                        class="mdi mdi-message-processing-outline text-blue-400 mr-3"
                                    ></span>
                                    {{ webConfig.environment[env] }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mask rounded-lg"></div>
            </div>
        </div>
        <div class="relative flex flex-wrap mt-3">
            <div class="col-3 px-1">
                <div class="h-[250px] card rounded-lg px-5 py-3">
                    <div v-if="recent20summary" class="h-full flex-1 flex flex-col justify-between">
                        <div class="card-title text-xl">Summoner Summary</div>
                        <div class="content flex flex-1 w-full">
                            <div class="flex flex-col flex-1">
                                <div class="text-gray-500 text-lg my-5">
                                    <span>{{ recent20summary.total }}</span
                                    >G <span>{{ recent20summary.win }}</span
                                    >胜 <span>{{ recent20summary.lose }}</span
                                    >负
                                </div>
                                <div class="flex items-center">
                                    <div class="detail ml-4 font-bold">
                                        <div class="kda">
                                            <span>{{
                                                (
                                                    recent20summary.kill / recent20summary.total
                                                ).toFixed(2)
                                            }}</span>
                                            /
                                            <span class="text-[#d93d53] font-bold">{{
                                                (
                                                    recent20summary.death / recent20summary.total
                                                ).toFixed(2)
                                            }}</span>
                                            /
                                            <span>{{
                                                (
                                                    recent20summary.assist / recent20summary.total
                                                ).toFixed(2)
                                            }}</span>
                                        </div>
                                        <div
                                            class="text-3xl tracking-wider my-2 font-bold text-center"
                                        >
                                            {{ recent20summary.kda.toFixed(2) }} : 1
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="flex flex-col flex-1">
                                <div class="text-gray-500 text-lg my-5 text-center">
                                    Recent 20 Games
                                </div>
                                <div v-if="date20">
                                    <ul class="flex justify-evenly">
                                        <li>
                                            <div class="flex items-end w-4 h-16 bg-gray-300">
                                                <div
                                                    class="w-4 h-6 bg-blue-500"
                                                    :style="{ height: `${date20.lane.TOP * 5}%` }"
                                                ></div>
                                            </div>
                                            <div class="mt-4">
                                                <positionImg width="16" position="top" />
                                            </div>
                                        </li>
                                        <li>
                                            <div class="flex items-end w-4 h-16 bg-gray-300">
                                                <div
                                                    class="w-4 h-6 bg-blue-500"
                                                    :style="{
                                                        height: `${date20.lane.JUGGLE * 5}%`,
                                                    }"
                                                ></div>
                                            </div>
                                            <div class="mt-4">
                                                <positionImg width="16" position="jungle" />
                                            </div>
                                        </li>
                                        <li>
                                            <div class="flex items-end w-4 h-16 bg-gray-300">
                                                <div
                                                    class="w-4 h-6 bg-blue-500"
                                                    :style="{
                                                        height: `${date20.lane.MIDDLE * 5}%`,
                                                    }"
                                                ></div>
                                            </div>
                                            <div class="mt-4">
                                                <positionImg width="16" position="middle" />
                                            </div>
                                        </li>
                                        <li>
                                            <div class="flex items-end w-4 h-16 bg-gray-300">
                                                <div
                                                    class="w-4 h-6 bg-blue-500"
                                                    :style="{ height: `${date20.lane.ADC * 5}%` }"
                                                ></div>
                                            </div>
                                            <div class="mt-4">
                                                <positionImg width="16" position="bottom" />
                                            </div>
                                        </li>
                                        <li>
                                            <div class="flex items-end w-4 h-16 bg-gray-300">
                                                <div
                                                    class="w-4 h-6 bg-blue-500"
                                                    :style="{
                                                        height: `${date20.lane.SUPPORT * 5}%`,
                                                    }"
                                                ></div>
                                            </div>
                                            <div class="mt-4">
                                                <positionImg width="16" position="utility" />
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-3 px-1">
                <div class="h-[250px] card rounded-lg px-5 py-3">
                    <div class="card-title text-xl">Season's Most Played Champions</div>
                    <div
                        v-if="recent20detail"
                        class="content flex justify-center items-center w-full mt-8"
                    >
                        <div class="flex justify-between items-center">
                            <div
                                v-for="(item, idx) in [
                                    recent20detail[1],
                                    recent20detail[0],
                                    recent20detail[2],
                                ]"
                                class="flex flex-col items-center"
                            >
                                <div class="mx-5">
                                    <championImg
                                        :width="idx === 1 ? 100 : 75"
                                        :championId="item[0]"
                                    />
                                </div>
                                <div class="font-bold text-center">
                                    <div>
                                        <span>{{ item[1].win }}</span
                                        >W <span>{{ item[1].lose }}</span
                                        >L
                                    </div>
                                    <div>
                                        <span>{{ item[1].kda.toFixed(2) }}</span>
                                        <span class="ml-1 text-sm text-gray-600">KDA</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-3 px-1">
                <div class="h-[250px] card rounded-lg px-5 py-3 flex flex-col">
                    <div class="card-title text-xl">Match Analysis</div>
                    <div
                        class="content flex-1 flex flex-col justify-center items-center w-full pt-3"
                    >
                        <div class="h-full w-full" ref="chartRef"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex flex-wrap mt-3">
            <div class="col-4 px-1">
                <div v-if="recent20summary" class="card rounded-lg px-5 py-3 flex flex-col">
                    <div class="rank-title text-xl flex items-center justify-between">
                        单双排
                        <span v-show="!rank['RANKED_SOLO_5x5'].tier" class="text-gray-400 font-bold"
                            >Unranked</span
                        >
                    </div>
                    <div
                        v-if="rank['RANKED_SOLO_5x5'].tier"
                        class="rank-solo-detail flex items-center justify-between"
                    >
                        <div class="flex justify-evenly items-center">
                            <div class="rank-icon w-16 h-16 flex items-center mr-3">
                                <perkImg :tier="rank['RANKED_SOLO_5x5'].tier" />
                            </div>
                            <div class="rank-level">
                                <div class="text-xl">
                                    {{ rank['RANKED_SOLO_5x5'].tier }}
                                </div>
                                <div class="text-gray-300">
                                    {{ rank['RANKED_SOLO_5x5'].division }}
                                </div>
                            </div>
                        </div>
                        <div class="text-gray-400 font-bold pr-3 text-right">
                            <div>
                                {{ rank['RANKED_SOLO_5x5'].win }}W
                                {{ rank['RANKED_SOLO_5x5'].loss }}L
                            </div>
                            <div>{{ (rank['RANKED_SOLO_5x5'].rate * 100).toFixed(2) }}%</div>
                        </div>
                    </div>
                </div>
                <div v-if="recent20summary" class="card rounded-lg px-5 py-3 flex flex-col my-3">
                    <div class="rank-title text-xl flex items-center justify-between">
                        灵活组排
                        <span v-show="!rank['RANKED_FLEX_SR'].tier" class="text-gray-400 font-bold">
                            Unranked
                        </span>
                    </div>
                    <div
                        v-if="rank['RANKED_FLEX_SR'].tier"
                        class="rank-solo-detail flex items-center justify-between"
                    >
                        <div class="flex justify-evenly items-center">
                            <div class="rank-icon w-16 h-16 flex items-center mr-3">
                                <perkImg :tier="rank['RANKED_FLEX_SR'].tier" />
                            </div>
                            <div class="rank-level">
                                <div class="text-xl">
                                    {{ rank['RANKED_FLEX_SR'].tier }}
                                </div>
                                <div class="text-gray-300">
                                    {{ rank['RANKED_FLEX_SR'].division }}
                                </div>
                            </div>
                        </div>
                        <div class="text-gray-400 font-bold pr-3 text-right">
                            <div>
                                {{ rank['RANKED_FLEX_SR'].win }}W {{ rank['RANKED_FLEX_SR'].loss }}L
                            </div>
                            <div>{{ rank['RANKED_FLEX_SR'].rate.toFixed(2) }}%</div>
                        </div>
                    </div>
                </div>
                <div class="card rounded-lg px-5 py-3">
                    <div class="card-title text-xl mb-4">Nearly 20 game matches</div>
                    <div class="match-list">
                        <div
                            v-for="(item, idx) in recent20detail"
                            :key="idx"
                            class="match-item flex justify-between items-center mb-5"
                        >
                            <div class="flex items-center">
                                <div class="mr-3">
                                    <championImg width="45" :championId="item[0]" />
                                </div>
                                <div>
                                    <div>{{ webConfig.champions[item[0]].label }}</div>
                                    <div>
                                        <span class="text-red-700"
                                            >{{ (item[1].rate * 100).toFixed(2) }}%</span
                                        >
                                        <span class="ml-3 text-gray-600"
                                            >{{ item[1].win }}W {{ item[1].lose }}L</span
                                        >
                                    </div>
                                </div>
                            </div>
                            <div>
                                <div class="kda">
                                    {{ item[1].kda.toFixed(2) }}:1
                                    <span class="text-sm text-gray-600">KDA</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex-1 pl-4">
                <div
                    class="appear card rounded-lg mb-3 text-left py-2 px-5 cursor-pointer"
                    @click="jumpMatch"
                >
                    <span class="line relative text-2xl text-gray-500"> 历史战绩 </span>
                    <span class="mdi mdi-chevron-right"></span>
                </div>
                <div v-if="recent20summary">
                    <template v-if="onloading">
                        <div class="h-[200px] card rounded-lg mb-3 overflow-hidden">
                            <div class="h-full w-full flex justify-center items-center">
                                <bullfrog></bullfrog>
                            </div>
                        </div>
                    </template>
                    <template v-else>
                        <div
                            v-for="(gameId, idx) in recent20summary.gameIds.slice(0, 6)"
                            :key="idx"
                            class="h-[200px] card rounded-lg mb-3 overflow-hidden"
                        >
                            <conciseRecord
                                :gameId="gameId"
                                :summonerId="summoner.summonerId"
                            ></conciseRecord>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { useRouter, useRoute } from 'vue-router'
import { ref, computed, watch, nextTick } from 'vue'
import { copyText, scrollTop } from '@/utils/common'
import { useGlobalStore } from '@/stores'
import conciseRecord from '@/components/conciseRecord.vue'
import { perkImg, profileImg, championImg, positionImg } from '@/components/icons'
import { bullfrog } from '@/components/loaders'
import * as echarts from 'echarts'
import axios from 'axios'
import webConfig from '@/global.config'
// router
const route = useRoute()
const router = useRouter()
// pinia
const useGlobal = useGlobalStore()
// refs
const onloading = ref()
const skinId = ref()
const summoner = ref()
const rank = ref()
const env = ref()
const bg = ref()
const chartRef = ref()
const date20 = ref()
const recent20detail = ref()
const recent20summary = ref()
// computed
const bgUrl = computed(() => {
    if (!skinId.value) {
        return ''
    } else return `https://game.gtimg.cn/images/lol/act/img/skin/big${skinId.value}.jpg`
})
// functions
const getEnvironmentInfo = async () => {
    const res = await axios.get(`${webConfig.baseUrl}/environment`)
    env.value = res.data
}
const getSummonerProfileInfo = async (puuid) => {
    const res = await axios.get(`${webConfig.baseUrl}/summoner-profile/${puuid}`)
    if ('backgroundSkinId' in res.data) {
        skinId.value = res.data.backgroundSkinId
    }
}
const getSummonerInfo = async (summonerId) => {
    const res = await axios.get(`${webConfig.baseUrl}/summoner/${summonerId}`)
    summoner.value = res.data
}
const init_echart = () => {
    var damageChart = echarts.init(chartRef.value)
    // 指定图表的配置项和数据
    var option = {
        tooltip: {
            trigger: 'axis',
        },
        grid: {
            top: '10%',
            left: '3%',
            right: '3%',
            bottom: '10%',
            containLabel: true,
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
        },
        yAxis: {
            type: 'value',
        },
        series: [
            {
                name: 'Damage Healt',
                type: 'line',
                stack: 'Total',
                data: date20.value['totalDamageDealt'],
            },
            {
                name: 'Damage Taken',
                type: 'line',
                stack: 'Total',
                data: date20.value['totalDamageTaken'],
            },
        ],
    }
    // 使用刚指定的配置项和数据显示图表。
    damageChart.setOption(option)
    window.addEventListener('resize', () => {
        damageChart.resize()
    })
}
const getRecentInfo = async (puuid) => {
    const res = await axios.get(`${webConfig.baseUrl}/recent-20/${puuid}`)
    recent20detail.value = Object.entries(res.data[0]).sort(
        (a, b) => b[1].win + b[1].lose - a[1].win - a[1].lose,
    )
    recent20summary.value = res.data[1]
    date20.value = res.data[2]
}
const getRankInfo = async (puuid) => {
    const res = await axios.get(`${webConfig.baseUrl}/rank-status/${puuid}`)
    rank.value = res.data
}
const jumpMatch = () => {
    router.push('/match/' + summoner.value.puuid)
}
watch(
    () => route.params.summonerId,
    async (toParams, previousParams) => {
        if (route.name !== 'account') return
        summoner.value =
            rank.value =
            bg.value =
            date20.value =
            recent20detail.value =
            recent20summary.value =
                null
        onloading.value = true
        if (!toParams) {
            summoner.value = await useGlobal.getSummonerInfo()
        } else {
            await getSummonerInfo(toParams)
        }

        const puuid = summoner.value.puuid
        await getSummonerProfileInfo(puuid)
        await getEnvironmentInfo(puuid)
        await getRankInfo(puuid)
        await getRecentInfo(puuid)
        init_echart()
        nextTick(() => {
            onloading.value = false
            scrollTop()
        })
    },
    { immediate: true, deep: true },
)
</script>
<style lang="scss" scoped>
.appear {
    .mdi {
        transition: opacity 0.2s ease-in-out;
        opacity: 0;
    }
    .line::after {
        position: absolute;
        content: '';
        bottom: -1px;
        left: 50%;
        height: 1px;
        width: 100%;
        transform: translateX(-50%);
        background-color: #666;
        transition: opacity 0.2s ease-in-out;
        opacity: 0;
    }
    &:hover {
        .line::after,
        .mdi {
            opacity: 1;
        }
    }
}
img {
    border-radius: 7px;
}
@media (min-width: 1080px) {
    .col-2 {
        flex: 0 0 50%;
        max-width: 50%;
    }
    .col-3 {
        flex: 0 0 33.333%;
        max-width: 33.333%;
    }
    .col-4 {
        flex: 0 0 25%;
        max-width: 25%;
    }
}
@media (max-width: 1080px) {
    .col-2 {
        flex: 0 0 100%;
        max-width: 100%;
    }
    .bottom {
        flex-direction: column;
    }
}

@media (max-width: 1280px) {
    .col-3 {
        flex: 0 0 100%;
        max-width: 100%;
        margin-bottom: 10px;
    }
}
.mask {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    // backdrop-filter: blur(0.7px) brightness(1);
    background-color: rgba(0, 0, 0, 0.29);
}

.card {
    position: relative;
    z-index: 10;
    background-color: #fff;
    box-shadow: 0 2px 10px -1px #55555514, 0 1px 10px #5555550f, 0 1px 30px #55555508;
}
.main-info {
    background-size: cover;
    background-repeat: no-repeat;

    .split {
        &::after,
        &::before {
            position: absolute;
            top: 50%;
            content: '';
            width: 1px;
            height: 80%;
            transform: translate(-50%, -50%);
            background-color: rgb(0, 0, 0, 0.5);
        }
        &::before {
            left: -10px;
        }
        &::after {
            right: -10px;
        }
    }

    .glass {
        background-color: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px) brightness(0.5);
    }

    .summonerAvatar img {
        border-radius: 30px;
    }
    .rotate {
        &::before {
            transform: rotate(45deg);
        }
    }
}
.lane {
    margin: 5px 0;
    .score {
        margin: 0 10px;
    }
    .champions {
        img {
            margin: 0 2px;
        }
    }
}

.circle {
    width: 80px;
    height: 80px;
    position: relative;
    border-radius: 50%;
    box-shadow: inset 0 0 0 8px #e84057;

    .ab {
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        margin: auto;
    }

    &_left {
        border: 8px solid #e84057;
        border-radius: 50%;
        clip: rect(0, 40px, 80px, 0);
    }

    &_right {
        border: 8px solid #e84057;
        border-radius: 50%;
        clip: rect(0, 80px, 80px, 40px);
    }

    &_text {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        .name {
            margin-bottom: 4px;
        }
    }
}
</style>
