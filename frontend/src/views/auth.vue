<template>
    <div class="w-full h-full flex bg-[#f2f5f8]">
        <div class="h-full w-[420px] bg-white border border-[rgba(0, 0, 0, 0.12)] elevation-1">
            <div class="py-14 text-center">
                <div class="font-bold text-4xl text-[#344767]">Lux Helper</div>
                <div class="my-4 text-">Welcome! Let's build amazing things together.</div>
            </div>
        </div>
        <div class="flex-1 h-full flex flex-col justify-center items-center">
            <div v-if="onconnecting" class="bg-white elevation-3 py-16 w-full max-w-[450px]">
                <div class="flex justify-center my-5 rounded">
                    <div class="spinner"></div>
                </div>
                <div class="text-center">
                    <span class="text-2xl"> Connecting...</span>
                </div>
            </div>
            <div v-else class="bg-white elevation-3 w-full max-w-[450px] px-5 pt-10 pb-5">
                <div class="text-center">
                    <div class="text-2xl">Whoops...</div>
                    <div class="text-sm text-gray-500 my-5">连接失败</div>
                </div>

                <div class="w-full mt-10">
                    <button class="relative w-full h-[48px] bg-[#344767]" @click="connect">
                        <span class="font-bold text-white tracking-wider">Reconnect</span>
                    </button>
                </div>
            </div>
            <div class="py-5">
                <span class="font-thin text-sm">
                    客户端无法连接?<span class="ml-1 cursor-pointer">解决方案</span>
                </span>
            </div>

            <div class="absolute bottom-3">
                <span>Vue 3.2 & Vite 4.2 & FastApi</span>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGlobalStore } from '@/stores'
const useGlobal = useGlobalStore()
// router
const router = useRouter()
// ref
const retry_times = 5
const onconnecting = ref(false)
// function
const connect = async () => {
    onconnecting.value = true
    for (let i = 0; i < retry_times; i++) {
        const res = await useGlobal.connect()
        if (res) {
            return router.push('/account')
        } else {
            setTimeout(() => {
                console.log(`第${i}次重连`)
            }, 2000)
        }
    }
    onconnecting.value = false
}
onMounted(async () => {
    await connect()
})
</script>
<style lang="scss" scoped>
* {
    user-select: none;
}
button {
    border-radius: 5px;
    box-shadow: 0px 0px 20px -20px;
    transition: all 0.2s ease-in-out 0ms;
    font-family: 'Poppins', sans-serif;
}

button:hover {
    background-color: #4a5a77;
    box-shadow: 0px 0px 20px -18px;
}

button:active {
    transform: scale(0.95);
}
.spinner {
    width: 56px;
    height: 56px;
    display: grid;
    border: 4.5px solid #0000;
    border-radius: 50%;
    border-color: #dbdcef #0000;
    animation: spinner-e04l1k 1s infinite linear;
}

.spinner::before,
.spinner::after {
    content: '';
    grid-area: 1/1;
    margin: 2.2px;
    border: inherit;
    border-radius: 50%;
}

.spinner::before {
    border-color: #474bff #0000;
    animation: inherit;
    animation-duration: 0.5s;
    animation-direction: reverse;
}

.spinner::after {
    margin: 8.9px;
}

@keyframes spinner-e04l1k {
    100% {
        transform: rotate(1turn);
    }
}
.elevation-1 {
    box-shadow: 0 2px 10px -1px #55555514, 0 1px 10px #5555550f, 0 1px 30px #55555508 !important;
}
.elevation-3 {
    box-shadow: 0 3px 30px -2px #55555514, 0 3px 40px #5555550f, 0 1px 30px #55555508 !important;
}
</style>
