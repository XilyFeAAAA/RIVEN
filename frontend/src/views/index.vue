<template>
    <div
        class="relative w-full h-full overflow-hidden"
        :style="{ '--v-layout-width': shrink ? '0px' : '220px' }"
    >
        <nav :style="{ transform: shrink ? 'translateX(-100%)' : 'translateX(0%)' }">
            <nav_drawer></nav_drawer>
        </nav>
        <header>
            <div class="h-16 flex items-center justify-between px-2 drag">
                <div class="flex items-center">
                    <div class="non-drag">
                        <button
                            class="w-12 h-12 rounded-full hover:bg-slate-100 active:bg-slate-300"
                            @click="shrink = !shrink"
                        >
                            <span class="mdi mdi-menu text-2xl"></span>
                        </button>
                    </div>
                    <div class="non-drag inp_shadow w-[400px] h-12 px-2 flex items-center rounded">
                        <div class="flex h-full justify-center items-center">
                            <span class="mdi mdi-magnify text-lg opacity-60"></span>
                        </div>
                        <div class="h-full ml-3 flex-1">
                            <input
                                type="text"
                                class="h-full w-full flex-wrap"
                                placeholder="Search"
                                v-model="summonerName"
                                @keydown="onKeyDown"
                            />
                        </div>
                    </div>
                </div>
                <div class="flex items-center mx-5 select-none">
                    <div v-if="summoner" class="h-12 w-12">
                        <profileImg
                            class="rounded-full non-drag cursor-pointer"
                            width="45"
                            :profileIconId="summoner.profileIconId"
                            @click="router.push('/account')"
                        />
                    </div>
                    <div v-if="summoner" class="h-12 ml-4">
                        <div>
                            <span
                                class="non-drag cursor-pointer hover:underline"
                                @click="router.push('/account')"
                            >
                                {{ summoner.displayName }}
                            </span>
                        </div>
                        <div v-if="status" class="text-sm text-blue-700">
                            <span> {{ webConfig.status[status] }}</span>
                        </div>
                    </div>
                    <button
                        class="non-drag w-12 h-12 rounded-full hover:bg-slate-100 active:bg-slate-300 ml-5"
                        @click="minWindow"
                    >
                        <span class="mdi mdi-window-minimize text-lg"></span>
                    </button>
                    <button
                        class="non-drag w-12 h-12 rounded-full hover:bg-slate-100 active:bg-slate-300"
                        @click="maxWindow"
                    >
                        <span class="mdi mdi-dock-window text-lg"></span>
                    </button>
                    <button
                        class="non-drag w-12 h-12 rounded-full hover:bg-slate-100 active:bg-slate-300"
                        @click="closeWindow"
                    >
                        <span class="mdi mdi-window-close text-lg"></span>
                    </button>
                </div>
            </div>
        </header>
        <main class="bg-[#f2f5f8]">
            <router-view v-slot="{ Component }">
                <keep-alive :include="['play', 'setting', 'account']">
                    <component :is="Component" />
                </keep-alive>
            </router-view>
        </main>
    </div>
</template>
<script setup>
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import { ref, onMounted, watch } from 'vue'
import { profileImg } from '@/components/icons'
import ws from '@/utils/websocket'
import { useGlobalStore } from '@/stores'
import nav_drawer from './nav_drawer.vue'
import webConfig from '@/global.config'
// ws
const ws_instance = ws.getInstance()
// route
const route = useRoute()
const router = useRouter()
// refs
const status = ref()
const summoner = ref()
const summonerName = ref()
const shrink = ref(false)
// pinia
const useGlobal = useGlobalStore()
const getPanelDataInSelect = async () => {
    const res = await axios.get(`${webConfig.baseUrl}/paneldata-champselect`)
    const data = {
        teams: [res.data[0]],
        teamup: [res.data[1]],
    }
    useGlobal.setCurrentGame(data)
}
const getPanelDataInGame = async () => {
    const res = await axios.get(`${webConfig.baseUrl}/paneldata-game`)
    // const data = {
    //     teams: [res.data['ORDER'], res.data['CHAOS']],
    // }
    const data = {
        teams: [res.data[0]['ORDER'], res.data[0]['CHAOS']],
        teamup: [res.data[1]['ORDER'], res.data[1]['CHAOS']],
    }
    useGlobal.setCurrentGame(data)
}
const maxWindow = () => {
    window.ipcRenderer.send('window-max')
}
const minWindow = () => {
    window.ipcRenderer.send('window-min') // 通知主进程我要进行窗口最小化操作
}
const closeWindow = () => {
    window.ipcRenderer.send('window-close')
}
watch(
    () => route.name,
    (to, prev) => {
        shrink.value = true
    },
)
onMounted(async () => {
    await useGlobal.getSetting()
    summoner.value = await useGlobal.getSummonerInfo()
    ws_instance.onmessage = async (event) => {
        const data = JSON.parse(event.data)
        if (data.uri === '/lol-gameflow/v1/gameflow-phase') {
            status.value = data.data
            if (data.data === 'ChampSelect') {
                // 获取面板数据inselect
                setTimeout(async () => {
                    await getPanelDataInSelect()
                    await send_remarks()
                }, 2000)
            }
            if (data.data === 'InProgress') {
                // 获取面板数据ingame
                setTimeout(async () => {
                    await getPanelDataInGame()
                }, 5000)
            }
        }
    }
})
// functions
const onKeyDown = async (event) => {
    if (event.keyCode === 13) {
        if (!summonerName.value) {
            return router.push('/account')
        }
        const res = await axios.get(`${webConfig.baseUrl}/summoner-byname/${summonerName.value}`)
        router.push('/account/' + res.data.summonerId)
    }
}
const send_remarks = async () => {
    if (!useGlobal.settings.remark.enable || useGlobal.current_game === null) return
    let msg = 'RIVEN英雄联盟助手:'
    const sorted = useGlobal.current_game.teams[0].sort((a, b) => {
        a.match.source - b.match.source
    })
    sorted.forEach((summoner) => {
        if (
            !useGlobal.settings.remark.excludeme ||
            summoner.summonerId != useGlobal.summoner.summonerId
        ) {
            msg += `\n玩家：${summoner.summonerName} 评分${summoner.match.source.toFixed(1)}`
        }
    })
    const teamup1 = useGlobal.current_game.teamup[0][0].join(',')
    const teamup2 = useGlobal.current_game.teamup[0][1].join(',')
    if (teamup1 || teamup2) {
        msg += `\n我方组排: ${teamup1 ? `(${teamup1})` : ''} ${teamup1 ? `(${teamup1})` : ''}`
    }
    await axios.post(webConfig.baseUrl + '/send_msg', {
        msg: msg,
        type: useGlobal.settings.remark.type,
    })
}
</script>
<style lang="scss" scoped>
.slide-enter-active,
.slide-leave-active {
    transition: all 0.75s ease-out;
}

.slide-enter-to {
    position: absolute;
    right: 0;
}

.slide-enter-from {
    position: absolute;
    right: -100%;
}

.slide-leave-to {
    position: absolute;
    left: -100%;
}

.slide-leave-from {
    position: absolute;
    left: 0;
}
nav {
    position: fixed;
    top: 0px;
    left: 0px;
    height: 100%;
    width: 220px;
    z-index: 1008;
    background-color: #fff;
    box-shadow: 0 2px 10px -1px #55555514, 0 1px 10px #5555550f, 0 1px 30px #55555508 !important;
    transition: all 0.2s ease-in-out;
}
main {
    display: flex;
    flex-direction: column;
    height: 100%;
    flex: 1 0 auto;
    padding-left: var(--v-layout-width);
    // padding-left: 256px;
    padding-top: 64px;
    max-width: 100%;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) 0.1s;
}
.drag {
    -webkit-app-region: drag;
}
.non-drag {
    -webkit-app-region: no-drag;
}
header {
    top: 0px;
    z-index: 1006;
    transform: translateY(0%);
    position: fixed;
    right: 0;
    width: calc((100% - var(--v-layout-width)) - 0px);
    box-shadow: 0 2px 30px -1px #55555514, 0 4px 30px #5555550f, 0 1px 30px #55555508;
    background-color: #fff;
    color: #000;
    transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1) 0.1s;
}
.inp_shadow {
    box-shadow: 0 3px 10px -2px #55555514, 0 2px 20px #5555550f, 0 1px 30px #55555508;
}
</style>
