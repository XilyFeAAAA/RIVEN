<template>
    <input hidden="" class="check-icon" :id="props.id" name="check-icon" type="checkbox" />
    <label class="icon-menu" :for="props.id">
        <div class="bar bar--1"></div>
        <div class="bar bar--2"></div>
        <div class="bar bar--3"></div>
    </label>
</template>
<script setup>
const props = defineProps(['id'])
</script>
<style lang="scss" scoped>
.icon-menu {
    --gap: 3px;
    --height-bar: 2px;
    --pos-y-bar-one: 0;
    --pos-y-bar-three: 0;
    --scale-bar: 1;
    --rotate-bar-one: 0;
    --rotate-bar-three: 0;
    width: 15px;
    display: flex;
    flex-direction: column;
    gap: var(--gap);
    cursor: pointer;
    position: relative;
}

.bar {
    position: relative;
    height: var(--height-bar);
    width: 100%;
    border-radius: 0.5rem;
    background-color: #000;
}

.bar--1 {
    top: var(--pos-y-bar-one);
    transform: rotate(var(--rotate-bar-one));
    transition: top 200ms 100ms, transform 100ms;
}

.bar--2 {
    transform: scaleX(var(--scale-bar));
    transition: transform 150ms 100ms;
}

.bar--3 {
    bottom: var(--pos-y-bar-three);
    transform: rotate(var(--rotate-bar-three));
    transition: bottom 200ms 100ms, transform 100ms;
}

.check-icon:checked + .icon-menu > .bar--1 {
    transition: top 200ms, transform 200ms 100ms;
}

.check-icon:checked + .icon-menu > .bar--3 {
    transition: bottom 200ms, transform 200ms 100ms;
}

.check-icon:checked + .icon-menu {
    --pos-y-bar-one: calc(var(--gap) + var(--height-bar));
    --pos-y-bar-three: calc(var(--gap) + var(--height-bar));
    --scale-bar: 0;
    --rotate-bar-one: 45deg;
    --rotate-bar-three: -45deg;
}
/* FIN ICON-MENU */
</style>
