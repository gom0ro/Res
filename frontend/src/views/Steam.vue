<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Бани & VIP Кабины</h1>
        <p class="text-gray-400 font-medium">Контроль аренды саун, хамама и VIP-зон в реальном времени</p>
      </div>
      <button @click="seedRooms" class="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-orange-600 to-red-500 hover:from-orange-500 hover:to-red-400 text-white rounded-xl font-bold text-sm shadow-lg shadow-orange-500/20 transition-all duration-300 flex items-center justify-center gap-2 hover:-translate-y-0.5">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 7.89H18"></path></svg>
        Инициализировать залы
      </button>
    </div>

    <!-- Rooms Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div 
        v-for="room in rooms" 
        :key="room.id" 
        class="glass-dark rounded-3xl border border-dark-border p-6 flex flex-col justify-between relative overflow-hidden group hover:border-orange-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-orange-500/5"
      >
        <!-- Top row -->
        <div>
          <div class="flex justify-between items-start mb-4">
            <span 
              class="px-3 py-1 rounded-xl text-xs font-bold uppercase tracking-wider"
              :class="{
                'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20': room.status === 'free',
                'bg-red-500/10 text-red-400 border border-red-500/20': room.status === 'occupied',
                'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20': room.status === 'reserved',
                'bg-gray-500/10 text-gray-400 border border-gray-500/20': room.status === 'maintenance'
              }"
            >
              <span class="inline-block w-2 h-2 rounded-full mr-1.5 animate-pulse" :class="{
                'bg-emerald-400': room.status === 'free',
                'bg-red-400': room.status === 'occupied',
                'bg-yellow-400': room.status === 'reserved',
                'bg-gray-400': room.status === 'maintenance'
              }"></span>
              {{ getStatusLabel(room.status) }}
            </span>
            <span class="text-sm font-bold text-gray-500 uppercase tracking-widest">{{ room.room_type === 'steam_room' ? 'Баня / Сауна' : 'VIP Кабина' }}</span>
          </div>

          <h3 class="text-2xl font-black text-white mb-2 leading-tight tracking-tight">{{ room.name }}</h3>
          <p class="text-gray-400 text-sm font-medium mb-6">Стоимость: <span class="text-white font-bold">{{ room.price_per_hour }} ₸</span> в час</p>
        </div>

        <!-- Timer / Occupancy Data -->
        <div v-if="room.status === 'occupied'" class="bg-black/20 border border-white/5 rounded-2xl p-4 mb-6">
          <p class="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">Время аренды</p>
          <div class="flex justify-between items-baseline">
            <span class="text-2xl font-black text-orange-400 font-mono tracking-wider">{{ getElapsedTime(room.current_occupancy_start) }}</span>
            <span class="text-xs text-gray-400">Начало: {{ formatTime(room.current_occupancy_start) }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
          <button 
            v-if="room.status === 'free'"
            @click="occupyRoom(room)"
            class="flex-1 py-3.5 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold text-sm shadow-md transition-all duration-300"
          >
            Сдать в аренду
          </button>
          
          <button 
            v-if="room.status === 'occupied'"
            @click="checkoutRoom(room)"
            class="flex-1 py-3.5 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white rounded-xl font-bold text-sm shadow-md transition-all duration-300"
          >
            Освободить & Оплатить
          </button>

          <!-- Status Dropdown or Quick status change -->
          <div class="relative shrink-0">
            <button 
              @click="toggleActionsDropdown(room.id)" 
              class="p-3 bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white rounded-xl border border-white/5 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path></svg>
            </button>
            <div 
              v-if="activeDropdownId === room.id" 
              class="absolute right-0 bottom-full mb-2 w-48 glass-dark border border-dark-border rounded-xl shadow-2xl py-2 z-20"
            >
              <button @click="changeStatus(room.id, 'free')" class="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-emerald-400 transition-colors">Свободен</button>
              <button @click="changeStatus(room.id, 'reserved')" class="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-yellow-400 transition-colors">Забронирован</button>
              <button @click="changeStatus(room.id, 'maintenance')" class="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-red-400 transition-colors">Ремонт / Уборка</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="rooms.length === 0" class="glass-dark rounded-3xl p-20 text-center border border-dark-border shadow-lg shadow-black/20">
      <svg class="w-20 h-20 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
      <h3 class="text-xl font-bold text-white mb-2">Залы не найдены</h3>
      <p class="text-gray-400 mb-6 max-w-md mx-auto">Список пуст. Пожалуйста, проведите инициализацию для заполнения базы демонстрационными банями и VIP кабинами.</p>
      <button @click="seedRooms" class="px-6 py-3 bg-orange-600 hover:bg-orange-500 text-white font-bold rounded-xl shadow-lg transition-colors">Заполнить базу</button>
    </div>

    <!-- Checkout / Bill Modal -->
    <div v-if="checkoutInvoice" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div class="glass-dark border border-dark-border rounded-3xl p-8 max-w-md w-full shadow-2xl relative text-white">
        <button @click="checkoutInvoice = null" class="absolute top-4 right-4 text-gray-400 hover:text-white text-lg">✕</button>
        
        <div class="text-center mb-6">
          <div class="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </div>
          <h3 class="text-2xl font-black">Аренда завершена</h3>
          <p class="text-gray-400 text-sm mt-1">Чек об оплате забронированной зоны</p>
        </div>

        <div class="space-y-4 border-t border-b border-dark-border/50 py-4 mb-6 font-medium">
          <div class="flex justify-between">
            <span class="text-gray-400">Объект:</span>
            <span class="text-white font-bold">{{ checkoutInvoice.room_name }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Тариф:</span>
            <span class="text-white font-bold">{{ checkoutInvoice.price_per_hour }} ₸/час</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Вход:</span>
            <span class="text-white font-bold font-mono">{{ formatInvoiceTime(checkoutInvoice.start_time) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Выход:</span>
            <span class="text-white font-bold font-mono">{{ formatInvoiceTime(checkoutInvoice.end_time) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Оплачено часов:</span>
            <span class="text-white font-bold">{{ checkoutInvoice.hours_billed }} ч.</span>
          </div>
          <div class="h-px bg-dark-border/30 my-2"></div>
          <div class="flex justify-between text-xl font-black">
            <span>Итого к оплате:</span>
            <span class="text-orange-400">{{ checkoutInvoice.total_amount }} ₸</span>
          </div>
        </div>

        <button 
          @click="checkoutInvoice = null" 
          class="w-full py-4 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold shadow-lg shadow-orange-500/20 transition-all text-center"
        >
          Подтвердить оплату и закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'

const rooms = ref([])
const activeDropdownId = ref(null)
const checkoutInvoice = ref(null)
const currentTime = ref(new Date())

let timeTicker;
let activeDropdownTimer;

onMounted(() => {
  fetchRooms()
  timeTicker = setInterval(() => {
    currentTime.value = new Date()
  }, 1000)
  
  // Close dropdown on click outside
  window.addEventListener('click', closeDropdownHandler)
})

onUnmounted(() => {
  clearInterval(timeTicker)
  window.removeEventListener('click', closeDropdownHandler)
})

const fetchRooms = async () => {
  try {
    const res = await api.get('/steam/')
    rooms.value = res.data
  } catch (err) {
    console.error("Error fetching rooms", err)
  }
}

const seedRooms = async () => {
  try {
    await api.post('/steam/seed')
    toast.success('Залы успешно добавлены!')
    fetchRooms()
  } catch (err) {
    toast.error('Ошибка инициализации залов')
  }
}

const occupyRoom = async (room) => {
  try {
    await api.post(`/steam/${room.id}/occupy`)
    toast.success(`${room.name} сдан в аренду!`)
    fetchRooms()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка')
  }
}

const checkoutRoom = async (room) => {
  if (!confirm(`Завершить аренду зала ${room.name}?`)) return
  try {
    const res = await api.post(`/steam/${room.id}/checkout`)
    checkoutInvoice.value = res.data
    toast.success('Аренда успешно завершена')
    fetchRooms()
  } catch (err) {
    toast.error('Ошибка при расчете стоимости')
  }
}

const changeStatus = async (roomId, newStatus) => {
  try {
    await api.post(`/steam/${roomId}/status?status=${newStatus}`)
    toast.success('Статус изменен')
    activeDropdownId.value = null
    fetchRooms()
  } catch (err) {
    toast.error('Не удалось изменить статус')
  }
}

const getStatusLabel = (status) => {
  const map = {
    'free': 'Свободен',
    'occupied': 'Занят',
    'reserved': 'Забронирован',
    'maintenance': 'Обслуживание'
  }
  return map[status] || status
}

const formatTime = (isoString) => {
  if (!isoString) return '-'
  // Append Z to correctly parse as UTC
  const d = new Date(isoString.endsWith('Z') ? isoString : isoString + 'Z')
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatInvoiceTime = (isoString) => {
  if (!isoString) return '-'
  const d = new Date(isoString.endsWith('Z') ? isoString : isoString + 'Z')
  return d.toLocaleString([], { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit' })
}

const getElapsedTime = (startIso) => {
  if (!startIso) return '00:00:00'
  const start = new Date(startIso.endsWith('Z') ? startIso : startIso + 'Z')
  // Calculate difference in milliseconds
  // Account for local vs UTC conversion differences
  const diff = currentTime.value - start
  const absDiff = Math.max(0, diff)
  
  const h = Math.floor(absDiff / 3600000)
  const m = Math.floor((absDiff % 3600000) / 60000)
  const s = Math.floor((absDiff % 60000) / 1000)
  
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const toggleActionsDropdown = (id) => {
  if (activeDropdownId.value === id) {
    activeDropdownId.value = null
  } else {
    activeDropdownId.value = id
  }
}

const closeDropdownHandler = (e) => {
  if (activeDropdownId.value && !e.target.closest('.relative')) {
    activeDropdownId.value = null
  }
}
</script>

<style scoped>
/* Glassmorphism custom styles are preloaded, standard Tailwind handles the layout */
</style>
