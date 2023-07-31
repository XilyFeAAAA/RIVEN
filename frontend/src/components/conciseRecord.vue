<template>
    <div
        v-if="me"
        :style="{
            borderColor: me.stats.win ? '#5383e8' : '#e84057',
            backgroundColor: me.stats.win ? '#ecf2ff' : '#fff1f3',
        }"
        class="flex justify-between p-4 h-full w-full border-l-[10px] border-solid"
    >
        <div class="flex flex-col justify-between">
            <div>
                <div class="font-bold text-xl">
                    <span :style="{ color: me.stats.win ? '#5383e8' : '#e84057' }">
                        {{ webConfig.queue[queueId] }}
                    </span>
                </div>
                <span class="text-sm">{{ last_time }} days ago</span>
            </div>
            <div>
                <div class="font-bold text-xl">
                    <span>{{ me.stats.win ? '胜利' : '失败' }}</span>
                </div>
                <span class="text-sm">{{ duration }}</span>
            </div>
        </div>
        <div class="flex flex-col justify-center">
            <div class="flex">
                <div class="relative">
                    <championImg width="80" :championId="me.championId" />
                    <div
                        class="flex justify-center items-center absolute h-6 w-6 bottom-0 right-2 bg-black text-white font-bold rounded-full"
                    >
                        {{ me.stats.champLevel }}
                    </div>
                </div>
                <div class="flex items-center">
                    <div class="flex flex-col justify-center mx-2 h-full">
                        <spellImg class="item rounded mb-1" width="30" :spellId="me.spell1Id" />
                        <spellImg class="item rounded" width="30" :spellId="me.spell2Id" />
                    </div>
                    <div class="flex flex-col justify-center h-full">
                        <runeImg
                            class="item rounded mb-1"
                            width="30"
                            :runeId="me.stats.perkPrimaryStyle"
                        />
                        <runeImg class="item rounded" width="30" :runeId="me.stats.perkSubStyle" />
                    </div>
                </div>
                <div class="flex flex-col justify-center pl-5">
                    <div class="text-2xl">
                        {{ me.stats.kills }} /
                        <span class="text-red-600">{{ me.stats.deaths }}</span> /
                        {{ me.stats.assists }}
                    </div>
                    <div>
                        {{
                            (
                                (me.stats.kills + me.stats.assists) /
                                Math.max(me.stats.deaths, 1)
                            ).toFixed(2)
                        }}:1 KDA
                    </div>
                </div>
            </div>
            <div class="flex items-center mt-3">
                <itemImg
                    v-for="index in [0, 1, 2, 3, 4, 5, 6]"
                    v-if="me.stats['item' + index] != 0"
                    :key="index"
                    class="item ml-1"
                    :style="{ borderRadius: index === 6 ? '50%' : '5px' }"
                    width="30"
                    :itemId="me.stats['item' + index]"
                />
            </div>
        </div>
        <div v-if="summonerList" class="flex w-1/3">
            <div v-if="team100" class="flex flex-col basis-1/2">
                <div v-for="idx in team100" :key="idx" class="flex my-[2px] items-center">
                    <championImg width="30" :championId="summonerList[idx].championId" />

                    <div
                        class="ml-2 truncate cursor-pointer hover:underline"
                        @click="jumpSummoner(summonerList[idx].summonerId)"
                    >
                        {{ summonerList[idx].summonerName }}
                    </div>
                </div>
            </div>
            <div class="flex flex-col basis-1/2">
                <div v-for="idx in team200" :key="idx" class="flex items-center my-[2px]">
                    <championImg width="30" :championId="summonerList[idx].championId" />
                    <div
                        class="ml-2 truncate cursor-pointer hover:underline"
                        @click="jumpSummoner(summonerList[idx].summonerId)"
                    >
                        {{ summonerList[idx].summonerName }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import webConfig from '@/global.config'
import { championImg, itemImg, spellImg, runeImg } from './icons'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { diffDays, formatDuration } from '@/utils/common'
// prop
const props = defineProps(['gameId', 'summonerId'])
// route
const router = useRouter()
// refs
const queueId = ref()
const last_time = ref()
const duration = ref()
const me = ref()
const team100 = ref([])
const team200 = ref([])
const summonerList = ref()
// functions
const getMatchDetail = async () => {
    let list = []
    const res = await axios.get(`${webConfig.baseUrl}/match/${props.gameId}`)
    const data = res.data
    queueId.value = data.queueId
    last_time.value = diffDays(data.gameCreationDate)
    duration.value = formatDuration(data.gameDuration)
    for (let i = 0; i < data.participantIdentities.length; i++) {
        const summoner = {
            puuid: data.participantIdentities[i].player.puuid,
            summonerId: data.participantIdentities[i].player.summonerId,
            summonerName: data.participantIdentities[i].player.summonerName,
            championId: data.participants[i].championId,
        }
        list.push(summoner)
        if (data.participants[i].teamId === 100) team100.value.push(i)
        else team200.value.push(i)
        if (summoner.summonerId == props.summonerId) {
            me.value = data.participants[i]
        }
    }
    summonerList.value = list
}
const jumpSummoner = (summonerId) => {
    router.push('/account/' + summonerId)
}
onMounted(async () => {
    await getMatchDetail()
})
</script>
<style lang="scss" scoped>
img:not(.item) {
    border-radius: 50%;
}
</style>
