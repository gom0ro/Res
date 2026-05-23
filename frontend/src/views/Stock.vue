<template>
  <div class="page-content page-stack">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Склад</h1>
        <p class="text-gray-400 font-medium">Приход товаров, себестоимость и остатки</p>
      </div>
      <button @click="showModal = true" class="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white rounded-xl font-bold text-sm shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2 hover:-translate-y-0.5">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
        Оформить приход
      </button>
    </div>

    <!-- Stock summary cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="glass-dark border border-dark-border rounded-3xl p-6">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Всего приходов</span>
        <h2 class="text-3xl font-black text-white mt-2">{{ receipts.length }}</h2>
        <span class="text-xs text-gray-500 font-bold mt-1 block">Записей в журнале</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Сумма закупок</span>
        <h2 class="text-3xl font-black text-orange-400 mt-2">{{ totalCost.toLocaleString() }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold mt-1 block">По себестоимости</span>
      </div>
      <div class="glass-dark border border-dark-border rounded-3xl p-6">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">Потенц. выручка</span>
        <h2 class="text-3xl font-black text-emerald-400 mt-2">{{ totalSell.toLocaleString() }} ₸</h2>
        <span class="text-xs text-gray-500 font-bold mt-1 block">По ценам продажи</span>
      </div>
    </div>

    <!-- Products stock table -->
    <div class="glass-dark rounded-3xl border border-dark-border overflow-hidden">
      <div class="p-6 border-b border-dark-border bg-white/5 flex justify-between items-center">
        <h3 class="text-lg font-bold text-white">Остатки на складе</h3>
        <button @click="fetchProducts" class="text-xs text-gray-400 hover:text-white transition-colors">Обновить</button>
      </div>
      <div class="table-wrap custom-scrollbar">
        <table class="w-full text-left text-sm text-gray-400">
          <thead class="text-xs text-gray-500 uppercase font-bold bg-dark-surface/50">
            <tr>
              <th class="px-6 py-4">Товар</th>
              <th class="px-6 py-4 text-right">Остаток</th>
              <th class="px-6 py-4 text-right">Цена продажи</th>
              <th class="px-6 py-4 text-right">Стоимость остатка</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in products" :key="p.id" class="border-b border-dark-border/50 hover:bg-white/5 transition-colors">
              <td class="px-6 py-4 text-white font-bold">{{ p.name }}</td>
              <td class="px-6 py-4 text-right">
                <span class="font-black" :class="p.stock_quantity <= 5 ? 'text-red-400' : p.stock_quantity <= 20 ? 'text-yellow-400' : 'text-emerald-400'">
                  {{ p.stock_quantity }} шт.
                </span>
              </td>
              <td class="px-6 py-4 text-right text-white font-bold">{{ p.price.toLocaleString() }} ₸</td>
              <td class="px-6 py-4 text-right text-orange-400 font-bold">{{ (p.price * p.stock_quantity).toLocaleString() }} ₸</td>
            </tr>
            <tr v-if="products.length === 0">
              <td colspan="4" class="px-6 py-10 text-center text-gray-500">Нет товаров</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Receipt history -->
    <div class="glass-dark rounded-3xl border border-dark-border overflow-hidden">
      <div class="p-6 border-b border-dark-border bg-white/5">
        <h3 class="text-lg font-bold text-white">История приходов</h3>
      </div>
      <div class="table-wrap custom-scrollbar">
        <table class="w-full text-left text-sm text-gray-400">
          <thead class="text-xs text-gray-500 uppercase font-bold bg-dark-surface/50">
            <tr>
              <th class="px-6 py-4">Дата</th>
              <th class="px-6 py-4">Товар</th>
              <th class="px-6 py-4 text-right">Кол-во</th>
              <th class="px-6 py-4 text-right">Себестоимость</th>
              <th class="px-6 py-4 text-right">Цена продажи</th>
              <th class="px-6 py-4 text-right">Наценка</th>
              <th class="px-6 py-4">Примечание</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in receipts" :key="r.id" class="border-b border-dark-border/50 hover:bg-white/5 transition-colors">
              <td class="px-6 py-4 font-mono text-xs text-gray-400">{{ formatDate(r.created_at) }}</td>
              <td class="px-6 py-4 text-white font-bold">{{ r.product_name }}</td>
              <td class="px-6 py-4 text-right text-white font-bold">{{ r.quantity }} шт.</td>
              <td class="px-6 py-4 text-right text-orange-400 font-bold">{{ r.cost_price.toLocaleString() }} ₸</td>
              <td class="px-6 py-4 text-right text-emerald-400 font-bold">{{ r.sell_price.toLocaleString() }} ₸</td>
              <td class="px-6 py-4 text-right">
                <span class="font-bold" :class="markup(r) > 0 ? 'text-emerald-400' : 'text-red-400'">
                  +{{ markup(r) }}%
                </span>
              </td>
              <td class="px-6 py-4 text-gray-400">{{ r.note || '—' }}</td>
            </tr>
            <tr v-if="receipts.length === 0">
              <td colspan="7" class="px-6 py-10 text-center text-gray-500">Приходов пока нет</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Receipt Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-md w-full shadow-2xl relative">
        <button @click="showModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-white">✕</button>
        <h3 class="text-2xl font-bold text-white mb-6">Оформить приход</h3>
        <form @submit.prevent="createReceipt" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Товар</label>
            <select v-model="form.product_id" required class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="" disabled>Выберите товар</option>
              <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }} (остаток: {{ p.stock_quantity }})</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Количество (шт.)</label>
            <input v-model.number="form.quantity" required type="number" min="1" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-emerald-500">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Себестоимость (₸)</label>
              <input v-model.number="form.cost_price" required type="number" min="0" placeholder="500" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-emerald-500">
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Цена продажи (₸)</label>
              <input v-model.number="form.sell_price" required type="number" min="0" placeholder="800" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-emerald-500">
            </div>
          </div>

          <!-- Margin preview -->
          <div v-if="form.cost_price > 0 && form.sell_price > 0" class="p-3 rounded-xl flex justify-between items-center"
            :class="form.sell_price >= form.cost_price ? 'bg-emerald-500/10 border border-emerald-500/20' : 'bg-red-500/10 border border-red-500/20'">
            <span class="text-gray-300 text-sm font-semibold">Наценка:</span>
            <span class="font-black text-lg" :class="form.sell_price >= form.cost_price ? 'text-emerald-400' : 'text-red-400'">
              {{ markupPreview }}%
            </span>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Примечание (необязательно)</label>
            <input v-model="form.note" type="text" placeholder="Поставщик, накладная..." class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-emerald-500">
          </div>

          <button type="submit" :disabled="loading" class="w-full py-3 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white rounded-xl font-bold shadow-lg transition-colors mt-2 disabled:opacity-50">
            {{ loading ? 'Сохранение...' : 'Оформить приход' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'

const receipts = ref([])
const products = ref([])
const showModal = ref(false)
const loading = ref(false)

const form = ref({
  product_id: '',
  quantity: 1,
  cost_price: 0,
  sell_price: 0,
  note: ''
})

const totalCost = computed(() =>
  receipts.value.reduce((s, r) => s + r.cost_price * r.quantity, 0)
)
const totalSell = computed(() =>
  receipts.value.reduce((s, r) => s + r.sell_price * r.quantity, 0)
)

const markupPreview = computed(() => {
  if (!form.value.cost_price) return 0
  return Math.round(((form.value.sell_price - form.value.cost_price) / form.value.cost_price) * 100)
})

const markup = (r) => {
  if (!r.cost_price) return 0
  return Math.round(((r.sell_price - r.cost_price) / r.cost_price) * 100)
}

const fetchReceipts = async () => {
  try {
    const res = await api.get('/stock/')
    receipts.value = res.data
  } catch (e) { console.error(e) }
}

const fetchProducts = async () => {
  try {
    const res = await api.get('/stock/products')
    products.value = res.data
  } catch (e) { console.error(e) }
}

const createReceipt = async () => {
  loading.value = true
  try {
    await api.post('/stock/', form.value)
    toast.success('Приход оформлен')
    showModal.value = false
    form.value = { product_id: '', quantity: 1, cost_price: 0, sell_price: 0, note: '' }
    await Promise.all([fetchReceipts(), fetchProducts()])
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка')
  } finally {
    loading.value = false
  }
}

const formatDate = (iso) => {
  if (!iso) return ''
  const d = new Date(iso.endsWith('Z') ? iso : iso + 'Z')
  return d.toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchReceipts()
  fetchProducts()
})
</script>
