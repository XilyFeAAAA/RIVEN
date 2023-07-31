<template>
    <div class="nav">
        <div class="nav-card flex justify-center items-center">
            <img width="45" src="../assets/imgs/icon.png" alt="" />
            <span class="text-4xl font-bold mx-2">RIVEN</span>
        </div>
        <div class="nav-content">
            <div class="nav-list overflow-y-auto non-scrollbar">
                <template v-for="(item, idx) in webConfig.nav_list" :key="idx">
                    <router-link :to="{ name: item.name }" v-if="!item.section">
                        <a class="nav-list-item" :class="{ active: current_path === item.name }">
                            <div class="item--overlay"></div>
                            <div class="item-content">
                                <div class="item-icon">
                                    <i class="mdi" :class="item.icon"></i>
                                </div>
                                <div class="item-text">
                                    <span>{{ item.text }}</span>
                                </div>
                            </div>
                        </a></router-link
                    >
                    <div v-else class="p-1 leading-8 text-sm tracking-[0.16rem]">
                        {{ item.text }}
                    </div>
                </template>
            </div>
        </div>
        <div class="nav-append p-3">
            <div class="nav-author p-2 rounded-[4px]">
                <div class="card-title">
                    <button @click="openExternel('http://github.com/XilyFeAAAA')">
                        <span class="mdi mdi-github"></span>
                    </button>
                    <span class="font-bold tracking-wider mx-3">Xilyfe</span>
                </div>
                <div class="card-text">
                    <div><b class="tracking-wide">Github:</b></div>
                    <div class="tracking-normal">github.com/XilyFeAAAA</div>
                </div>
                <div class="card-action">
                    <button
                        class="flex items-center justify-center bg-white w-full px-2 h-9 rounded"
                        @click="openExternel('http://github.com/XilyFeAAAA')"
                    >
                        <i class="mdi-thumb-up-outline mdi mr-1"></i>
                        Star-Me
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import webConfig from '@/global.config'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { openExternel } from '@/utils/common'
// ref
const current_path = ref()
// route
const route = useRoute()
watch(
    () => route,
    (toParams, previousParams) => {
        current_path.value = toParams.name
    },
    { immediate: true, deep: true },
)
</script>
<style lang="scss" scoped>
* {
    user-select: none;
}
.nav {
    width: 100%;
    height: 100%;
    .nav-card {
        height: 100px;
        box-shadow: rgba(0, 0, 0, 0.05) 0px 25px 15px -20px;
    }
    .nav-content {
        flex: 0 1 auto;
        height: calc(100% - 325px);
        max-width: 100%;
        .nav-list {
            height: 100%;
            position: relative;
            padding: 8px;
            background-color: transparent;
            .nav-list-item {
                display: block;
                position: relative;
                margin-bottom: 4px;
                min-height: 48px;
                padding-inline-start: 8px;
                padding-inline-end: 8px;
                border-radius: 4px;
                overflow: hidden;
                cursor: pointer;
                .item--overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    height: 100%;
                    width: 100%;
                    opacity: 0;
                    background-color: rgb(52, 71, 103);
                    pointer-events: none;
                    transition: opacity 0.2s ease-in-out;
                }
                .item-content {
                    display: flex;
                    align-items: center;
                    line-height: 40px;
                    .item-icon {
                        font-size: 25px;
                        opacity: 0.6;
                    }
                    .item-text {
                        margin: 0 30px;
                        font-size: 0.875rem;
                    }
                }
                &:hover .item--overlay {
                    opacity: 0.04;
                }
                &.active {
                    border-left: 5px solid;
                    border-image-slice: 1;
                    border-image-source: linear-gradient(to bottom, #3a456c, #a4abbb);
                    .item--overlay {
                        opacity: 0.12;
                    }
                }
            }
        }
    }
    .nav-append {
        height: 225px;
        box-shadow: rgba(0, 0, 0, 0.05) 0px -25px 15px -20px;
        .nav-author {
            height: 200px;
            background-color: rgb(30, 41, 59);
            box-shadow: #919eab4d 0 0 2px, #919eab05 0 12px 24px -4px !important;
            .card-title {
                display: flex;
                align-items: center;
                line-height: 2rem;
                flex: none;
                font-size: 1.25rem;
                font-weight: 500;
                padding: 0.5rem 1rem;
                color: #fff;
                button {
                    margin-right: 8px;
                    height: 40px;
                    width: 40px;
                    color: #000;
                    font-size: 40px;
                    background-color: #fff;
                    border-radius: 50%;
                }
            }
            .card-text {
                line-height: 1.25rem;
                flex: 1 1 auto;
                font-size: 0.875rem;
                font-weight: 400;
                padding: 1rem;
                text-transform: none;
                color: #fff;
            }
            .card-action {
                align-items: center;
                display: flex;
                flex: none;
                min-height: 52px;
                padding: 0.5rem;
                button {
                    &:hover {
                        opacity: 0.9;
                    }
                }
            }
        }
    }
}
</style>
