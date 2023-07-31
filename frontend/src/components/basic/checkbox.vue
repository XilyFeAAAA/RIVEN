<template>
    <div class="checkbox-wrapper-8">
        <input
            type="checkbox"
            :id="id"
            class="tgl tgl-skewed"
            v-model="isChecked"
            @change="onChange"
        />
        <label :for="id" data-tg-on="ON" data-tg-off="OFF" class="tgl-btn"></label>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
    checked: {
        type: Boolean,
        default: false,
    },
    id: {
        type: String,
        required: true,
    },
})

const emits = defineEmits(['change', 'update:checked'])

const isChecked = ref(props.checked)
const id = ref(props.id)
const onChange = () => {
    emits('update:checked', isChecked.value)
    emits('change')
}
defineExpose({
    isChecked,
})
</script>

<style>
.checkbox-wrapper-8 .tgl {
    display: none;
}

.checkbox-wrapper-8 .tgl,
.checkbox-wrapper-8 .tgl:after,
.checkbox-wrapper-8 .tgl:before,
.checkbox-wrapper-8 .tgl *,
.checkbox-wrapper-8 .tgl *:after,
.checkbox-wrapper-8 .tgl *:before,
.checkbox-wrapper-8 .tgl + .tgl-btn {
    box-sizing: border-box;
}

.checkbox-wrapper-8 .tgl::-moz-selection,
.checkbox-wrapper-8 .tgl:after::-moz-selection,
.checkbox-wrapper-8 .tgl:before::-moz-selection,
.checkbox-wrapper-8 .tgl *::-moz-selection,
.checkbox-wrapper-8 .tgl *:after::-moz-selection,
.checkbox-wrapper-8 .tgl *:before::-moz-selection,
.checkbox-wrapper-8 .tgl + .tgl-btn::-moz-selection,
.checkbox-wrapper-8 .tgl::selection,
.checkbox-wrapper-8 .tgl:after::selection,
.checkbox-wrapper-8 .tgl:before::selection,
.checkbox-wrapper-8 .tgl *::selection,
.checkbox-wrapper-8 .tgl *:after::selection,
.checkbox-wrapper-8 .tgl *:before::selection,
.checkbox-wrapper-8 .tgl + .tgl-btn::selection {
    background: none;
}

.checkbox-wrapper-8 .tgl + .tgl-btn {
    outline: 0;
    display: block;
    width: 4em;
    height: 2em;
    position: relative;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.checkbox-wrapper-8 .tgl + .tgl-btn:after,
.checkbox-wrapper-8 .tgl + .tgl-btn:before {
    position: relative;
    display: block;
    content: '';
    width: 50%;
    height: 100%;
}

.checkbox-wrapper-8 .tgl + .tgl-btn:after {
    left: 0;
}

.checkbox-wrapper-8 .tgl + .tgl-btn:before {
    display: none;
}

.checkbox-wrapper-8 .tgl:checked + .tgl-btn:after {
    left: 50%;
}

.checkbox-wrapper-8 .tgl-skewed + .tgl-btn {
    overflow: hidden;
    transform: skew(-10deg);
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
    transition: all 0.2s ease;
    font-family: sans-serif;
    background: #888;
}

.checkbox-wrapper-8 .tgl-skewed + .tgl-btn:after,
.checkbox-wrapper-8 .tgl-skewed + .tgl-btn:before {
    transform: skew(10deg);
    display: inline-block;
    transition: all 0.2s ease;
    width: 100%;
    text-align: center;
    position: absolute;
    line-height: 2em;
    font-weight: bold;
    color: #fff;
    text-shadow: 0 1px 0 rgba(0, 0, 0, 0.4);
}

.checkbox-wrapper-8 .tgl-skewed + .tgl-btn:after {
    left: 100%;
    content: attr(data-tg-on);
}

.checkbox-wrapper-8 .tgl-skewed + .tgl-btn:before {
    left: 0;
    content: attr(data-tg-off);
}

.checkbox-wrapper-8 .tgl-skewed + .tgl-btn:active {
    background: #888;
}

.checkbox-wrapper-8 .tgl-skewed + .tgl-btn:active:before {
    left: -10%;
}

.checkbox-wrapper-8 .tgl-skewed:checked + .tgl-btn {
    background: #86d993;
}

.checkbox-wrapper-8 .tgl-skewed:checked + .tgl-btn:before {
    left: -100%;
}

.checkbox-wrapper-8 .tgl-skewed:checked + .tgl-btn:after {
    left: 0;
}

.checkbox-wrapper-8 .tgl-skewed:checked + .tgl-btn:active:after {
    left: 10%;
}
</style>
