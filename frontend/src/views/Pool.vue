<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Управление Бассейном</h1>
        <p class="text-gray-400 font-medium">Контроль посетителей, тарифов и история</p>
      </div>
      <button @click="showModal = true" class="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 text-white rounded-xl font-bold text-sm shadow-lg shadow-primary-500/20 transition-all duration-300 flex items-center justify-center gap-2 hover:-translate-y-0.5">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        Новый посетитель
      </button>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">В бассейне сейчас</span>
        <h2 class="text-3xl font-black text-white mt-2">{{ activeCount }} / {{ poolCapacity }} чел.</h2>
        <div class="w-full bg-dark-bg h-2 rounded-full overflow-hidden mt-3">
          <div class="h-full bg-primary-500 rounded-full transition-all" :style="{ width: `${(activeCount / poolCapacity) * 100}%` }"></div>
        </div>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Всего за сегодня</span>
        <h2 class="text-3xl font-black text-emerald-400 mt-2">{{ totalToday }} чел.</h2>
        <span class="text-xs text-gray-500 font-bold mt-2">Количество посещений</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Свободно мест</span>
        <h2 class="text-3xl font-black text-green-400 mt-2">{{ availableSlots }} чел.</h2>
        <span class="text-xs text-gray-500 font-bold mt-2">Доступно шкафчиков</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Выручка за сегодня</span>
        <h2 class="text-3xl font-black text-orange-400 mt-2">{{ totalRevenueToday }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold mt-2">С закрытых браслетов</span>
      </div>
    </div>

    <!-- Active Visitors Table -->
    <div class="glass-dark rounded-3xl border border-dark-border shadow-lg shadow-black/20 overflow-hidden">
      <div class="p-6 border-b border-dark-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white/5">
        <h3 class="text-xl font-bold text-white tracking-tight">Активные браслеты ({{ activeCount }})</h3>
      </div>
      <div class="overflow-x-auto custom-scrollbar">
        <table class="w-full text-left text-sm text-gray-400 whitespace-nowrap">
          <thead class="text-xs text-gray-500 uppercase font-bold bg-dark-surface/50">
            <tr>
              <th class="px-6 py-4 rounded-tl-xl">Браслет #</th>
              <th class="px-6 py-4">Клиент</th>
              <th class="px-6 py-4">Тариф</th>
              <th class="px-6 py-4">Вход</th>
              <th class="px-6 py-4">Осталось</th>
              <th class="px-6 py-4 text-right rounded-tr-xl">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="v in visits" :key="v.id" class="border-b border-dark-border/50 hover:bg-white/5 transition-colors group">
              <td class="px-6 py-5 font-black text-white text-base">#{{ v.bracelet_number }}</td>
              <td class="px-6 py-5">
                <div class="text-white font-bold">{{ v.client_name || 'Не указан' }}</div>
              </td>
              <td class="px-6 py-5 font-medium">
                <span class="px-2 py-1 bg-white/10 rounded-md">{{ v.tariff_type }}</span>
              </td>
              <td class="px-6 py-5">{{ formatTime(v.entry_time) }}</td>
              <td class="px-6 py-5 font-bold" :class="getTimeLeft(v.expected_exit_time).includes('-') ? 'text-red-400' : 'text-green-400'">
                {{ getTimeLeft(v.expected_exit_time) }}
              </td>
              <td class="px-6 py-5 text-right">
                <button v-if="v.status === 'active'" @click="checkout(v.id)" class="px-4 py-2 bg-green-500/20 text-green-400 hover:bg-green-500 hover:text-white font-bold rounded-lg transition-colors">
                  Завершить ({{ v.total_amount }} ₸)
                </button>
                <span v-else class="text-gray-500 font-bold">Оплачено</span>
              </td>
            </tr>
            <tr v-if="visits.length === 0">
              <td colspan="6" class="px-6 py-10 text-center text-gray-500">Нет активных посетителей</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-md w-full shadow-2xl relative">
        <button @click="showModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-white">✕</button>
        <h3 class="text-2xl font-bold text-white mb-6">Новый посетитель</h3>
        <form @submit.prevent="createVisit" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Номер браслета</label>
            <input v-model="form.bracelet_number" required type="text" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Имя (необязательно)</label>
            <input v-model="form.client_name" type="text" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Тариф</label>
              <select v-model="form.tariff_type" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
                <option value="hourly">Часовой</option>
                <option value="daily">Безлимит</option>
                <option value="child">Детский</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Часов</label>
              <input v-model="form.expected_hours" type="number" min="1" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
            </div>
          </div>
          <button type="submit" class="w-full py-3 bg-primary-600 hover:bg-primary-500 text-white rounded-xl font-bold shadow-lg transition-colors mt-4">Выдать браслет</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'

const visits = ref([])
const showModal = ref(false)
const now = ref(new Date())

const form = ref({
  bracelet_number: '',
  client_name: '',
  tariff_type: 'hourly',
  expected_hours: 2
})

const poolCapacity = ref(100)
const activeCount = computed(() => visits.value.filter(v => v.status === 'active').length)
const availableSlots = computed(() => Math.max(0, poolCapacity.value - activeCount.value))

const totalToday = computed(() => {
  const today = new Date().toDateString()
  return visits.value.filter(v => {
    const entryDate = new Date(v.entry_time + 'Z').toDateString()
    return entryDate === today
  }).length
})

const totalRevenueToday = computed(() => {
  const today = new Date().toDateString()
  return visits.value
    .filter(v => {
      const entryDate = new Date(v.entry_time + 'Z').toDateString()
      return entryDate === today && v.is_paid
    })
    .reduce((acc, v) => acc + (v.total_amount || 0), 0)
})

let timer;
onMounted(() => {
  fetchVisits()
  timer = setInterval(() => { now.value = new Date() }, 1000)
})
onUnmounted(() => clearInterval(timer))

const fetchVisits = async () => {
  try {
    const res = await api.get('/pool/')
    visits.value = res.data
  } catch (err) { console.error(err) }
}

const createVisit = async () => {
  try {
    await api.post('/pool/', form.value)
    showModal.value = false
    form.value = { bracelet_number: '', client_name: '', tariff_type: 'hourly', expected_hours: 2 }
    toast.success('Браслет выдан')
    fetchVisits()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка')
  }
}

const checkout = async (id) => {
  if(!confirm("Завершить посещение?")) return;
  try {
    await api.post(`/pool/${id}/checkout`)
    toast.success('Успешно оплачено')
    fetchVisits()
  } catch (err) { toast.error('Ошибка') }
}

const formatTime = (isoString) => {
  if(!isoString) return '-';
  return new Date(isoString + 'Z').toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

const getTimeLeft = (expectedExit) => {
  if(!expectedExit) return 'Безлимит';
  const exit = new Date(expectedExit + 'Z');
  const diff = exit - now.value;
  const isNegative = diff < 0;
  const absDiff = Math.abs(diff);
  
  const h = Math.floor(absDiff / 3600000);
  const m = Math.floor((absDiff % 3600000) / 60000);
  const s = Math.floor((absDiff % 60000) / 1000);
  
  const f = `${h.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
  return isNegative ? `-${f}` : f;
}
</script>
