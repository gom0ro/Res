<template>
  <div class="space-y-6">
    <!-- Stats Overview -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
      <div v-for="stat in stats" :key="stat.name" class="glass-dark p-6 rounded-3xl relative overflow-hidden group hover:border-primary-500/50 transition-all duration-300 hover:shadow-xl hover:shadow-primary-500/10 cursor-default hover:-translate-y-1">
        <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br opacity-10 rounded-full blur-3xl -mr-10 -mt-10 transition-transform duration-500 group-hover:scale-150" :class="stat.gradient"></div>
        <div class="flex items-center justify-between mb-4 relative z-10">
          <div class="p-3 rounded-2xl bg-white/5 text-gray-300 group-hover:bg-white/10 transition-colors">
            <component :is="stat.icon" class="w-6 h-6" />
          </div>
          <span class="flex items-center text-sm font-bold px-2 py-1 rounded-lg bg-black/20 text-green-400">
            {{ stat.change }}
            <svg class="w-4 h-4 ml-1 text-green-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg>
          </span>
        </div>
        <h3 class="text-3xl sm:text-4xl font-black text-white mb-1 tracking-tight relative z-10">{{ stat.value }}</h3>
        <p class="text-sm font-medium text-gray-400 relative z-10">{{ stat.name }}</p>
      </div>
    </div>

    <!-- Quick Actions & Active Items -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <div class="xl:col-span-2 glass-dark rounded-3xl p-6 sm:p-8 border border-dark-border shadow-lg shadow-black/20">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold text-white tracking-tight">Активные посетители в бассейне</h3>
          <router-link to="/pool" class="text-sm font-semibold text-primary-400 hover:text-primary-300 transition-colors px-3 py-1.5 rounded-lg hover:bg-primary-500/10">Все посетители</router-link>
        </div>
        
        <div class="space-y-3">
          <div 
            v-for="v in activeVisits.slice(0, 5)" 
            :key="v.id" 
            @click="$router.push('/pool')"
            class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-white/5 hover:bg-white/10 transition-colors border border-white/5 group cursor-pointer"
          >
            <div class="flex items-center gap-4 mb-3 sm:mb-0">
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500/20 to-blue-600/10 text-blue-400 flex items-center justify-center font-bold text-lg shadow-inner border border-blue-500/20 group-hover:border-blue-500/40 transition-colors">
                #{{ v.bracelet_number }}
              </div>
              <div>
                <p class="text-white font-bold text-base">{{ v.client_name || 'Неизвестный гость' }}</p>
                <p class="text-sm text-gray-400 font-medium mt-0.5">
                  Тариф: <span class="capitalize">{{ getTariffLabel(v.tariff_type) }}</span> • Вход: {{ formatTime(v.entry_time) }}
                </p>
              </div>
            </div>
            <div class="flex items-center justify-between sm:justify-end sm:text-right w-full sm:w-auto gap-4">
              <p class="text-white font-bold text-lg">{{ v.total_amount }} ₸</p>
              <span class="inline-flex items-center px-3 py-1 rounded-xl text-xs font-bold bg-blue-500/20 text-blue-400 border border-blue-500/20">
                <span class="w-1.5 h-1.5 rounded-full bg-blue-400 mr-2 animate-pulse"></span>
                В бассейне
              </span>
            </div>
          </div>

          <div v-if="activeVisits.length === 0" class="text-center py-12 text-gray-500 font-medium">
            В данный момент в бассейне нет активных посетителей.
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="glass-dark rounded-3xl p-6 sm:p-8 border border-dark-border shadow-lg shadow-black/20 flex flex-col">
        <h3 class="text-xl font-bold text-white mb-6 tracking-tight">Быстрые действия</h3>
        <div class="grid grid-cols-2 gap-4 flex-1 content-start">
          <button @click="$router.push('/pool')" class="p-5 rounded-2xl bg-gradient-to-br from-white/5 to-white/0 hover:from-primary-500/20 hover:to-primary-600/10 border border-white/10 hover:border-primary-500/30 transition-all duration-300 group flex flex-col items-center justify-center text-center gap-4 shadow-lg hover:shadow-primary-500/20 hover:-translate-y-1">
            <div class="p-3.5 bg-white/5 rounded-2xl group-hover:bg-primary-500/20 group-hover:text-primary-400 text-gray-400 transition-colors shadow-inner">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path></svg>
            </div>
            <span class="text-sm font-bold text-gray-300 group-hover:text-white">Новый гость</span>
          </button>
          
          <button @click="$router.push('/bar')" class="p-5 rounded-2xl bg-gradient-to-br from-white/5 to-white/0 hover:from-green-500/20 hover:to-green-600/10 border border-white/10 hover:border-green-500/30 transition-all duration-300 group flex flex-col items-center justify-center text-center gap-4 shadow-lg hover:shadow-green-500/20 hover:-translate-y-1">
            <div class="p-3.5 bg-white/5 rounded-2xl group-hover:bg-green-500/20 group-hover:text-green-400 text-gray-400 transition-colors shadow-inner">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
            </div>
            <span class="text-sm font-bold text-gray-300 group-hover:text-white">Новый заказ</span>
          </button>

          <button @click="$router.push('/loungers')" class="p-5 rounded-2xl bg-gradient-to-br from-white/5 to-white/0 hover:from-purple-500/20 hover:to-purple-600/10 border border-white/10 hover:border-purple-500/30 transition-all duration-300 group flex flex-col items-center justify-center text-center gap-4 shadow-lg hover:shadow-purple-500/20 hover:-translate-y-1">
            <div class="p-3.5 bg-white/5 rounded-2xl group-hover:bg-purple-500/20 group-hover:text-purple-400 text-gray-400 transition-colors shadow-inner">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
            </div>
            <span class="text-sm font-bold text-gray-300 group-hover:text-white">Бронь топчана</span>
          </button>

          <button @click="$router.push('/steam')" class="p-5 rounded-2xl bg-gradient-to-br from-white/5 to-white/0 hover:from-yellow-500/20 hover:to-yellow-600/10 border border-white/10 hover:border-yellow-500/30 transition-all duration-300 group flex flex-col items-center justify-center text-center gap-4 shadow-lg hover:shadow-yellow-500/20 hover:-translate-y-1">
            <!-- Dynamic Fire/Steam room icon -->
            <div class="p-3.5 bg-white/5 rounded-2xl group-hover:bg-yellow-500/20 group-hover:text-yellow-400 text-gray-400 transition-colors shadow-inner">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            </div>
            <span class="text-sm font-bold text-gray-300 group-hover:text-white">Бани & VIP</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../stores/auth'
import { 
  CurrencyDollarIcon, 
  UserGroupIcon, 
  MapIcon, 
  ShoppingCartIcon 
} from '@heroicons/vue/24/outline'

const stats = ref([
  { name: 'Выручка за сегодня', value: '45 000 ₸', icon: CurrencyDollarIcon, change: '12%', changeType: 'increase', gradient: 'from-green-500 to-green-600', key: 'daily_revenue' },
  { name: 'Активно в бассейне', value: '0', icon: UserGroupIcon, change: '5%', changeType: 'increase', gradient: 'from-blue-500 to-blue-600', key: 'active_pool_guests' },
  { name: 'Занятость топчанов', value: '0%', icon: MapIcon, change: '2%', changeType: 'increase', gradient: 'from-purple-500 to-purple-600', key: 'loungers_occupancy' },
  { name: 'Активные заказы', value: '0', icon: ShoppingCartIcon, change: '18%', changeType: 'increase', gradient: 'from-yellow-500 to-yellow-600', key: 'active_orders' },
])

const activeVisits = ref([])

onMounted(() => {
  fetchStats()
  fetchActivePoolVisits()
})

const fetchStats = async () => {
  try {
    const res = await api.get('/dashboard/stats')
    // Map response keys directly to update the reactive values
    stats.value.forEach(stat => {
      if (res.data[stat.key] !== undefined) {
        stat.value = res.data[stat.key]
      }
    })
  } catch (err) {
    console.error("Error loading dashboard stats", err)
  }
}

const fetchActivePoolVisits = async () => {
  try {
    const res = await api.get('/pool/')
    // Filter active visits
    activeVisits.value = res.data.filter(v => v.status === 'active')
  } catch (err) {
    console.error("Error loading active pool visits", err)
  }
}

const formatTime = (isoString) => {
  if (!isoString) return '-'
  return new Date(isoString + 'Z').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getTariffLabel = (tariff) => {
  const map = {
    'hourly': 'Часовой',
    'daily': 'Безлимит',
    'child': 'Детский',
    'vip': 'VIP'
  }
  return map[tariff] || tariff
}
</script>
