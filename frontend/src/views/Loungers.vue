<template>
  <div class="page-content page-stack">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Карта Топчанов</h1>
        <p class="text-gray-400 font-medium">Интерактивная карта и управление</p>
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
      <h3 class="text-lg font-bold text-white mb-4">Управление топчанами</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Add lounger form -->
        <div>
          <h4 class="text-sm font-bold text-gray-300 mb-3">Добавить топчан</h4>
          <form @submit.prevent="addLounger" class="space-y-3">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-semibold text-gray-400 mb-1">Номер</label>
                <input v-model="newLounger.number" required type="text" placeholder="T-1" class="w-full px-3 py-2.5 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-purple-500">
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-400 mb-1">Зона</label>
                <select v-model="newLounger.zone" class="w-full px-3 py-2.5 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-purple-500">
                  <option value="main">Основная</option>
                  <option value="vip">VIP</option>
                  <option value="kids">Детская</option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-400 mb-1">Цена за час (₸)</label>
              <input v-model.number="newLounger.price_per_hour" required type="number" min="0" placeholder="3000" class="w-full px-3 py-2.5 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-purple-500">
            </div>
            <button type="submit" class="w-full py-2.5 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white rounded-xl font-bold text-sm shadow-lg transition-all">
              Добавить топчан
            </button>
          </form>
        </div>

        <!-- Lounger list for deletion -->
        <div>
          <h4 class="text-sm font-bold text-gray-300 mb-3">Список топчанов ({{ loungers.length }})</h4>
          <div class="space-y-2 max-h-64 overflow-y-auto custom-scrollbar pr-1">
            <div
              v-for="l in loungers"
              :key="l.id"
              class="flex items-center justify-between p-3 bg-dark-bg border border-dark-border/50 rounded-xl"
            >
              <div>
                <span class="text-white font-bold text-sm">{{ l.number }}</span>
                <span class="text-gray-500 text-xs ml-2">{{ l.zone }} · {{ l.price_per_hour }} ₸/ч</span>
              </div>
              <button
                @click="deleteLounger(l)"
                class="p-1.5 text-red-400/60 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                title="Удалить"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              </button>
            </div>
            <div v-if="loungers.length === 0" class="text-center py-6 text-gray-500 text-sm">
              Топчаны не добавлены
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lounger Map -->
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

      <div class="grid grid-cols-2 min-[400px]:grid-cols-3 sm:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
        <div
          v-for="lounger in loungers"
          :key="lounger.id"
          @click="handleLoungerClick(lounger)"
          class="aspect-square rounded-2xl border flex flex-col items-center justify-center cursor-pointer transition-all duration-300 hover:scale-105 shadow-lg group relative overflow-hidden p-2 text-center"
          :class="{
            'bg-green-500/10 border-green-500/30 text-green-400 hover:bg-green-500/20': lounger.status === 'free',
            'bg-red-500/10 border-red-500/30 text-red-400 hover:bg-red-500/20': lounger.status === 'occupied',
            'bg-yellow-500/10 border-yellow-500/30 text-yellow-400 hover:bg-yellow-500/20': lounger.status === 'reserved',
          }"
        >
          <div class="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <h3 class="text-2xl font-black mb-0.5 z-10">{{ lounger.number }}</h3>
          <span class="text-[10px] font-bold uppercase tracking-wider opacity-70 z-10 mb-1">{{ lounger.zone }}</span>
          
          <div v-if="lounger.status === 'reserved' && lounger.reservation_time" class="text-[10px] font-black z-10 text-yellow-300 mb-4 truncate w-full max-w-[90%]">
            Бронь: {{ lounger.reservation_time }}
          </div>
          <div v-else class="h-4"></div>

          <div class="absolute bottom-2 font-medium text-[10px] z-10 opacity-70">{{ lounger.price_per_hour }} ₸/ч</div>
        </div>
      </div>

      <div v-if="loungers.length === 0" class="text-center py-20 text-gray-500">
        Нет добавленных топчанов. Откройте «Настройки» чтобы добавить.
      </div>
    </div>

    <!-- Lounger Action Modal -->
    <div v-if="selectedLounger" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-sm w-full shadow-2xl relative text-white">
        <button @click="selectedLounger = null; showBookingTimePrompt = false; bookingTimeInput = ''" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>

        <div class="mb-1 text-xs font-bold text-gray-500 uppercase tracking-widest">
          Топчан / Зона: {{ selectedLounger.zone }}
        </div>
        <h3 class="text-2xl font-black text-white mb-1">{{ selectedLounger.number }}</h3>
        <p class="text-gray-400 text-sm mb-5">{{ selectedLounger.price_per_hour.toLocaleString() }} ₸/час</p>

        <!-- FREE: Rent or Reserve -->
        <div v-if="selectedLounger.status === 'free'" class="space-y-3">
          <div v-if="!showBookingTimePrompt" class="space-y-3">
            <button @click="changeStatus(selectedLounger.id, 'occupied'); selectedLounger = null" class="w-full py-4 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white rounded-xl font-bold shadow-lg transition-all">
              Сдать в аренду
            </button>
            <button @click="showBookingTimePrompt = true" class="w-full py-3 bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500/30 rounded-xl font-bold text-sm transition-all">
              Забронировать
            </button>
          </div>
          <div v-else class="space-y-3 p-3 bg-white/5 border border-dark-border rounded-2xl">
            <label class="block text-xs font-semibold text-gray-300 mb-1">Время / Имя для брони</label>
            <input v-model="bookingTimeInput" type="text" placeholder="Например: 19:00 (Иван)" class="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-purple-500">
            <div class="grid grid-cols-2 gap-2 mt-2">
              <button @click="showBookingTimePrompt = false; bookingTimeInput = ''" class="py-2 bg-dark-surface border border-dark-border text-gray-400 hover:text-white rounded-xl text-xs font-bold transition-all">
                Отмена
              </button>
              <button @click="changeStatus(selectedLounger.id, 'reserved', bookingTimeInput); selectedLounger = null; showBookingTimePrompt = false; bookingTimeInput = ''" class="py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl text-xs font-bold transition-all">
                Подтвердить
              </button>
            </div>
          </div>
        </div>

        <!-- OCCUPIED: vacate -->
        <div v-else-if="selectedLounger.status === 'occupied'" class="space-y-4">
          <p class="text-center text-red-400 text-sm py-2 font-bold">Топчан занят клиентом</p>
          <button @click="changeStatus(selectedLounger.id, 'free'); selectedLounger = null" class="w-full py-4 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white rounded-xl font-bold shadow-lg transition-all">
            Освободить топчан
          </button>
        </div>

        <!-- RESERVED -->
        <div v-else class="space-y-3">
          <p class="text-center text-gray-400 text-sm py-2">Топчан забронирован</p>
          <div v-if="selectedLounger.reservation_time" class="p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-xl text-center text-yellow-400 text-sm font-bold">
            Время брони: {{ selectedLounger.reservation_time }}
          </div>
          <button @click="changeStatus(selectedLounger.id, 'free'); selectedLounger = null" class="w-full py-3 bg-green-500/20 text-green-400 hover:bg-green-500/30 rounded-xl font-bold text-sm transition-all">
            Освободить
          </button>
          <button @click="changeStatus(selectedLounger.id, 'occupied'); selectedLounger = null" class="w-full py-3 bg-purple-500/20 text-purple-400 hover:bg-purple-500/30 rounded-xl font-bold text-sm transition-all">
            Сдать в аренду
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'
import { XMarkIcon as XIcon } from '@heroicons/vue/24/solid'

const loungers = ref([])
const showSettings = ref(false)
const selectedLounger = ref(null)
const showBookingTimePrompt = ref(false)
const bookingTimeInput = ref('')

const newLounger = ref({
  number: '',
  zone: 'main',
  price_per_hour: 3000
})

const fetchLoungers = async () => {
  try {
    const res = await api.get('/loungers/')
    loungers.value = res.data
  } catch (err) { console.error(err) }
}

onMounted(() => fetchLoungers())

const addLounger = async () => {
  try {
    await api.post('/loungers/', newLounger.value)
    toast.success(`Топчан ${newLounger.value.number} добавлен`)
    newLounger.value = { number: '', zone: 'main', price_per_hour: 3000 }
    fetchLoungers()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка добавления')
  }
}

const deleteLounger = async (lounger) => {
  if (!confirm(`Удалить топчан ${lounger.number}?`)) return
  try {
    await api.delete(`/loungers/${lounger.id}`)
    toast.success(`Топчан ${lounger.number} удалён`)
    fetchLoungers()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка удаления')
  }
}

const handleLoungerClick = (lounger) => {
  selectedLounger.value = { ...lounger }
  showBookingTimePrompt.value = false
  bookingTimeInput.value = ''
}

const changeStatus = async (loungerId, status, reservationTime = '') => {
  try {
    let url = `/loungers/${loungerId}/status?status=${status}`
    if (status === 'reserved' && reservationTime) {
      url += `&reservation_time=${encodeURIComponent(reservationTime)}`
    }
    await api.post(url)
    fetchLoungers()
  } catch (err) {
    toast.error('Ошибка изменения статуса')
  }
}
</script>
