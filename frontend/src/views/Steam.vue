<template>
  <div class="page-content page-stack">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Бани & VIP Кабины</h1>
        <p class="text-gray-400 font-medium">Интерактивная карта и управление арендой</p>
      </div>
      <button
        @click="showSettings = !showSettings"
        class="px-5 py-2.5 bg-dark-surface border border-dark-border hover:bg-white/5 text-gray-300 rounded-xl font-bold text-sm transition-all flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><circle cx="12" cy="12" r="3"></circle></svg>
        Настройки
      </button>
    </div>

    <!-- Settings Panel -->
    <div v-if="showSettings" class="glass-dark border border-dark-border rounded-3xl p-6">
      <h3 class="text-lg font-bold text-white mb-4">Управление залами</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Add room form -->
        <div>
          <h4 class="text-sm font-bold text-gray-300 mb-3">Добавить зал</h4>
          <form @submit.prevent="addRoom" class="space-y-3">
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">Название</label>
              <input v-model="newRoom.name" required type="text" placeholder="Хамам Люкс" class="w-full px-3 py-2.5 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-orange-500">
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-gray-400 mb-1">Тип</label>
                <select v-model="newRoom.room_type" class="w-full px-3 py-2.5 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-orange-500">
                  <option value="steam_room">Баня / Сауна</option>
                  <option value="vip_cabin">VIP Кабина</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-400 mb-1">Цена за час (₸)</label>
                <input v-model.number="newRoom.price_per_hour" required type="number" min="0" placeholder="5000" class="w-full px-3 py-2.5 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-orange-500">
              </div>
            </div>
            <button type="submit" class="w-full py-2.5 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold text-sm shadow-lg transition-all">
              Добавить зал
            </button>
          </form>
        </div>

        <!-- Room list for deletion -->
        <div>
          <h4 class="text-sm font-bold text-gray-300 mb-3">Список залов ({{ rooms.length }})</h4>
          <div class="space-y-2 max-h-64 overflow-y-auto custom-scrollbar pr-1">
            <div
              v-for="r in rooms"
              :key="r.id"
              class="flex items-center justify-between p-3 bg-dark-bg border border-dark-border/50 rounded-xl"
            >
              <div>
                <span class="text-white font-bold text-sm">{{ r.name }}</span>
                <span class="text-gray-500 text-xs ml-2">{{ r.room_type === 'steam_room' ? 'Баня' : 'VIP' }} · {{ r.price_per_hour.toLocaleString() }} ₸/ч</span>
              </div>
              <button
                @click="deleteRoom(r)"
                :disabled="r.status === 'occupied'"
                class="p-1.5 text-red-400/60 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors disabled:opacity-30 disabled:pointer-events-none"
                title="Удалить"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              </button>
            </div>
            <div v-if="rooms.length === 0" class="text-center py-6 text-gray-500 text-sm">
              Залы не добавлены
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex items-center gap-6 flex-wrap">
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
      <div class="flex items-center gap-2">
        <div class="w-4 h-4 rounded-full bg-gray-500/20 border border-gray-500/50"></div>
        <span class="text-sm text-gray-300">Обслуживание</span>
      </div>
    </div>

    <!-- Rooms Map -->
    <div class="glass-dark p-6 sm:p-8 rounded-3xl border border-dark-border shadow-lg shadow-black/20">
      <div class="grid grid-cols-1 min-[360px]:grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-4">
        <div
          v-for="room in rooms"
          :key="room.id"
          class="rounded-2xl border flex flex-col items-center justify-center cursor-pointer transition-all duration-300 hover:scale-105 shadow-lg group relative overflow-hidden p-4 min-h-[120px]"
          :class="{
            'bg-green-500/10 border-green-500/30 text-green-400 hover:bg-green-500/20': room.status === 'free',
            'bg-red-500/10 border-red-500/30 text-red-400 hover:bg-red-500/20': room.status === 'occupied',
            'bg-yellow-500/10 border-yellow-500/30 text-yellow-400 hover:bg-yellow-500/20': room.status === 'reserved',
            'bg-gray-500/10 border-gray-500/30 text-gray-400 hover:bg-gray-500/20': room.status === 'maintenance',
          }"
          @click="handleRoomClick(room)"
        >
          <div class="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>

          <!-- Type badge -->
          <span class="text-[10px] font-bold uppercase tracking-widest opacity-60 z-10 mb-1 flex items-center gap-1">
            <component :is="room.room_type === 'steam_room' ? FireIcon : SparklesIcon" class="w-3 h-3" :class="room.room_type === 'steam_room' ? 'text-orange-400' : 'text-yellow-400'"/>
            <span>{{ room.room_type === 'steam_room' ? 'Баня' : 'VIP' }}</span>
          </span>

          <!-- Name -->
          <h3 class="text-sm font-black text-white text-center leading-tight z-10 mb-2">{{ room.name }}</h3>

          <!-- Timer if occupied -->
          <div v-if="room.status === 'occupied'" class="text-xs font-mono font-black z-10 text-red-300">
            {{ getElapsedTime(room.current_occupancy_start) }}
          </div>

          <!-- Price -->
          <div class="text-xs font-bold z-10 mt-1 opacity-70">{{ room.price_per_hour.toLocaleString() }} ₸/ч</div>

          <!-- Status dot -->
          <div class="absolute top-2 right-2 w-2 h-2 rounded-full z-10 animate-pulse"
            :class="{
              'bg-green-400': room.status === 'free',
              'bg-red-400': room.status === 'occupied',
              'bg-yellow-400': room.status === 'reserved',
              'bg-gray-400': room.status === 'maintenance',
            }">
          </div>
        </div>
      </div>

      <div v-if="rooms.length === 0" class="text-center py-20 text-gray-500">
        Нет добавленных залов. Откройте «Настройки» чтобы добавить.
      </div>
    </div>

    <!-- Room Action Modal (click on room) -->
    <div v-if="selectedRoom" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-sm w-full shadow-2xl relative">
        <button @click="selectedRoom = null" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>

        <div class="mb-1 text-xs font-bold text-gray-500 uppercase tracking-widest">
          {{ selectedRoom.room_type === 'steam_room' ? 'Баня / Сауна' : 'VIP Кабина' }}
        </div>
        <h3 class="text-2xl font-black text-white mb-1">{{ selectedRoom.name }}</h3>
        <p class="text-gray-400 text-sm mb-5">{{ selectedRoom.price_per_hour.toLocaleString() }} ₸/час</p>

        <!-- FREE: start rental -->
        <div v-if="selectedRoom.status === 'free'" class="space-y-3">
          <button @click="occupyRoom(selectedRoom)" class="w-full py-4 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold shadow-lg transition-all">
            Сдать в аренду
          </button>
          <div class="grid grid-cols-2 gap-2">
            <button @click="changeStatus(selectedRoom.id, 'reserved'); selectedRoom = null" class="py-2.5 bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500/30 rounded-xl font-bold text-sm transition-all">
              Забронировать
            </button>
            <button @click="changeStatus(selectedRoom.id, 'maintenance'); selectedRoom = null" class="py-2.5 bg-gray-500/20 text-gray-400 hover:bg-gray-500/30 rounded-xl font-bold text-sm transition-all">
              Обслуживание
            </button>
          </div>
        </div>

        <!-- OCCUPIED: show timer + checkout -->
        <div v-else-if="selectedRoom.status === 'occupied'" class="space-y-4">
          <div class="p-4 bg-black/20 border border-white/5 rounded-2xl text-center">
            <p class="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">Время аренды</p>
            <p class="text-3xl font-black text-orange-400 font-mono">{{ getElapsedTime(selectedRoom.current_occupancy_start) }}</p>
            <p class="text-xs text-gray-400 mt-1">Начало: {{ formatTime(selectedRoom.current_occupancy_start) }}</p>
          </div>
          <button @click="openCheckout(selectedRoom)" class="w-full py-4 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white rounded-xl font-bold shadow-lg transition-all">
            Освободить & Оплатить
          </button>
        </div>

        <!-- RESERVED / MAINTENANCE -->
        <div v-else class="space-y-3">
          <p class="text-center text-gray-400 text-sm py-2">
            {{ selectedRoom.status === 'reserved' ? 'Зал забронирован' : 'Зал на обслуживании' }}
          </p>
          <button @click="changeStatus(selectedRoom.id, 'free'); selectedRoom = null" class="w-full py-3 bg-green-500/20 text-green-400 hover:bg-green-500/30 rounded-xl font-bold text-sm transition-all">
            Освободить
          </button>
          <button v-if="selectedRoom.status === 'reserved'" @click="occupyRoom(selectedRoom)" class="w-full py-3 bg-orange-500/20 text-orange-400 hover:bg-orange-500/30 rounded-xl font-bold text-sm transition-all">
            Сдать в аренду
          </button>
        </div>
      </div>
    </div>

    <!-- Checkout / Payment Modal -->
    <div v-if="checkoutRoom" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div class="glass-dark border border-dark-border rounded-3xl p-8 max-w-sm w-full shadow-2xl relative text-white">
        <button @click="checkoutRoom = null" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>

        <h3 class="text-2xl font-black mb-1">Оплата аренды</h3>
        <p class="text-gray-400 text-sm mb-5">{{ checkoutRoom.name }}</p>

        <div class="p-4 bg-white/5 rounded-2xl mb-2 flex justify-between items-center">
          <span class="text-gray-300 font-semibold text-sm">Начало:</span>
          <span class="text-white font-bold">{{ formatTime(checkoutRoom.current_occupancy_start) }}</span>
        </div>
        <div class="p-4 bg-white/5 rounded-2xl mb-5 flex justify-between items-center">
          <span class="text-gray-300 font-semibold text-sm">Время:</span>
          <span class="text-orange-400 font-black text-xl font-mono">{{ getElapsedTime(checkoutRoom.current_occupancy_start) }}</span>
        </div>

        <p class="text-sm font-semibold text-gray-300 mb-3">Способ оплаты:</p>
        <div class="grid grid-cols-2 gap-3 mb-5">
          <button
            @click="selectedPayment = 'cash'"
            class="py-4 rounded-2xl border-2 font-bold text-sm transition-all flex flex-col items-center gap-2"
            :class="selectedPayment === 'cash' ? 'border-emerald-500 bg-emerald-500/20 text-emerald-400' : 'border-dark-border bg-white/5 text-gray-400 hover:border-gray-500'"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            Наличные
          </button>
          <button
            @click="selectedPayment = 'kaspi'"
            class="py-4 rounded-2xl border-2 font-bold text-sm transition-all flex flex-col items-center gap-2"
            :class="selectedPayment === 'kaspi' ? 'border-orange-500 bg-orange-500/20 text-orange-400' : 'border-dark-border bg-white/5 text-gray-400 hover:border-gray-500'"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
            Каспий
          </button>
        </div>

        <button @click="confirmCheckout" class="w-full py-4 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white rounded-xl font-bold shadow-lg transition-all">
          Подтвердить оплату
        </button>
      </div>
    </div>

    <!-- Invoice Modal (after checkout) -->
    <div v-if="invoice" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div class="glass-dark border border-dark-border rounded-3xl p-8 max-w-md w-full shadow-2xl relative text-white">
        <div class="text-center mb-6">
          <div class="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </div>
          <h3 class="text-2xl font-black">Аренда завершена</h3>
        </div>

        <div class="space-y-3 border-t border-b border-dark-border/50 py-4 mb-6">
          <div class="flex justify-between text-sm">
            <span class="text-gray-400">Объект:</span>
            <span class="text-white font-bold">{{ invoice.room_name }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-400">Тариф:</span>
            <span class="text-white font-bold">{{ invoice.price_per_hour.toLocaleString() }} ₸/час</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-400">Оплачено часов:</span>
            <span class="text-white font-bold">{{ invoice.hours_billed }} ч.</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-400">Способ оплаты:</span>
            <span class="font-bold" :class="invoice.payment_method === 'kaspi' ? 'text-orange-400' : 'text-emerald-400'">
              {{ invoice.payment_method === 'kaspi' ? 'Каспий' : 'Наличные' }}
            </span>
          </div>
          <div class="flex justify-between text-xl font-black pt-2 border-t border-dark-border/30">
            <span>Итого:</span>
            <span class="text-orange-400">{{ invoice.total_amount.toLocaleString() }} ₸</span>
          </div>
        </div>

        <button @click="invoice = null" class="w-full py-4 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold shadow-lg transition-all">
          Закрыть
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'
import { XMarkIcon as XIcon, FireIcon, SparklesIcon } from '@heroicons/vue/24/solid'

const rooms = ref([])
const showSettings = ref(false)
const selectedRoom = ref(null)
const checkoutRoom = ref(null)
const invoice = ref(null)
const selectedPayment = ref('cash')
const currentTime = ref(new Date())

const newRoom = ref({
  name: '',
  room_type: 'steam_room',
  price_per_hour: 5000
})

let timeTicker
onMounted(() => {
  fetchRooms()
  timeTicker = setInterval(() => { currentTime.value = new Date() }, 1000)
})
onUnmounted(() => clearInterval(timeTicker))

const fetchRooms = async () => {
  try {
    const res = await api.get('/steam/')
    rooms.value = res.data
  } catch (err) { console.error(err) }
}

const addRoom = async () => {
  try {
    await api.post('/steam/', newRoom.value)
    toast.success(`Зал "${newRoom.value.name}" добавлен`)
    newRoom.value = { name: '', room_type: 'steam_room', price_per_hour: 5000 }
    fetchRooms()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка добавления')
  }
}

const deleteRoom = async (room) => {
  if (!confirm(`Удалить зал "${room.name}"?`)) return
  try {
    await api.delete(`/steam/${room.id}`)
    toast.success(`Зал "${room.name}" удалён`)
    fetchRooms()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка удаления')
  }
}

const handleRoomClick = (room) => {
  selectedRoom.value = { ...room }
}

const occupyRoom = async (room) => {
  try {
    await api.post(`/steam/${room.id}/occupy`)
    toast.success(`${room.name} сдан в аренду`)
    selectedRoom.value = null
    fetchRooms()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка')
  }
}

const openCheckout = (room) => {
  checkoutRoom.value = { ...room }
  selectedRoom.value = null
  selectedPayment.value = 'cash'
}

const confirmCheckout = async () => {
  if (!checkoutRoom.value) return
  try {
    const res = await api.post(`/steam/${checkoutRoom.value.id}/checkout?payment_method=${selectedPayment.value}`)
    invoice.value = { ...res.data, payment_method: selectedPayment.value }
    toast.success('Аренда завершена')
    checkoutRoom.value = null
    fetchRooms()
  } catch (err) {
    toast.error('Ошибка при расчёте')
  }
}

const changeStatus = async (roomId, status) => {
  try {
    await api.post(`/steam/${roomId}/status?status=${status}`)
    fetchRooms()
  } catch (err) {
    toast.error('Не удалось изменить статус')
  }
}

const getElapsedTime = (startIso) => {
  if (!startIso) return '00:00:00'
  const start = new Date(startIso.endsWith('Z') ? startIso : startIso + 'Z')
  const diff = Math.max(0, currentTime.value - start)
  const h = Math.floor(diff / 3600000)
  const m = Math.floor((diff % 3600000) / 60000)
  const s = Math.floor((diff % 60000) / 1000)
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

const formatTime = (isoString) => {
  if (!isoString) return '-'
  const d = new Date(isoString.endsWith('Z') ? isoString : isoString + 'Z')
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
