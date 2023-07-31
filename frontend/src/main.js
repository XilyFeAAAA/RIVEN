import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import pinia from '@/stores/pinia'

import '@mdi/font/css/materialdesignicons.css'
import './assets/css/iconfont.css'
import './assets/css/main.css'
import './assets/css/common.scss'
import './assets/js/iconfont'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.use(pinia)
app.use(router)
app.mount('#app')
