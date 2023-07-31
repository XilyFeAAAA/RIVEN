<template>
    <img :width="props.width" :src="url" />
</template>
<script setup>
import { computed, onMounted } from 'vue'
// computed
const url = computed(() => {
    if (props.itemId === 0) {
        return 'https://gw.alipayobjects.com/zos/rmsportal/wYnHWSXDmBhiEmuwXsym.png'
    } else return 'https://game.gtimg.cn/images/lol/act/img/item/' + props.itemId + '.png'
})
// props
const props = defineProps(['width', 'itemId'])
</script>
