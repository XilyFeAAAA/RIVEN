<template>
    <VlazyImage
        :width="props.width"
        :src="
            'http://ddragon.leagueoflegends.com/cdn/13.14.1/img/profileicon/' +
            profileIconId +
            '.png'
        "
    />
</template>
<script setup>
// props
import VlazyImage from 'v-lazy-image'
const props = defineProps(['width', 'profileIconId'])
</script>
