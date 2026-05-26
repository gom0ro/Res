<template>
  <div class="min-h-[100dvh] flex items-center justify-center relative overflow-hidden app-shell safe-top safe-bottom px-4 py-8">

    <PremiumBackground />
    <div class="fixed top-6 right-6 z-20">
      <ThemeToggle />
    </div>

    <div
      v-motion
      :initial="{ opacity: 0, y: 24, scale: 0.98 }"
      :enter="{ opacity: 1, y: 0, scale: 1, transition: { duration: 550, ease: [0.22, 1, 0.36, 1] } }"
      class="relative z-10 w-full max-w-[22rem] mx-4"
    >
      <div class="glass-card glass-card--flat rounded-premium-xl p-8 sm:p-9 !shadow-modal">
        <div class="flex flex-col items-center mb-8">
          <div
            class="w-14 h-14 rounded-premium-xl flex items-center justify-center mb-5"
            style="background: linear-gradient(135deg, var(--accent-from), var(--accent-to)); box-shadow: var(--glow-md)"
          >
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-ink tracking-tight">Resort <span class="text-gradient">OS</span></h1>
          <p class="text-ink-muted text-sm mt-1.5 font-medium">Панель управления курортом</p>
        </div>

        <form class="space-y-5" @submit.prevent="handleLogin">
          <div
            v-motion
            :initial="{ opacity: 0, y: 8 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: 120, duration: 400 } }"
          >
            <label class="block text-[10px] font-semibold text-ink-muted mb-2 uppercase tracking-[0.12em]">Email</label>
            <div class="relative">
              <input v-model="email" type="email" required placeholder="admin@resort.com" class="input-premium pl-10" />
              <svg class="w-4 h-4 text-ink-muted absolute left-3.5 top-3.5 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
              </svg>
            </div>
          </div>

          <div
            v-motion
            :initial="{ opacity: 0, y: 8 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: 180, duration: 400 } }"
          >
            <label class="block text-[10px] font-semibold text-ink-muted mb-2 uppercase tracking-[0.12em]">Пароль</label>
            <div class="relative">
              <input v-model="password" type="password" required placeholder="••••••••" class="input-premium pl-10" />
              <svg class="w-4 h-4 text-ink-muted absolute left-3.5 top-3.5 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
          </div>

          <button
            v-motion
            :initial="{ opacity: 0 }"
            :enter="{ opacity: 1, transition: { delay: 260, duration: 400 } }"
            type="submit"
            :disabled="loading"
            class="btn-primary w-full py-3.5 mt-1 flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ loading ? 'Вход...' : 'Войти в систему' }}
          </button>
        </form>

        <div class="flex items-center justify-center gap-2 mt-7">
          <span class="text-[10px] text-ink-muted font-medium">Resort Management</span>
          <span class="text-[9px] px-1.5 py-0.5 rounded-md font-bold text-emerald-400" style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.15)">v1.0</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { toast } from 'vue3-toastify'
import PremiumBackground from '../components/ui/PremiumBackground.vue'
import ThemeToggle from '../components/ui/ThemeToggle.vue'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    toast.success('Добро пожаловать!')
    router.push('/')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка входа')
  } finally {
    loading.value = false
  }
}
</script>
