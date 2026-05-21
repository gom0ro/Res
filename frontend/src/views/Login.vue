<template>
  <div class="min-h-screen flex items-center justify-center bg-[#0a0f1c] relative overflow-hidden font-sans">
    
    <!-- Animated background elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute w-[600px] h-[600px] bg-primary-600/20 rounded-full blur-[100px] -top-20 -left-20 animate-slow-spin mix-blend-screen"></div>
      <div class="absolute w-[800px] h-[800px] bg-purple-600/20 rounded-full blur-[120px] top-1/2 -right-40 animate-slow-spin-reverse mix-blend-screen"></div>
      <div class="absolute w-[400px] h-[400px] bg-blue-500/10 rounded-full blur-[80px] bottom-0 left-1/4 animate-pulse mix-blend-screen"></div>
    </div>
    
    <div class="glass-dark p-10 sm:p-12 rounded-[2rem] w-full max-w-md z-10 shadow-2xl shadow-black/50 border border-white/10 mx-4 backdrop-blur-2xl transition-transform transform hover:scale-[1.01] duration-500">
      
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-primary-500 to-purple-500 shadow-lg shadow-primary-500/30 mb-6 relative group">
          <div class="absolute inset-0 bg-white/20 rounded-2xl blur group-hover:blur-md transition-all"></div>
          <svg class="w-8 h-8 text-white relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
        </div>
        <h1 class="text-3xl font-black text-white mb-2 tracking-tight">Resort Manager</h1>
        <p class="text-gray-400 font-medium">Войдите в панель управления</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-semibold text-gray-300 mb-2">Email</label>
          <div class="relative">
            <input 
              v-model="email" 
              type="email" 
              required
              class="w-full px-5 py-4 pl-12 rounded-xl bg-dark-surface/50 border border-dark-border text-white placeholder-gray-500 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 outline-none backdrop-blur-sm"
              placeholder="admin@resort.com"
            />
            <svg class="w-5 h-5 text-gray-500 absolute left-4 top-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path></svg>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-300 mb-2">Пароль</label>
          <div class="relative">
            <input 
              v-model="password" 
              type="password" 
              required
              class="w-full px-5 py-4 pl-12 rounded-xl bg-dark-surface/50 border border-dark-border text-white placeholder-gray-500 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 outline-none backdrop-blur-sm"
              placeholder="••••••••"
            />
            <svg class="w-5 h-5 text-gray-500 absolute left-4 top-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
          </div>
        </div>
        
        <button 
          type="submit" 
          :disabled="loading"
          class="w-full py-4 px-4 bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 text-white rounded-xl font-bold text-lg shadow-lg shadow-primary-500/20 transition-all duration-300 focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 focus:ring-offset-dark-bg disabled:opacity-50 flex justify-center items-center hover:-translate-y-1"
        >
          <span v-if="loading" class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></span>
          {{ loading ? 'Вход в систему...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { toast } from 'vue3-toastify'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('admin@resort.com')
const password = ref('Admin123!')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  try {
    const success = await authStore.login(email.value, password.value)
    if (success) {
      toast.success('Добро пожаловать!')
      router.push('/')
    } else {
      toast.error('Неверный логин или пароль')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.animate-slow-spin {
  animation: spin 20s linear infinite;
}

.animate-slow-spin-reverse {
  animation: spin 25s linear infinite reverse;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
