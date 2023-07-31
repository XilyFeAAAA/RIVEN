<template>
    <img :width="props.width" :src="url" />
</template>
<script setup>
import { computed } from 'vue'
import Webconfig from '@/global.config'
// props
const props = defineProps(['width', 'runeId'])
const url = computed(() => {
    if (Webconfig.runes[props.runeId] === undefined) {
        return 'https://gw.alipayobjects.com/zos/rmsportal/wYnHWSXDmBhiEmuwXsym.png'
    } else
        return (
            'https://game.gtimg.cn/images/lol/act/img/rune/' +
            Webconfig.runes[props.runeId] +
            '.png'
        )
})
</script>
