<template>
  <div
    class="premium-bg fixed inset-0 pointer-events-none overflow-hidden z-0"
    aria-hidden="true"
  >
    <!-- Gradient mesh -->
    <div
      class="premium-bg__mesh absolute inset-0 transition-transform duration-[1200ms] ease-out will-change-transform"
      :style="meshStyle"
    />

    <!-- Floating orbs -->
    <div
      v-for="(orb, i) in orbs"
      :key="i"
      class="premium-bg__orb absolute rounded-full will-change-transform"
      :class="orb.animation"
      :style="{
        width: orb.size,
        height: orb.size,
        top: orb.top,
        left: orb.left,
        right: orb.right,
        bottom: orb.bottom,
        background: orb.gradient,
        filter: `blur(${orb.blur}px)`,
        opacity: orb.opacity,
        transform: `translate(${parallax.x * orb.depth}px, ${parallax.y * orb.depth}px)`,
        transition: reducedMotion ? 'none' : 'transform 0.8s cubic-bezier(0.22, 1, 0.36, 1)',
      }"
    />

    <!-- Subtle grid -->
    <div class="premium-bg__grid absolute inset-0" />

    <!-- Light noise -->
    <div class="premium-bg__noise absolute inset-0" />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useMouse, usePreferredReducedMotion } from '@vueuse/core'
import { useThemeStore } from '../../stores/theme'

const themeStore = useThemeStore()
const { x, y } = useMouse()
const reducedMotion = usePreferredReducedMotion()

const centerX = ref(typeof window !== 'undefined' ? window.innerWidth / 2 : 0)
const centerY = ref(typeof window !== 'undefined' ? window.innerHeight / 2 : 0)

const updateCenter = () => {
  centerX.value = window.innerWidth / 2
  centerY.value = window.innerHeight / 2
}

onMounted(() => {
  updateCenter()
  window.addEventListener('resize', updateCenter)
})
onUnmounted(() => window.removeEventListener('resize', updateCenter))

const parallax = computed(() => {
  if (reducedMotion.value) return { x: 0, y: 0 }
  const factor = 0.012
  return {
    x: (x.value - centerX.value) * factor,
    y: (y.value - centerY.value) * factor,
  }
})

const meshStyle = computed(() => {
  const px = parallax.value.x * 0.5
  const py = parallax.value.y * 0.5
  const isLight = themeStore.theme === 'light'
  return {
    transform: `translate(${px}px, ${py}px)`,
    background: isLight
      ? `
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(59, 130, 246, 0.12), transparent 50%),
        radial-gradient(ellipse 70% 50% at 85% 80%, rgba(124, 58, 237, 0.1), transparent 50%),
        radial-gradient(ellipse 60% 40% at 50% 50%, rgba(6, 182, 212, 0.06), transparent 55%)
      `
      : `
        radial-gradient(ellipse 80% 60% at 15% 5%, rgba(59, 130, 246, 0.14), transparent 55%),
        radial-gradient(ellipse 70% 50% at 90% 85%, rgba(124, 58, 237, 0.1), transparent 55%),
        radial-gradient(ellipse 55% 45% at 45% 45%, rgba(99, 102, 241, 0.06), transparent 60%)
      `,
  }
})

const orbs = computed(() => {
  const isLight = themeStore.theme === 'light'
  const baseOpacity = isLight ? 0.35 : 1
  return [
    {
      size: '520px',
      top: '-180px',
      left: '-120px',
      gradient: 'radial-gradient(circle, rgba(59,130,246,0.35), transparent 68%)',
      blur: 72,
      opacity: 0.06 * baseOpacity,
      depth: 1.2,
      animation: 'animate-orb',
    },
    {
      size: '440px',
      bottom: '-140px',
      right: '-80px',
      gradient: 'radial-gradient(circle, rgba(124,58,237,0.3), transparent 70%)',
      blur: 80,
      opacity: 0.05 * baseOpacity,
      depth: 0.8,
      animation: 'animate-orb-2',
    },
    {
      size: '360px',
      top: '38%',
      left: '42%',
      gradient: 'radial-gradient(circle, rgba(6,182,212,0.25), transparent 72%)',
      blur: 64,
      opacity: 0.04 * baseOpacity,
      depth: 0.5,
      animation: 'animate-orb-3',
    },
  ]
})
</script>
