<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Карта Топчанов</h1>
        <p class="text-gray-400 font-medium">Интерактивная карта и управление бронью</p>
      </div>
      <button @click="seedLoungers" class="px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white rounded-xl font-bold text-sm shadow-lg shadow-purple-500/20 transition-all">
        Сгенерировать топчаны
      </button>
    </div>
    
    <div class="glass-dark p-6 sm:p-10 rounded-3xl border border-dark-border shadow-lg shadow-black/20">
       <div class="flex items-center gap-6 mb-8">
          <div class="flex items-center gap-2">
            <div class="w-4 h-4 rounded-full bg-green-500/20 border border-green-500/50"></div>
            <span class="text-sm text-gray-300">Свободен</span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-4 h-4 rounded-full bg-red-500/20 border border-red-500/50"></div>
            <span class="text-sm text-gray-300">Занят</span>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-4 h-4 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
            <span class="text-sm text-gray-300">Забронирован</span>
          </div>
       </div>

       <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-4">
         <div 
           v-for="lounger in loungers" 
           :key="lounger.id"
           @click="toggleStatus(lounger)"
           class="aspect-square rounded-2xl border flex flex-col items-center justify-center cursor-pointer transition-all duration-300 hover:scale-105 shadow-lg group relative overflow-hidden"
           :class="{
             'bg-green-500/10 border-green-500/30 text-green-400 hover:bg-green-500/20': lounger.status === 'free',
             'bg-red-500/10 border-red-500/30 text-red-400 hover:bg-red-500/20': lounger.status === 'occupied',
             'bg-yellow-500/10 border-yellow-500/30 text-yellow-400 hover:bg-yellow-500/20': lounger.status === 'reserved',
           }"
         >
            <div class="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <h3 class="text-2xl font-black mb-1 z-10">{{ lounger.number }}</h3>
            <span class="text-xs font-bold uppercase tracking-wider opacity-70 z-10">{{ lounger.zone }}</span>
            
            <div class="absolute bottom-2 font-medium text-xs z-10">
              {{ lounger.price_per_hour }} ₸/час
            </div>
         </div>
       </div>
       
       <div v-if="loungers.length === 0" class="text-center py-20 text-gray-500">
         Нет добавленных топчанов. Нажмите "Сгенерировать топчаны".
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'

const loungers = ref([])

const fetchLoungers = async () => {
  try {
    const res = await api.get('/loungers/')
    loungers.value = res.data
  } catch (err) { console.error(err) }
}

onMounted(() => fetchLoungers())

const seedLoungers = async () => {
  try {
    await api.post('/loungers/seed')
    toast.success('Топчаны добавлены!')
    fetchLoungers()
  } catch (err) { toast.error('Ошибка') }
}

const toggleStatus = async (lounger) => {
  const nextStatus = {
    'free': 'occupied',
    'occupied': 'reserved',
    'reserved': 'free'
  }[lounger.status] || 'free';
  
  try {
    await api.post(`/loungers/${lounger.id}/status?status=${nextStatus}`)
    lounger.status = nextStatus
    toast.success(`${lounger.number} теперь ${nextStatus}`)
  } catch (err) { toast.error('Ошибка изменения статуса') }
}
</script>
