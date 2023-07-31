import { h, Transition } from 'vue'

const transitionStyle = '0.3s height ease-in-out'

function beforeEnter(el) {
    el.style.transition = transitionStyle
    if (!el.dataset) el.dataset = {}
    el.style.height = 0
}

function enter(el) {
    if (el.scrollHeight !== 0) {
        el.style.height = `${el.scrollHeight}px`
    } else {
        el.style.height = ''
    }
    el.style.overflow = 'hidden'
}

function afterEnter(el) {
    el.style.transition = ''
    el.style.height = ''
}

function beforeLeave(el) {
    if (!el.dataset) el.dataset = {}
    el.style.display = 'block'
    el.style.height = `${el.scrollHeight}px`
    el.style.overflow = 'hidden'
}

function leave(el) {
    if (el.scrollHeight !== 0) {
        el.style.transition = transitionStyle
        el.style.height = 0
    }
}

function afterLeave(el) {
    el.style.transition = ''
    el.style.height = ''
}

export default {
    name: 'CollapseTransition',
    setup(_, { slots }) {
        return () =>
            h(
                Transition,
                {
                    onBeforeEnter: beforeEnter,
                    onEnter: enter,
                    onAfterEnter: afterEnter,
                    onBeforeLeave: beforeLeave,
                    onLeave: leave,
                    onAfterLeave: afterLeave,
                },
                slots.default,
            )
    },
}
