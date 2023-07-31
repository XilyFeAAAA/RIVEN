// store/global.js
import webConfig from '@/global.config'
import { defineStore } from 'pinia'
import axios from 'axios'

const api = {
    summoner: '/current-summoner',
    state: '/state',
    setting: '/get-app-setting',
}

// 创建 store
const useGlobalStore = defineStore('global', {
    // 定义状态：一个函数，返回一个对象
    state: () => ({
        _summoner: null,
        _current_game: null,
        _api_connected: false,
        _settings: null,
    }),
    getters: {
        summoner: (state) => {
            return state._summoner
        },
        current_game: (state) => {
            return state._current_game
        },
        api_connected: (state) => {
            return state._api_connected
        },
        settings: (state) => {
            return state._settings
        },
    },
    // 定义 actions，有同步和异步两种类型
    actions: {
        async getSummonerInfo() {
            if (!this._summoner) {
                const res = await axios.get(webConfig.baseUrl + api.summoner)
                this._summoner = res.data
            }
            return this._summoner
        },
        async connect() {
            try {
                const res = await axios.get(webConfig.baseUrl + api.state, {
                    timeout: 5000,
                })
                this._api_connected = res.data
                return res.data
            } catch (error) {
                return false
            }
        },
        async getSetting() {
            const res = await axios.get(webConfig.baseUrl + api.setting)
            this._settings = res.data
        },
        setCurrentGame(game) {
            this._current_game = game
        },
        setSetting(new_setting) {
            this._settings = new_setting
        },
    },
})

export default useGlobalStore
