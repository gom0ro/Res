<template>
  <div class="page-content page-stack flex flex-col min-h-0 flex-1">
    <!-- Header -->
    <div>
      <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Финансы & Касса</h1>
      <p class="text-gray-400 font-medium">Анализ доходов, чаевых и закрытых чеков комплекса в реальном времени</p>
    </div>

    <!-- Filters Grid -->
    <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col md:flex-row gap-4 items-end">
      <div class="flex-1 w-full">
        <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Начало периода</label>
        <input type="date" v-model="startDate" class="w-full px-4 py-2.5 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
      </div>
      <div class="flex-1 w-full">
        <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Конец периода</label>
        <input type="date" v-model="endDate" class="w-full px-4 py-2.5 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
      </div>
      <div class="flex-1 w-full">
        <label class="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Категория услуг</label>
        <select v-model="selectedCategory" class="w-full px-4 py-2.5 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
          <option value="">Все категории</option>
          <option value="pool">Бассейн 🏊</option>
          <option value="bar">Бар 🍹</option>
          <option value="room">Бани & VIP 🧖‍♂️</option>
        </select>
      </div>
      <div class="flex gap-2 w-full md:w-auto">
        <button @click="applyFilters" class="flex-1 md:flex-initial px-6 py-2.5 bg-orange-600 hover:bg-orange-500 text-white rounded-xl font-bold text-sm shadow-lg shadow-orange-500/20 transition-all">
          Применить
        </button>
        <button @click="resetFilters" class="px-4 py-2.5 bg-white/5 hover:bg-white/10 text-gray-300 rounded-xl font-bold text-sm transition-all">
          Сброс
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Общая выручка</span>
        <h2 class="text-3xl font-black text-white mt-2">{{ stats.total }} ₸</h2>
        <span class="text-xs text-emerald-400 font-bold mt-2">Касса (брутто)</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Чистая выручка</span>
        <h2 class="text-3xl font-black text-emerald-400 mt-2">{{ stats.subtotal }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold mt-2">За вычетом чаевых</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Чаевые (10% обслуживание)</span>
        <h2 class="text-3xl font-black text-orange-400 mt-2">{{ stats.service_fee }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold mt-2">С заказов бара</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6 flex flex-col justify-between">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Количество чеков</span>
        <h2 class="text-3xl font-black text-white mt-2">{{ stats.count }}</h2>
        <span class="text-xs text-gray-500 font-bold mt-2">Всего транзакций</span>
      </div>
    </div>

    <!-- Category Breakdown & Transaction/Orders Tabbed Board -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
      <!-- Category breakdown -->
      <div class="glass-dark border border-dark-border rounded-3xl p-6 space-y-4 lg:col-span-1">
        <h3 class="text-lg font-bold text-white tracking-tight">Доли направлений</h3>
        <div class="space-y-4">
          <div v-for="(val, cat) in stats.breakdown" :key="cat" class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-300 font-bold capitalize">{{ getCategoryName(cat) }}</span>
              <span class="text-white font-black">{{ val.amount }} ₸</span>
            </div>
            <div class="w-full bg-dark-bg h-2.5 rounded-full overflow-hidden">
              <div class="h-full rounded-full transition-all duration-500" :class="getCategoryColor(cat)" :style="{ width: `${getCategoryPercent(val.amount)}%` }"></div>
            </div>
            <div class="flex justify-between text-[11px] text-gray-500">
              <span>{{ val.count }} транз.</span>
              <span>{{ getCategoryPercent(val.amount) }}%</span>
            </div>
          </div>
          <div v-if="!stats.breakdown || Object.keys(stats.breakdown).length === 0" class="text-center py-6 text-gray-500 text-sm">
            Нет данных по направлениям
          </div>
        </div>
      </div>

      <!-- Main Ledger Column with Tabs -->
      <div class="glass-dark border border-dark-border rounded-3xl p-6 lg:col-span-2 flex flex-col h-[520px]">
        <!-- Tab switches -->
        <div class="flex justify-between items-center border-b border-dark-border/50 pb-4 mb-4 shrink-0">
          <div class="bg-dark-surface border border-dark-border p-1 rounded-xl flex gap-1">
            <button 
              @click="activeSubTab = 'history'"
              class="px-4 py-2 text-xs font-bold rounded-lg transition-colors"
              :class="activeSubTab === 'history' ? 'bg-orange-600 text-white shadow' : 'text-gray-400 hover:text-white'"
            >
              История транзакций
            </button>
            <button 
              @click="activeSubTab = 'unpaid'"
              class="px-4 py-2 text-xs font-bold rounded-lg transition-colors relative"
              :class="activeSubTab === 'unpaid' ? 'bg-orange-600 text-white shadow' : 'text-gray-400 hover:text-white'"
            >
              Ожидают оплаты
              <span v-if="unpaidOrders.length > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border border-dark-surface text-[9px] font-black text-white flex items-center justify-center">
                {{ unpaidOrders.length }}
              </span>
            </button>
          </div>
        </div>

        <!-- History List Tab -->
        <div v-if="activeSubTab === 'history'" class="overflow-y-auto custom-scrollbar flex-1 pr-2">
          <table class="w-full text-left text-sm border-collapse">
            <thead>
              <tr class="border-b border-dark-border/50 text-gray-400 font-bold">
                <th class="py-3">Время</th>
                <th class="py-3">Направление</th>
                <th class="py-3">Детали заказа</th>
                <th class="py-3 text-right">Сумма</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-dark-border/30">
              <tr v-for="t in transactions" :key="t.id" class="text-white hover:bg-white/5 transition-colors">
                <td class="py-3.5 font-mono text-xs text-gray-400">{{ formatTime(t.created_at) }}</td>
                <td class="py-3.5">
                  <span class="px-2 py-0.5 rounded-lg text-xs font-bold uppercase tracking-wider" :class="getCategoryBadgeClass(t.category)">
                    {{ getCategoryName(t.category) }}
                  </span>
                </td>
                <td class="py-3.5 font-bold">{{ t.item_name }}</td>
                <td class="py-3.5 text-right font-black text-orange-400">{{ t.total_amount }} ₸</td>
              </tr>
              <tr v-if="transactions.length === 0">
                <td colspan="4" class="text-center py-10 text-gray-500">
                  Транзакции за выбранный период не найдены
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Unpaid Orders Tab -->
        <div v-else class="overflow-y-auto custom-scrollbar flex-1 pr-2 space-y-4">
          <div 
            v-for="o in unpaidOrders" 
            :key="o.id" 
            class="p-4 bg-dark-surface/20 border border-dark-border/60 rounded-2xl flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 hover:border-orange-500/20 transition-all"
          >
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <span class="font-black text-white text-base">Заказ #{{ o.id }}</span>
                <span class="px-2 py-0.5 bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 rounded-md text-[10px] font-bold uppercase">
                  {{ getStatusLabel(o.status) }}
                </span>
                <span class="text-xs text-gray-400 font-mono">{{ formatTime(o.created_at) }}</span>
              </div>
              <p class="text-sm font-bold text-orange-400">
                {{ o.lounger_id ? `Топчан T-${o.lounger_id}` : 'Барная стойка' }}
              </p>
              <div class="flex flex-wrap gap-1.5 text-xs text-gray-400 mt-1">
                <span v-for="item in o.items" :key="item.id" class="px-1.5 py-0.5 bg-white/5 border border-white/5 rounded-md">
                  {{ item.product?.name || 'Товар' }} × {{ item.quantity }}
                </span>
              </div>
            </div>

            <div class="flex sm:flex-col items-end gap-3 justify-between sm:justify-center shrink-0">
              <div class="text-right">
                <span class="text-[10px] text-gray-500 font-bold uppercase tracking-wider block">Сумма заказа</span>
                <span class="text-lg font-black text-white">{{ o.total_amount }} ₸</span>
              </div>
              <button 
                @click="payOrder(o.id)" 
                class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-emerald-500/10 transition-all"
              >
                Оплатить
              </button>
            </div>
          </div>

          <div v-if="unpaidOrders.length === 0" class="text-center py-20 text-gray-500">
            Нет активных заказов, ожидающих оплаты
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'

const startDate = ref('')
const endDate = ref('')
const selectedCategory = ref('')
const activeSubTab = ref('history')

const transactions = ref([])
const unpaidOrders = ref([])
const stats = ref({
  subtotal: 0,
  service_fee: 0,
  total: 0,
  count: 0,
  breakdown: {}
})

const getCategoryName = (cat) => {
  const map = {
    pool: 'Бассейн 🏊',
    bar: 'Бар 🍹',
    room: 'Бани & VIP 🧖‍♂️'
  }
  return map[cat] || cat
}

const getCategoryBadgeClass = (cat) => {
  const map = {
    pool: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    bar: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    room: 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
  }
  return map[cat] || 'bg-gray-500/10 text-gray-400 border border-gray-500/20'
}

const getCategoryColor = (cat) => {
  const map = {
    pool: 'bg-blue-500',
    bar: 'bg-emerald-500',
    room: 'bg-purple-500'
  }
  return map[cat] || 'bg-gray-500'
}

const getCategoryPercent = (amount) => {
  if (!stats.value.total) return 0
  return Math.round((amount / stats.value.total) * 100)
}

const formatTime = (isoString) => {
  if (!isoString) return ''
  const d = new Date(isoString.endsWith('Z') ? isoString : isoString + 'Z')
  return d.toLocaleString([], {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusLabel = (status) => {
  const map = {
    new: 'Новый',
    preparing: 'Готовится',
    ready: 'Готов к выдаче',
    served: 'Подан',
    paid: 'Оплачен',
    cancelled: 'Отменен'
  }
  return map[status] || status
}

const fetchFinanceData = async () => {
  try {
    const params = {}
    if (startDate.value) params.start_date = startDate.value
    if (endDate.value) params.end_date = endDate.value
    if (selectedCategory.value) params.category = selectedCategory.value

    const [txRes, statsRes] = await Promise.all([
      api.get('/finance/', { params }),
      api.get('/finance/stats', { params: { start_date: startDate.value, end_date: endDate.value } })
    ])
    
    transactions.value = txRes.data
    stats.value = statsRes.data
  } catch (err) {
    console.error("Error loading finance logs", err)
  }
}

const fetchUnpaidOrders = async () => {
  try {
    const res = await api.get('/bar/orders')
    // Filter active unpaid waiter/bar orders
    unpaidOrders.value = res.data.filter(o => !o.is_paid && o.status !== 'cancelled' && o.status !== 'completed')
  } catch(e) {}
}

const payOrder = async (orderId) => {
  if (!confirm('Провести оплату по этому заказу?')) return
  try {
    // Transition status to paid and flag is_paid = true
    await api.post(`/bar/orders/${orderId}/status?status=paid&is_paid=true`)
    toast.success('Оплата успешно проведена')
    fetchUnpaidOrders()
    fetchFinanceData()
  } catch (e) {
    toast.error('Не удалось провести оплату')
  }
}

const applyFilters = () => {
  fetchFinanceData()
}

const resetFilters = () => {
  startDate.value = ''
  endDate.value = ''
  selectedCategory.value = ''
  fetchFinanceData()
}

let pollInterval
onMounted(() => {
  fetchFinanceData()
  fetchUnpaidOrders()
  pollInterval = setInterval(fetchUnpaidOrders, 5000) // Refresh unpaid list every 5s
})

onUnmounted(() => {
  clearInterval(pollInterval)
})
</script>
