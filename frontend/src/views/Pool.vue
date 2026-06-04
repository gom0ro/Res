<template>
  <div class="page-content page-stack">
    <div class="page-toolbar">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Управление Бассейном</h1>
        <p class="text-gray-400 font-medium">Контроль посетителей, тарифов и история</p>
      </div>
      <div class="page-toolbar__actions">
      <button @click="showModal = true" class="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 text-white rounded-xl font-bold text-sm shadow-lg shadow-primary-500/20 transition-all duration-300 flex items-center justify-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        Новый посетитель
      </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">В бассейне сейчас</span>
        <h2 class="text-3xl font-black text-white mt-2">{{ activeCount }} / {{ poolCapacity }} чел.</h2>
        <div class="w-full bg-dark-bg h-2 rounded-full overflow-hidden mt-3">
          <div class="h-full bg-primary-500 rounded-full transition-all" :style="{ width: `${Math.min((activeCount / poolCapacity) * 100, 100)}%` }"></div>
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
        <h2 class="text-3xl font-black text-orange-400 mt-2">{{ totalRevenueToday.toLocaleString() }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold mt-2">С закрытых браслетов</span>
      </div>
    </div>

    <!-- Tariff Cards -->
    <div class="grid grid-cols-1 min-[360px]:grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
      <div v-for="t in tariffs" :key="t.key" class="glass-dark border border-dark-border rounded-2xl p-4 flex flex-col gap-1">
        <span class="text-xs font-bold uppercase tracking-widest" :class="t.color">{{ t.label }}</span>
        <span class="text-2xl font-black text-white">{{ t.price.toLocaleString() }} ₸</span>
        <span class="text-xs text-gray-500">фиксированная цена</span>
      </div>
    </div>

    <!-- Active Visitors Table -->
    <div class="glass-dark rounded-3xl border border-dark-border shadow-lg shadow-black/20 overflow-hidden">
      <div class="p-6 border-b border-dark-border flex justify-between items-center bg-white/5">
        <h3 class="text-xl font-bold text-white tracking-tight">Активные браслеты ({{ activeCount }})</h3>
      </div>
      <div class="table-wrap custom-scrollbar">
        <table class="w-full text-left text-sm text-gray-400 whitespace-nowrap">
          <thead class="text-xs text-gray-500 uppercase font-bold bg-dark-surface/50">
            <tr>
              <th class="px-6 py-4">Браслет #</th>
              <th class="px-6 py-4">Клиент</th>
              <th class="px-6 py-4">Тариф</th>
              <th class="px-6 py-4">Вход</th>
              <th class="px-6 py-4">Время в бассейне</th>
              <th class="px-6 py-4 text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="v in activeVisits" :key="v.id" class="border-b border-dark-border/50 hover:bg-white/5 transition-colors">
              <td class="px-6 py-5 font-black text-white text-base">#{{ v.bracelet_number }}</td>
              <td class="px-6 py-5">
                <div class="text-white font-bold">{{ v.client_name || 'Не указан' }}</div>
              </td>
              <td class="px-6 py-5">
                <span class="px-2 py-1 rounded-lg text-xs font-bold" :class="getTariffBadge(v.tariff_type)">
                  {{ getTariffLabel(v.tariff_type) }}
                </span>
              </td>
              <td class="px-6 py-5">{{ formatTime(v.entry_time) }}</td>
              <td class="px-6 py-5 font-bold text-blue-400 font-mono">
                {{ getElapsed(v.entry_time) }}
              </td>
              <td class="px-6 py-5 text-right">
                <button @click="openCheckout(v)" class="px-4 py-2 bg-green-500/20 text-green-400 hover:bg-green-500 hover:text-white font-bold rounded-lg transition-colors">
                  Завершить ({{ v.total_amount.toLocaleString() }} ₸)
                </button>
              </td>
            </tr>
            <tr v-if="activeVisits.length === 0">
              <td colspan="6" class="px-6 py-10 text-center text-gray-500">Нет активных посетителей</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Visitor Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-md w-full shadow-2xl relative">
        <button @click="showModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>
        <h3 class="text-2xl font-bold text-white mb-6">Новый посетитель</h3>
        <form @submit.prevent="createVisit" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Номер браслета</label>
            <input v-model="form.bracelet_number" required type="text" placeholder="001" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Имя клиента (необязательно)</label>
            <input v-model="form.client_name" type="text" placeholder="Иван Иванов" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
          </div>

          <!-- Tariff selection cards -->
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-3">Тариф</label>
            <div class="grid grid-cols-2 gap-3">
              <button
                v-for="t in tariffs" :key="t.key"
                type="button"
                @click="form.tariff_type = t.key"
                class="p-4 rounded-2xl border-2 text-left transition-all"
                :class="form.tariff_type === t.key
                  ? 'border-primary-500 bg-primary-500/20'
                  : 'border-dark-border bg-white/5 hover:border-gray-500'"
              >
                <div class="font-black text-white text-lg">{{ t.price.toLocaleString() }} ₸</div>
                <div class="text-sm font-bold mt-0.5" :class="t.color">{{ t.label }}</div>
              </button>
            </div>
          </div>

          <!-- Price preview -->
          <div class="p-4 bg-primary-500/10 border border-primary-500/20 rounded-xl flex justify-between items-center">
            <span class="text-gray-300 font-semibold">К оплате:</span>
            <span class="text-primary-400 font-black text-xl">{{ selectedTariffPrice.toLocaleString() }} ₸</span>
          </div>

          <button type="submit" class="w-full py-3 bg-primary-600 hover:bg-primary-500 text-white rounded-xl font-bold shadow-lg transition-colors">
            Выдать браслет
          </button>
        </form>
      </div>
    </div>

    <!-- Checkout / Payment Modal -->
    <div v-if="checkoutVisit" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-sm w-full shadow-2xl relative">
        <button @click="checkoutVisit = null" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>
        <h3 class="text-2xl font-bold text-white mb-1">Оплата</h3>
        <p class="text-gray-400 text-sm mb-1">Браслет #{{ checkoutVisit.bracelet_number }}</p>
        <p class="text-gray-400 text-sm mb-5">{{ checkoutVisit.client_name || 'Гость' }} · {{ getTariffLabel(checkoutVisit.tariff_type) }} · {{ getElapsed(checkoutVisit.entry_time) }}</p>

        <div class="p-4 bg-white/5 rounded-2xl mb-6 flex justify-between items-center">
          <span class="text-gray-300 font-semibold">Сумма:</span>
          <span class="text-white font-black text-2xl">{{ checkoutVisit.total_amount.toLocaleString() }} ₸</span>
        </div>

        <p class="text-sm font-semibold text-gray-300 mb-3">Способ оплаты:</p>
        <div class="grid grid-cols-2 gap-3 mb-6">
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'
import { XMarkIcon as XIcon } from '@heroicons/vue/24/solid'

const visits = ref([])
const showModal = ref(false)
const now = ref(new Date())
const checkoutVisit = ref(null)
const selectedPayment = ref('cash')

const tariffs = [
  { key: 'adult',  label: 'Взрослый', price: 2000,  color: 'text-blue-400' },
  { key: 'child',  label: 'Детский',  price: 1000,  color: 'text-green-400' },
]

const form = ref({
  bracelet_number: '',
  client_name: '',
  tariff_type: 'adult',
  expected_hours: 1
})

const selectedTariffPrice = computed(() => {
  return tariffs.find(t => t.key === form.value.tariff_type)?.price || 0
})

const poolCapacity = ref(100)
const activeVisits = computed(() => visits.value.filter(v => v.status === 'active'))
const activeCount = computed(() => activeVisits.value.length)
const availableSlots = computed(() => Math.max(0, poolCapacity.value - activeCount.value))

const totalToday = computed(() => {
  const today = new Date().toDateString()
  return visits.value.filter(v => new Date(v.entry_time + 'Z').toDateString() === today).length
})

const totalRevenueToday = computed(() => {
  const today = new Date().toDateString()
  return visits.value
    .filter(v => new Date(v.entry_time + 'Z').toDateString() === today && v.is_paid)
    .reduce((acc, v) => acc + (v.total_amount || 0), 0)
})

let timer
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
    await api.post('/pool/', {
      bracelet_number: form.value.bracelet_number,
      client_name: form.value.client_name,
      tariff_type: form.value.tariff_type,
      expected_hours: 1
    })
    showModal.value = false
    form.value = { bracelet_number: '', client_name: '', tariff_type: 'adult', expected_hours: 1 }
    toast.success('Браслет выдан')
    fetchVisits()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка')
  }
}

const openCheckout = (visit) => {
  checkoutVisit.value = visit
  selectedPayment.value = 'cash'
}

const confirmCheckout = async () => {
  if (!checkoutVisit.value) return
  try {
    await api.post(`/pool/${checkoutVisit.value.id}/checkout?payment_method=${selectedPayment.value}`)
    toast.success('Оплата принята')
    checkoutVisit.value = null
    fetchVisits()
  } catch (err) {
    toast.error('Ошибка при оплате')
  }
}

const getTariffLabel = (tariff) => {
  const map = { adult: 'Взрослый', child: 'Детский', daily: 'Безлимит', vip: 'VIP', hourly: 'Часовой' }
  return map[tariff] || tariff
}

const getTariffBadge = (tariff) => {
  const map = {
    adult: 'bg-blue-500/20 text-blue-400',
    child: 'bg-green-500/20 text-green-400',
    daily: 'bg-purple-500/20 text-purple-400',
    vip: 'bg-yellow-500/20 text-yellow-400',
    hourly: 'bg-gray-500/20 text-gray-400'
  }
  return map[tariff] || 'bg-gray-500/20 text-gray-400'
}

const formatTime = (isoString) => {
  if (!isoString) return '-'
  return new Date(isoString + 'Z').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getElapsed = (entryIso) => {
  if (!entryIso) return '-'
  const entry = new Date(entryIso + 'Z')
  const diff = Math.max(0, now.value - entry)
  const h = Math.floor(diff / 3600000)
  const m = Math.floor((diff % 3600000) / 60000)
  const s = Math.floor((diff % 60000) / 1000)
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}
</script>
