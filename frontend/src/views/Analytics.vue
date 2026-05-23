<template>
  <div class="page-content page-stack">
    <div>
      <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Аналитика</h1>
      <p class="text-gray-400 font-medium">Сводная статистика по всем направлениям</p>
    </div>

    <!-- Period filter -->
    <div class="glass-dark border border-dark-border rounded-3xl p-4 flex flex-wrap gap-3 items-center">
      <span class="text-sm font-bold text-gray-400">Период:</span>
      <button v-for="p in periods" :key="p.key" @click="selectedPeriod = p.key; loadAll()"
        class="px-4 py-2 rounded-xl text-sm font-bold transition-all"
        :class="selectedPeriod === p.key ? 'bg-primary-600 text-white' : 'bg-white/5 text-gray-400 hover:text-white'">
        {{ p.label }}
      </button>
    </div>

    <!-- KPI cards -->
    <div class="stats-grid">
      <div class="glass-dark border border-dark-border rounded-3xl p-5">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Выручка</span>
        <h2 class="text-2xl font-black text-white mt-2">{{ stats.total.toLocaleString() }} ₸</h2>
        <span class="text-xs text-emerald-400 font-bold">Брутто</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-5">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Транзакций</span>
        <h2 class="text-2xl font-black text-white mt-2">{{ stats.count }}</h2>
        <span class="text-xs text-gray-500 font-bold">Закрытых чеков</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-5">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Ср. чек</span>
        <h2 class="text-2xl font-black text-white mt-2">{{ avgCheck.toLocaleString() }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold">На транзакцию</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-5">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Сервисный сбор</span>
        <h2 class="text-2xl font-black text-orange-400 mt-2">{{ stats.service_fee.toLocaleString() }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold">10% с заказов бара</span>
      </div>
    </div>

    <!-- Revenue by category -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="glass-dark border border-dark-border rounded-3xl p-6">
        <h3 class="text-lg font-bold text-white mb-5">Выручка по направлениям</h3>
        <div class="space-y-4">
          <div v-for="(val, cat) in stats.breakdown" :key="cat">
            <div class="flex justify-between text-sm mb-1.5">
              <span class="text-gray-300 font-bold">{{ getCatName(cat) }}</span>
              <span class="text-white font-black">{{ val.amount.toLocaleString() }} ₸</span>
            </div>
            <div class="w-full bg-dark-bg h-3 rounded-full overflow-hidden">
              <div class="h-full rounded-full transition-all duration-700" :class="getCatColor(cat)"
                :style="{ width: `${getPercent(val.amount)}%` }"></div>
            </div>
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>{{ val.count }} чеков</span>
              <span>{{ getPercent(val.amount) }}%</span>
            </div>
          </div>
          <div v-if="!stats.breakdown || Object.keys(stats.breakdown).length === 0"
            class="text-center py-8 text-gray-500">Нет данных за период</div>
        </div>
      </div>

      <!-- Pool stats -->
      <div class="glass-dark border border-dark-border rounded-3xl p-6">
        <h3 class="text-lg font-bold text-white mb-5">Бассейн за период</h3>
        <div class="space-y-4">
          <div class="flex justify-between items-center p-3 bg-white/5 rounded-xl">
            <span class="text-gray-300 font-semibold text-sm">Всего посещений</span>
            <span class="text-white font-black text-lg">{{ poolStats.total }}</span>
          </div>
          <div class="flex justify-between items-center p-3 bg-white/5 rounded-xl">
            <span class="text-gray-300 font-semibold text-sm">Сейчас в бассейне</span>
            <span class="text-blue-400 font-black text-lg">{{ poolStats.active }}</span>
          </div>
          <div v-for="(count, tariff) in poolStats.byTariff" :key="tariff"
            class="flex justify-between items-center p-3 bg-white/5 rounded-xl">
            <span class="text-gray-300 font-semibold text-sm">{{ getTariffLabel(tariff) }}</span>
            <span class="text-white font-black">{{ count }} чел.</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Top products -->
    <div class="glass-dark border border-dark-border rounded-3xl p-6">
      <h3 class="text-lg font-bold text-white mb-5">Остатки склада (топ по стоимости)</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div v-for="p in topProducts" :key="p.id"
          class="p-4 bg-white/5 border border-dark-border/50 rounded-2xl flex justify-between items-center">
          <div>
            <p class="text-white font-bold text-sm">{{ p.name }}</p>
            <p class="text-gray-500 text-xs mt-0.5">{{ p.stock_quantity }} шт. × {{ p.price.toLocaleString() }} ₸</p>
          </div>
          <span class="text-emerald-400 font-black text-sm">{{ (p.price * p.stock_quantity).toLocaleString() }} ₸</span>
        </div>
        <div v-if="topProducts.length === 0" class="col-span-full text-center py-6 text-gray-500">
          Нет данных
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../stores/auth'

const selectedPeriod = ref('today')
const periods = [
  { key: 'today', label: 'Сегодня' },
  { key: 'week', label: 'Неделя' },
  { key: 'month', label: 'Месяц' },
  { key: 'all', label: 'Всё время' },
]

const stats = ref({ total: 0, count: 0, service_fee: 0, subtotal: 0, breakdown: {} })
const poolVisits = ref([])
const topProducts = ref([])

const avgCheck = computed(() =>
  stats.value.count > 0 ? Math.round(stats.value.total / stats.value.count) : 0
)

const poolStats = computed(() => {
  const today = new Date().toDateString()
  const filtered = selectedPeriod.value === 'today'
    ? poolVisits.value.filter(v => new Date(v.entry_time + 'Z').toDateString() === today)
    : poolVisits.value

  const byTariff = {}
  filtered.forEach(v => {
    byTariff[v.tariff_type] = (byTariff[v.tariff_type] || 0) + 1
  })

  return {
    total: filtered.length,
    active: poolVisits.value.filter(v => v.status === 'active').length,
    byTariff
  }
})

const getDateRange = () => {
  const now = new Date()
  const today = now.toISOString().split('T')[0]
  if (selectedPeriod.value === 'today') return { start_date: today, end_date: today }
  if (selectedPeriod.value === 'week') {
    const d = new Date(now); d.setDate(d.getDate() - 7)
    return { start_date: d.toISOString().split('T')[0], end_date: today }
  }
  if (selectedPeriod.value === 'month') {
    const d = new Date(now); d.setDate(d.getDate() - 30)
    return { start_date: d.toISOString().split('T')[0], end_date: today }
  }
  return {}
}

const loadAll = async () => {
  try {
    const range = getDateRange()
    const params = new URLSearchParams()
    if (range.start_date) params.append('start_date', range.start_date)
    if (range.end_date) params.append('end_date', range.end_date)

    const [statsRes, poolRes, productsRes] = await Promise.all([
      api.get(`/finance/stats?${params}`),
      api.get('/pool/'),
      api.get('/stock/products')
    ])
    stats.value = statsRes.data
    poolVisits.value = poolRes.data
    topProducts.value = [...productsRes.data]
      .sort((a, b) => (b.price * b.stock_quantity) - (a.price * a.stock_quantity))
      .slice(0, 6)
  } catch (e) { console.error(e) }
}

const getPercent = (amount) => {
  if (!stats.value.total) return 0
  return Math.round((amount / stats.value.total) * 100)
}

const getCatName = (cat) => ({ pool: 'Бассейн 🏊', bar: 'Бар 🍹', room: 'Бани & VIP 🧖' }[cat] || cat)
const getCatColor = (cat) => ({ pool: 'bg-blue-500', bar: 'bg-emerald-500', room: 'bg-purple-500' }[cat] || 'bg-gray-500')
const getTariffLabel = (t) => ({ adult: 'Взрослый', child: 'Детский', daily: 'Безлимит', vip: 'VIP', hourly: 'Часовой' }[t] || t)

onMounted(() => loadAll())
</script>
