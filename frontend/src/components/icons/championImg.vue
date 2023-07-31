<template>
    <img :width="props.width" :src="webConfig.champions[props.championId].avatar" />
</template>
<script setup>
import webConfig from '@/global.config'
// props
const props = defineProps(['width', 'championId'])
</script>
