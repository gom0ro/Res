<template>
  <div class="app-shell">
    <router-view />
  </div>
</template>

<script setup>
import { watch } from 'vue'
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()

watch(
  () => themeStore.theme,
  (t) => {
    document.body.setAttribute('data-theme', t)
  },
  { immediate: true }
)
</script>
