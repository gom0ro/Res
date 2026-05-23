<template>
  <div
    class="skeleton"
    :class="[
      roundedClass,
      { 'skeleton--circle': variant === 'circle' },
    ]"
    :style="{ width, height }"
    role="status"
    aria-label="Загрузка"
  />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  width: { type: String, default: '100%' },
  height: { type: String, default: '1rem' },
  variant: { type: String, default: 'rect' }, // rect | circle
  rounded: { type: String, default: 'lg' }, // sm | md | lg | xl | 2xl | 3xl
})

const roundedClass = computed(() => {
  if (props.variant === 'circle') return 'rounded-full'
  const map = {
    sm: 'rounded-lg',
    md: 'rounded-xl',
    lg: 'rounded-2xl',
    xl: 'rounded-2xl',
    '2xl': 'rounded-3xl',
    '3xl': 'rounded-[1.75rem]',
  }
  return map[props.rounded] || 'rounded-2xl'
})
</script>
