import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const stored = typeof localStorage !== 'undefined'
    ? localStorage.getItem('resort-theme')
    : null

  const theme = ref(stored === 'light' || stored === 'dark' ? stored : 'dark')

  const applyTheme = (value) => {
    const root = document.documentElement
    root.classList.remove('light', 'dark')
    root.classList.add(value)
    root.setAttribute('data-theme', value)
    localStorage.setItem('resort-theme', value)
  }

  const setTheme = (value) => {
    theme.value = value
    applyTheme(value)
  }

  const toggle = () => {
    setTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  const init = () => applyTheme(theme.value)

  watch(theme, applyTheme)

  return { theme, setTheme, toggle, init }
})
