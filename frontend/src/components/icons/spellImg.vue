<template>
    <img :width="props.width" :src="url" />
</template>
<script setup>
import { computed } from 'vue'
import Webconfig from '@/global.config'
// props
const props = defineProps(['width', 'spellId'])
const url = computed(() => {
    if (Webconfig.spells[props.spellId] === undefined) {
        return 'https://gw.alipayobjects.com/zos/rmsportal/wYnHWSXDmBhiEmuwXsym.png'
    } else
        return (
            'https://game.gtimg.cn/images/lol/act/img/spell/' +
            Webconfig.spells[props.spellId] +
            '.png'
        )
})
</script>
