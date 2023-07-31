<template>
    <img
        :width="props.width"
        :src="webConfig.baseUrl + '/imgs/perk/emblem-' + props.tier.toLowerCase() + '.png'"
    />
</template>
<script setup>
import webConfig from '@/global.config'
// props
const props = defineProps(['width', 'tier'])
</script>
