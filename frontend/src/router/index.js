import { createRouter, createWebHistory } from 'vue-router'
import { useGlobalStore } from '@/stores'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'index',
            component: () => import('@/views/index.vue'),
            children: [
                {
                    path: '/',
                    redirect: '/account',
                },
                {
                    path: '/account/:summonerId?',
                    name: 'account',
                    component: () => import('@/views/account.vue'),
                    meta: {
                        keepAlive: false, //false为不缓存
                    },
                },
                {
                    path: '/match/:puuid',
                    name: 'match',
                    component: () => import('@/views/match.vue'),
                    meta: {
                        keepAlive: false, //false为不缓存
                    },
                },
                {
                    path: '/play',
                    name: 'play',
                    component: () => import('@/views/play.vue'),
                    meta: {
                        keepAlive: true,
                    },
                },
                {
                    path: '/setting',
                    name: 'setting',
                    component: () => import('@/views/setting.vue'),
                    meta: {
                        keepAlive: true,
                    },
                },
            ],
        },
        {
            path: '/auth',
            name: 'auth',
            component: () => import('@/views/auth.vue'),
        },
    ],
})

router.beforeEach((to, from) => {
    const useGlobal = useGlobalStore()
    if (to.name !== 'auth' && !useGlobal.api_connected) {
        return { name: 'auth' }
    }
})

export default router
