<template>
    <img
        :width="props.width"
        :src="webConfig.baseUrl + `/imgs/position/icon-position-${props.position}.svg`"
    />
</template>
<script setup>
import webConfig from '@/global.config'
// props
const props = defineProps(['width', 'position'])
</script>
