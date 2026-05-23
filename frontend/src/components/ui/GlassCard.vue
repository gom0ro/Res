<template>
  <component
    :is="tag"
    v-motion
    :initial="motionInitial"
    :enter="motionEnter"
    :hover="hoverable ? { y: -2, transition: { duration: 250 } } : undefined"
    class="glass-card"
    :class="[
      paddingClass,
      roundedClass,
      { 'glass-card--interactive': hoverable, 'glass-card--flat': !hoverable },
    ]"
  >
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tag: { type: String, default: 'div' },
  hoverable: { type: Boolean, default: true },
  padding: { type: String, default: 'none' }, // none | sm | md | lg
  rounded: { type: String, default: '3xl' },
  delay: { type: Number, default: 0 },
  animate: { type: Boolean, default: true },
})

const paddingClass = computed(() => ({
  none: '',
  sm: 'p-4',
  md: 'p-5',
  lg: 'p-6',
}[props.padding]))

const roundedClass = computed(() => ({
  '2xl': 'rounded-[1.25rem]',
  '3xl': 'rounded-[1.5rem]',
  '4xl': 'rounded-[1.75rem]',
}[props.rounded] || 'rounded-[1.5rem]'))

const motionInitial = computed(() =>
  props.animate ? { opacity: 0, y: 16 } : false
)
const motionEnter = computed(() =>
  props.animate
    ? {
        opacity: 1,
        y: 0,
        transition: {
          delay: props.delay,
          duration: 450,
          ease: [0.22, 1, 0.36, 1],
        },
      }
    : false
)
</script>
