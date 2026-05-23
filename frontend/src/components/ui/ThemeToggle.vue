<template>
  <button
    type="button"
    class="theme-toggle"
    :aria-label="themeStore.theme === 'dark' ? 'Светлая тема' : 'Тёмная тема'"
    @click="themeStore.toggle()"
  >
    <span class="theme-toggle__track">
      <span
        class="theme-toggle__thumb"
        :class="themeStore.theme === 'light' ? 'translate-x-[18px]' : 'translate-x-0.5'"
      >
        <SunIcon v-if="themeStore.theme === 'dark'" class="w-3 h-3 text-amber-400" />
        <MoonIcon v-else class="w-3 h-3 text-indigo-500" />
      </span>
    </span>
  </button>
</template>

<script setup>
import { SunIcon, MoonIcon } from '@heroicons/vue/24/outline'
import { useThemeStore } from '../../stores/theme'

const themeStore = useThemeStore()
</script>

<style scoped>
.theme-toggle {
  @apply p-0.5 rounded-xl transition-all duration-300;
  background: var(--surface-muted);
  border: 1px solid var(--border-subtle);
}
.theme-toggle:hover {
  border-color: var(--border-hover);
  background: var(--surface-hover);
}
.theme-toggle__track {
  @apply relative flex items-center w-10 h-5 rounded-full;
  background: var(--surface-elevated);
}
.theme-toggle__thumb {
  @apply absolute flex items-center justify-center w-4 h-4 rounded-full transition-transform duration-300;
  transition-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
  background: var(--surface-card);
  box-shadow: var(--shadow-sm);
}
</style>
