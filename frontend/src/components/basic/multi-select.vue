<template>
    <div class="multiselect">
        <div class="selected" @click="toggleDropdown">{{ selectedText }}</div>
        <teleport to="body">
            <div v-if="isOpen" class="dropdown-menu" ref="dropdownMenu">
                <div v-for="(item, index) in options" :key="index" class="dropdown-item">
                    <label>
                        <input type="checkbox" :value="item.value" v-model="selectedValues" />
                        {{ item.text }}
                    </label>
                </div>
            </div>
        </teleport>
    </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
    setup() {
        const isOpen = ref(false)
        const selectedValues = ref([])
        const options = ref([
            { text: '选项1', value: 1 },
            { text: '选项2', value: 2 },
            { text: '选项3', value: 3 },
            { text: '选项4', value: 4 },
            { text: '选项5', value: 5 },
        ])

        const toggleDropdown = () => {
            isOpen.value = !isOpen.value
        }

        const selectedText = computed(() => {
            if (selectedValues.value.length === 0) {
                return '请选择'
            } else if (selectedValues.value.length === 1) {
                const item = options.value.find(
                    (option) => option.value === selectedValues.value[0],
                )
                return item ? item.text : ''
            } else {
                return `已选择 ${selectedValues.value.length} 项`
            }
        })

        const handleClickOutside = (event) => {
            if (!event.target.closest('.dropdown-menu')) {
                isOpen.value = false
            }
        }

        const onMounted = () => {
            document.addEventListener('mousedown', handleClickOutside)
        }

        const onBeforeUnmount = () => {
            document.removeEventListener('mousedown', handleClickOutside)
        }

        return {
            isOpen,
            selectedValues,
            options,
            toggleDropdown,
            selectedText,
            onMounted,
            onBeforeUnmount,
        }
    },
    mounted() {
        this.onMounted()
    },
    beforeUnmount() {
        this.onBeforeUnmount()
    },
}
</script>

<style scoped>
.multiselect {
    position: relative;
    display: inline-block;
}
.multiselect .selected {
    cursor: pointer;
    padding: 10px;
    border: 1px solid #ccc;
}
.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 1000;
    min-width: 160px;
    padding: 5px 0;
    margin: 2px 0 0;
    font-size: 14px;
    text-align: left;
    list-style: none;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.175);
}
.dropdown-item {
    display: block;
    padding: 3px 20px;
    clear: both;
    font-weight: 400;
    color: #333;
    white-space: nowrap;
    background-color: transparent;
    border: 0;
    text-align: left;
}
.dropdown-item:hover {
    background-color: #f5f5f5;
}
</style>
