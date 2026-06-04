<template>
  <div class="page-content page-stack flex flex-col min-h-0 flex-1">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Панель Официанта</h1>
        <p class="text-gray-400 font-medium">Приём заказов, топчаны и статус</p>
      </div>
      <div class="flex items-center gap-3">
        <div class="px-4 py-2 rounded-xl glass-dark border border-dark-border text-sm">
          <span class="text-gray-400">Активных заказов:</span>
          <span class="ml-1 text-primary-400 font-black text-lg">{{ myActiveOrders.length }}</span>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex flex-col sm:flex-row gap-2 bg-dark-surface/50 p-1.5 rounded-2xl border border-dark-border/50 w-full sm:w-fit">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        class="px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 relative flex items-center justify-center gap-2 flex-1 w-full sm:w-auto"
        :class="activeTab === tab.key
          ? 'bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-lg shadow-primary-500/25'
          : 'text-gray-400 hover:text-white hover:bg-white/5'"
      >
        <component :is="getTabIcon(tab.key)" class="w-4 h-4"/>
        <span>{{ tab.label }}</span>
        <span
          v-if="tab.key === 'orders' && myActiveOrders.length > 0"
          class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full border border-dark-surface text-[10px] font-black text-white flex items-center justify-center"
        >{{ myActiveOrders.length }}</span>
      </button>
    </div>

    <!-- TAB: Новый заказ -->
    <div v-if="activeTab === 'new-order'" class="flex flex-col lg:flex-row gap-6 flex-1 min-h-0">
      <!-- Left: Lounger Selection -->
      <div class="lg:w-1/3 flex flex-col gap-4">
        <div class="glass-dark rounded-2xl border border-dark-border p-5">
          <h3 class="text-white font-bold text-lg mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            Выберите топчан
          </h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-[min(40dvh,300px)] overflow-y-auto custom-scrollbar pr-1">
            <button
              v-for="l in occupiedLoungers"
              :key="l.id"
              @click="selectedLounger = l"
              class="aspect-square rounded-xl border flex flex-col items-center justify-center transition-all duration-200 text-sm font-bold"
              :class="selectedLounger?.id === l.id
                ? 'bg-primary-500/20 border-primary-500 text-primary-400 scale-105 shadow-lg shadow-primary-500/20'
                : 'bg-white/5 border-dark-border text-gray-400 hover:bg-white/10 hover:text-white'"
            >
              <span class="text-lg font-black">{{ l.number }}</span>
              <span class="text-[10px] uppercase tracking-wider opacity-60">{{ l.zone }}</span>
            </button>
          </div>
          <p v-if="occupiedLoungers.length === 0" class="text-gray-500 text-sm text-center py-4">Нет занятых топчанов</p>
        </div>

        <!-- Cart summary -->
        <div class="glass-dark rounded-2xl border border-dark-border p-5 flex-1">
          <h3 class="text-white font-bold text-lg mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
            Корзина
          </h3>
          <div v-if="cart.length === 0" class="text-gray-500 text-sm text-center py-6">Корзина пуста</div>
          <div v-else class="space-y-2 max-h-[250px] overflow-y-auto custom-scrollbar pr-1">
            <div v-for="(item, idx) in cart" :key="idx" class="flex items-center justify-between bg-white/5 rounded-xl px-3 py-2 group">
              <div class="flex-1 min-w-0">
                <p class="text-white text-sm font-semibold truncate">{{ item.product.name }}</p>
                <p class="text-gray-500 text-xs">{{ item.product.price }} ₸ × {{ item.quantity }}</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-primary-400 font-bold text-sm">{{ item.product.price * item.quantity }} ₸</span>
                <button @click="removeFromCart(idx)" class="text-red-400/50 hover:text-red-400 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
            </div>
          </div>
          <div v-if="cart.length > 0" class="mt-4 pt-4 border-t border-dark-border space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-400">Подытог</span>
              <span class="text-white font-bold">{{ cartSubtotal }} ₸</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-400">Обслуживание (10%)</span>
              <span class="text-yellow-400 font-bold">{{ cartServiceFee }} ₸</span>
            </div>
            <div class="flex justify-between text-lg font-black">
              <span class="text-white">Итого</span>
              <span class="text-emerald-400">{{ cartTotal }} ₸</span>
            </div>
            <button
              @click="submitOrder"
              :disabled="!selectedLounger || submitting"
              class="w-full mt-3 py-3 rounded-xl font-bold text-sm transition-all duration-300 shadow-lg"
              :class="selectedLounger
                ? 'bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white shadow-emerald-500/25 hover:shadow-emerald-500/40'
                : 'bg-gray-700 text-gray-500 cursor-not-allowed'"
            >
              <span v-if="submitting">Отправка...</span>
              <span v-else-if="!selectedLounger">Выберите топчан ↑</span>
              <span v-else>Отправить заказ → T-{{ selectedLounger.number }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Right: Product Catalog -->
      <div class="lg:w-2/3 flex flex-col gap-4">
        <!-- Categories scroll -->
        <div class="flex gap-2 overflow-x-auto pb-2 custom-scrollbar">
          <button
            @click="selectedCategory = null"
            class="px-4 py-2 rounded-xl text-sm font-bold whitespace-nowrap transition-all duration-200"
            :class="!selectedCategory
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/25'
              : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 border border-dark-border'"
          >Все блюда</button>
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="selectedCategory = cat.id"
            class="px-4 py-2 rounded-xl text-sm font-bold whitespace-nowrap transition-all duration-200"
            :class="selectedCategory === cat.id
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/25'
              : 'bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 border border-dark-border'"
          >{{ cat.name }}</button>
        </div>

        <!-- Product grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-4 gap-3 overflow-y-auto custom-scrollbar flex-1 min-h-0 max-h-[min(55dvh,28rem)] lg:max-h-none">
          <div
            v-for="p in filteredProducts"
            :key="p.id"
            @click="addToCart(p)"
            class="glass-dark border border-dark-border rounded-2xl p-4 cursor-pointer transition-all duration-300 hover:border-primary-500/50 hover:shadow-lg hover:shadow-primary-500/10 hover:scale-[1.02] group flex flex-col"
          >
            <div class="w-full aspect-square rounded-xl bg-gradient-to-br from-primary-500/10 to-purple-500/10 flex items-center justify-center mb-3">
              <svg class="w-10 h-10 text-primary-400/50 group-hover:text-primary-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0A1.75 1.75 0 013 15.546V12a9 9 0 0118 0v3.546zM12 3v2m6.364 1.636l-1.414 1.414M21 12h-2M5 12H3m3.05-4.95L4.636 5.636"/></svg>
            </div>
            <h4 class="text-white text-sm font-bold truncate">{{ p.name }}</h4>
            <div class="flex justify-between items-center mt-auto pt-2">
              <span class="text-primary-400 font-black">{{ p.price }} ₸</span>
              <span class="text-[10px] text-gray-500 font-medium">ост: {{ p.stock_quantity !== null ? p.stock_quantity : '∞' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB: Мои заказы -->
    <div v-if="activeTab === 'orders'" class="space-y-4">
      <div v-if="myOrders.length === 0" class="glass-dark rounded-2xl border border-dark-border p-12 text-center">
        <svg class="w-16 h-16 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        <p class="text-gray-500 text-lg font-bold">У вас пока нет заказов</p>
        <p class="text-gray-600 text-sm mt-1">Перейдите во вкладку «Новый заказ», чтобы принять первый</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <div
          v-for="order in myOrders"
          :key="order.id"
          class="glass-dark border rounded-2xl p-5 transition-all duration-300 hover:shadow-lg"
          :class="{
            'border-yellow-500/30 hover:shadow-yellow-500/10': order.status === 'new',
            'border-blue-500/30 hover:shadow-blue-500/10': order.status === 'preparing',
            'border-emerald-500/30 hover:shadow-emerald-500/10': order.status === 'ready',
            'border-gray-600/30': order.status === 'completed'
          }"
        >
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <span class="text-white font-black text-lg">#{{ order.id }}</span>
              <span v-if="order.lounger_id" class="px-2 py-0.5 rounded-lg bg-purple-500/20 text-purple-400 text-xs font-bold">T-{{ order.lounger_id }}</span>
            </div>
            <span
              class="px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider"
              :class="{
                'bg-yellow-500/20 text-yellow-400': order.status === 'new',
                'bg-blue-500/20 text-blue-400': order.status === 'preparing',
                'bg-emerald-500/20 text-emerald-400': order.status === 'ready',
                'bg-gray-600/20 text-gray-400': order.status === 'completed'
              }"
            >
              {{ statusLabels[order.status] || order.status }}
            </span>
          </div>
          <div class="space-y-1.5 mb-3">
            <div v-for="item in order.items" :key="item.id" class="flex justify-between text-sm">
              <span class="text-gray-300">{{ item.product?.name || 'Товар' }} × {{ item.quantity }}</span>
              <span class="text-gray-400">{{ item.price_at_time * item.quantity }} ₸</span>
            </div>
          </div>
          <div class="flex justify-between items-center pt-3 border-t border-dark-border">
            <span class="text-gray-500 text-xs">{{ formatTime(order.created_at) }}</span>
            <span class="text-white font-black">{{ order.total_amount }} ₸</span>
          </div>
          <div v-if="order.status === 'ready'" class="mt-3">
            <button
              @click="markDelivered(order.id)"
              class="w-full py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-emerald-500 text-white font-bold text-sm hover:from-emerald-500 hover:to-emerald-400 transition-all shadow-lg shadow-emerald-500/20"
            >✓ Доставлено гостю</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB: Топчаны -->
    <div v-if="activeTab === 'loungers'" class="space-y-4">
      <div class="glass-dark p-6 rounded-2xl border border-dark-border">
        <div class="flex items-center gap-6 mb-6">
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
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-2 sm:gap-3">
          <div
            v-for="l in loungers"
            :key="l.id"
            class="aspect-square rounded-2xl border flex flex-col items-center justify-center transition-all duration-300 group relative overflow-hidden"
            :class="{
              'bg-green-500/10 border-green-500/30 text-green-400': l.status === 'free',
              'bg-red-500/10 border-red-500/30 text-red-400': l.status === 'occupied',
              'bg-yellow-500/10 border-yellow-500/30 text-yellow-400': l.status === 'reserved',
            }"
          >
            <h3 class="text-2xl font-black mb-1">{{ l.number }}</h3>
            <span class="text-xs font-bold uppercase tracking-wider opacity-70">{{ l.zone }}</span>
            <div class="absolute bottom-2 font-medium text-xs">{{ l.price_per_hour }} ₸/ч</div>
          </div>
        </div>
        <div v-if="loungers.length === 0" class="text-center py-12 text-gray-500">Нет добавленных топчанов.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore, api } from '../stores/auth'
import { toast } from 'vue3-toastify'
import { PlusIcon, QueueListIcon, MapIcon } from '@heroicons/vue/24/solid'

const authStore = useAuthStore()

const activeTab = ref('new-order')
const tabs = [
  { key: 'new-order', label: 'Новый заказ' },
  { key: 'orders', label: 'Мои заказы' },
  { key: 'loungers', label: 'Топчаны' }
]

const getTabIcon = (key) => {
  return {
    'new-order': PlusIcon,
    'orders': QueueListIcon,
    'loungers': MapIcon
  }[key]
}

const statusLabels = {
  'new': 'Новый',
  'preparing': 'Готовится',
  'ready': 'Готов',
  'completed': 'Выполнен'
}

// Data
const products = ref([])
const categories = ref([])
const loungers = ref([])
const myOrders = ref([])
const cart = ref([])
const selectedLounger = ref(null)
const selectedCategory = ref(null)
const submitting = ref(false)

// Computed
const occupiedLoungers = computed(() => loungers.value.filter(l => l.status === 'occupied'))

const filteredProducts = computed(() => {
  if (!selectedCategory.value) return products.value
  return products.value.filter(p => p.category_id === selectedCategory.value)
})

const cartSubtotal = computed(() => cart.value.reduce((s, i) => s + i.product.price * i.quantity, 0))
const cartServiceFee = computed(() => Math.round(cartSubtotal.value * 0.1))
const cartTotal = computed(() => cartSubtotal.value + cartServiceFee.value)

const myActiveOrders = computed(() => myOrders.value.filter(o => o.status !== 'completed'))

// Cart methods
const addToCart = (product) => {
  const existing = cart.value.find(i => i.product.id === product.id)
  if (existing) {
    existing.quantity++
  } else {
    cart.value.push({ product: { ...product }, quantity: 1 })
  }
  toast.success(`${product.name} добавлен`)
}

const removeFromCart = (idx) => {
  cart.value.splice(idx, 1)
}

// Submit order
const submitOrder = async () => {
  if (!selectedLounger.value || cart.value.length === 0) return
  submitting.value = true
  try {
    const payload = {
      items: cart.value.map(i => ({ product_id: i.product.id, quantity: i.quantity })),
      lounger_id: selectedLounger.value.id,
      waiter_id: authStore.user?.id || null
    }
    await api.post('/bar/orders', payload)
    toast.success(`Заказ отправлен к T-${selectedLounger.value.number}!`)
    cart.value = []
    selectedLounger.value = null
    fetchMyOrders()
    fetchProducts()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка создания заказа')
  } finally {
    submitting.value = false
  }
}

// Mark delivered
const markDelivered = async (orderId) => {
  try {
    await api.post(`/bar/orders/${orderId}/status?status=completed`)
    toast.success('Заказ доставлен гостю!')
    fetchMyOrders()
  } catch (err) {
    toast.error('Ошибка обновления')
  }
}

// Fetching
const fetchProducts = async () => {
  try {
    const res = await api.get('/bar/products')
    products.value = res.data
  } catch (e) { console.error(e) }
}

const fetchCategories = async () => {
  try {
    const res = await api.get('/bar/categories')
    categories.value = res.data
  } catch (e) { console.error(e) }
}

const fetchLoungers = async () => {
  try {
    const res = await api.get('/loungers/')
    loungers.value = res.data
  } catch (e) { console.error(e) }
}

const fetchMyOrders = async () => {
  try {
    const res = await api.get('/bar/orders')
    // Filter by current waiter
    const userId = authStore.user?.id
    myOrders.value = userId
      ? res.data.filter(o => o.waiter_id === userId)
      : res.data
  } catch (e) { console.error(e) }
}

const formatTime = (dt) => {
  if (!dt) return ''
  const d = new Date(dt + 'Z')
  return d.toLocaleString('ru-RU', { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit' })
}

// Lifecycle
onMounted(() => {
  fetchProducts()
  fetchCategories()
  fetchLoungers()
  fetchMyOrders()
})

// Auto refresh orders
let interval
onMounted(() => {
  interval = setInterval(() => {
    fetchMyOrders()
  }, 8000)
})

import { onUnmounted } from 'vue'
onUnmounted(() => clearInterval(interval))
</script>
