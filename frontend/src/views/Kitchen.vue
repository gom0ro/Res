<template>
  <div class="page-content page-stack flex flex-col min-h-0 flex-1">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-center space-y-2 sm:space-y-0">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Монитор Кухни (KDS)</h1>
        <p class="text-gray-400 font-medium">Экран приготовления заказов в реальном времени</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="px-3 py-1.5 bg-dark-surface border border-dark-border text-gray-300 font-bold rounded-xl text-sm">
          Всего в работе: {{ activeOrdersCount }}
        </span>
        <button @click="showCategoryModal = true; fetchCategories()" class="px-5 py-2.5 bg-dark-surface border border-dark-border hover:bg-white/5 text-gray-300 rounded-xl font-bold text-sm transition-all duration-300 hover:-translate-y-0.5">
          Категории
        </button>
        <button @click="openAddModal" class="px-5 py-2.5 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold text-sm shadow-lg transition-all duration-300 hover:-translate-y-0.5">
          Добавить блюдо
        </button>
      </div>
    </div>

    <!-- Category Filter Bar -->
    <div class="flex gap-2 overflow-x-auto pb-3 custom-scrollbar whitespace-nowrap shrink-0">
      <button 
        @click="selectedKitchenCategoryId = null"
        class="px-4 py-2 text-xs font-bold rounded-xl border transition-all"
        :class="selectedKitchenCategoryId === null ? 'bg-orange-600 border-orange-600 text-white' : 'bg-dark-surface/50 border-dark-border text-gray-400 hover:text-white'"
      >
        Все категории
      </button>
      <button 
        v-for="cat in categories" :key="cat.id"
        @click="selectedKitchenCategoryId = cat.id"
        class="px-4 py-2 text-xs font-bold rounded-xl border transition-all flex items-center gap-1.5"
        :class="selectedKitchenCategoryId === cat.id ? 'bg-orange-600 border-orange-600 text-white' : 'bg-dark-surface/50 border-dark-border text-gray-400 hover:text-white'"
        :style="selectedKitchenCategoryId === cat.id ? {} : { borderColor: cat.color ? cat.color + '40' : undefined, color: cat.color || undefined }"
      >
        <span>{{ cat.icon || '' }}</span>
        <span>{{ cat.name }}</span>
      </button>
    </div>

    <!-- Kitchen Orders Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 flex-1 overflow-y-auto pr-2 custom-scrollbar h-full">
      <div 
        v-for="o in filteredOrders" 
        :key="o.id" 
        class="glass-dark border rounded-3xl p-4 md:p-6 flex flex-col justify-between transition-all"
        :class="o.status === 'preparing' ? 'border-blue-500/30 bg-blue-500/5' : 'border-red-500/30 bg-red-500/5 animate-pulse-subtle'"
      >
        <div>
          <!-- Card Header -->
          <div class="flex justify-between items-start mb-2 md:mb-4">
            <div>
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Заказ #{{ o.id }}</span>
              <h3 class="text-lg md:text-xl font-black text-white mt-1">
                {{ o.lounger_id ? `Топчан T-${o.lounger_id}` : 'У барной стойки' }}
              </h3>
            </div>
            <span 
              class="px-2.5 py-1 rounded-lg text-xs font-bold uppercase tracking-wider"
              :class="o.status === 'preparing' ? 'bg-blue-500/20 text-blue-400' : 'bg-red-500/20 text-red-400'"
            >
              {{ o.status === 'preparing' ? 'Готовится' : 'Новый' }}
            </span>
          </div>

          <!-- Time Elapsed -->
          <p class="text-xs text-gray-500 font-bold mb-4">
            Поступил: {{ formatTime(o.created_at) }}
          </p>

          <!-- Order Items (Large font for kitchen) -->
          <div class="border-t border-dark-border/50 pt-4 space-y-3">
            <div v-for="item in o.items" :key="item.id" class="flex justify-between text-sm">
              <span class="text-white font-bold">{{ item.product?.name || 'Блюдо' }}</span>
              <span class="text-orange-400 font-black text-base">× {{ item.quantity }}</span>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="border-t border-dark-border/50 pt-4 mt-6">
          <button 
            v-if="o.status === 'new'"
            @click="updateStatus(o.id, 'preparing')"
            class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-500/20 flex items-center justify-center gap-2"
          >
            <span>Начать готовить</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </button>
          
          <button 
            v-if="o.status === 'preparing'"
            @click="updateStatus(o.id, 'ready')"
            class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2"
          >
            <span>Готово</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          </button>
        </div>
      </div>

      <div v-if="orders.length === 0" class="col-span-full h-96 flex flex-col items-center justify-center text-gray-500 opacity-60">
        <svg class="w-20 h-20 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
        <h3 class="text-xl font-bold text-gray-300">Очередь пуста</h3>
        <p class="text-sm text-gray-500 mt-1">Ожидайте заказов от официантов</p>
      </div>
    </div>

    <!-- Modal for Adding Dish -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-full md:max-w-md w-full shadow-2xl relative">
        <button @click="showAddModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>
        <h3 class="text-2xl font-bold text-white mb-6">Новое блюдо / Товар</h3>
        <form @submit.prevent="createProduct" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Название блюда</label>
            <input v-model="newProduct.name" required type="text" placeholder="Например: Плов Ташкентский" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Категория</label>
            <select v-model="newProduct.category_id" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
              <option :value="null">Без категории (Общее)</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Цена (₸)</label>
              <input v-model.number="newProduct.price" required type="number" min="0" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Количество порций</label>
              <input v-model.number="newProduct.stock_quantity" required type="number" min="0" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
            </div>
          </div>
          <button type="submit" class="w-full py-3 bg-orange-600 hover:bg-orange-500 text-white rounded-xl font-bold shadow-lg transition-colors mt-4">Добавить в меню</button>
        </form>
      </div>
    </div>
    <!-- Modal for Managing Categories -->
    <div v-if="showCategoryModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-full md:max-w-md w-full shadow-2xl relative flex flex-col max-h-[90vh]">
        <button @click="showCategoryModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>
        <h3 class="text-2xl font-bold text-white mb-4">Управление категориями</h3>
        
        <!-- List of Categories -->
        <div class="flex-1 overflow-y-auto custom-scrollbar mb-6 pr-1 space-y-2 max-h-[300px]">
          <div v-for="cat in categories" :key="cat.id" class="p-3 bg-dark-bg border border-dark-border/50 rounded-xl flex items-center justify-between">
            <!-- View Mode -->
            <div v-if="editingCategoryId !== cat.id" class="flex-1 flex justify-between items-center">
              <div>
                <p class="text-white font-bold text-sm flex items-center gap-2">
                  <span class="text-lg" :style="{ color: cat.color || undefined }">{{ cat.icon || '' }}</span>
                  <span>{{ cat.name }}</span>
                </p>
                <p v-if="cat.description" class="text-xs text-gray-400">{{ cat.description }}</p>
              </div>
              <div class="flex gap-1">
                <button 
                  @click="startEdit(cat)"
                  class="p-2 text-blue-400 hover:text-blue-300 hover:bg-blue-500/10 rounded-lg transition-colors"
                  title="Редактировать"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                </button>
                <button 
                  v-if="cat.name !== 'Общее' && cat.name !== 'Напитки' && cat.name !== 'Закуски'"
                  @click="deleteCategory(cat.id)" 
                  class="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors"
                  title="Удалить категорию"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
              </div>
            </div>

            <!-- Edit Mode -->
            <div v-else class="flex-1 space-y-3 p-1">
              <div class="flex gap-2">
                <input v-model="editForm.name" required type="text" placeholder="Название" class="flex-1 px-3 py-1.5 bg-dark-surface border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-1 focus:ring-orange-500">
                <input v-model="editForm.icon" type="text" placeholder="Иконка (emoji)" class="w-20 px-3 py-1.5 bg-dark-surface border border-dark-border rounded-xl text-center text-white text-sm outline-none focus:ring-1 focus:ring-orange-500">
              </div>
              <div class="flex gap-2">
                <input v-model="editForm.description" type="text" placeholder="Описание" class="flex-1 px-3 py-1.5 bg-dark-surface border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-1 focus:ring-orange-500">
                <input v-model="editForm.color" type="color" class="w-12 h-9 p-0 bg-transparent border-0 rounded-lg cursor-pointer">
              </div>
              <div class="flex justify-end gap-2 text-xs">
                <button type="button" @click="editingCategoryId = null" class="px-3 py-1.5 bg-dark-surface border border-dark-border text-gray-400 hover:text-white rounded-lg">Отмена</button>
                <button type="button" @click="saveEdit(cat.id)" class="px-3 py-1.5 bg-orange-600 hover:bg-orange-500 text-white rounded-lg font-bold">Сохранить</button>
              </div>
            </div>
          </div>
          <div v-if="categories.length === 0" class="text-center py-6 text-gray-500 text-sm">
            Категории отсутствуют
          </div>
        </div>

        <!-- Add Category Form -->
        <div class="border-t border-dark-border/50 pt-4 shrink-0">
          <h4 class="text-sm font-bold text-white mb-3">Создать категорию</h4>
          <form @submit.prevent="createCategory" class="space-y-3">
            <div class="flex gap-2">
              <div class="flex-1">
                <label class="block text-[10px] font-semibold text-gray-400 mb-1">Название категории</label>
                <input v-model="newCategory.name" required type="text" placeholder="Например: Горячие блюда" class="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-orange-500">
              </div>
              <div class="w-20">
                <label class="block text-[10px] font-semibold text-gray-400 mb-1">Иконка</label>
                <input v-model="newCategory.icon" type="text" placeholder="🍲" class="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-xl text-center text-white text-sm outline-none focus:ring-2 focus:ring-orange-500">
              </div>
            </div>
            <div class="flex gap-2 items-end">
              <div class="flex-1">
                <label class="block text-[10px] font-semibold text-gray-400 mb-1">Описание (необязательно)</label>
                <input v-model="newCategory.description" type="text" placeholder="Описание..." class="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-xl text-white text-sm outline-none focus:ring-2 focus:ring-orange-500">
              </div>
              <div class="w-12 flex flex-col items-center">
                <label class="block text-[10px] font-semibold text-gray-400 mb-1 text-center">Цвет</label>
                <input v-model="newCategory.color" type="color" class="w-full h-[38px] p-0 bg-transparent border-0 rounded-lg cursor-pointer">
              </div>
            </div>
            <button type="submit" class="w-full py-2.5 bg-orange-600 hover:bg-orange-500 text-white rounded-xl font-bold text-sm shadow-lg transition-colors mt-2">
              Добавить категорию
            </button>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'
import { XMarkIcon as XIcon } from '@heroicons/vue/24/solid'
const orders = ref([])
const showAddModal = ref(false)
const showCategoryModal = ref(false)
const categories = ref([])
const selectedKitchenCategoryId = ref(null)

const editingCategoryId = ref(null)
const editForm = ref({
  name: '',
  description: '',
  color: '#4B5563',
  icon: '',
  position: 0
})

const newProduct = ref({
  name: '',
  price: 0,
  stock_quantity: 0,
  category_id: null
})
const newCategory = ref({
  name: '',
  description: '',
  color: '#4B5563',
  icon: ''
})

const activeOrdersCount = computed(() => orders.value.length)

const filteredOrders = computed(() => {
  if (selectedKitchenCategoryId.value === null) return orders.value
  return orders.value.filter(o => 
    o.items.some(item => item.product?.category_id === selectedKitchenCategoryId.value)
  )
})

const fetchCategories = async () => {
  try {
    const res = await api.get('/bar/categories')
    categories.value = res.data
  } catch (e) {}
}

const createCategory = async () => {
  try {
    await api.post('/bar/categories', newCategory.value)
    newCategory.value = { name: '', description: '', color: '#4B5563', icon: '🍲' }
    toast.success('Категория успешно создана')
    await fetchCategories()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка создания категории')
  }
}

const startEdit = (cat) => {
  editingCategoryId.value = cat.id
  editForm.value = {
    name: cat.name,
    description: cat.description || '',
    color: cat.color || '#4B5563',
    icon: cat.icon || '',
    position: cat.position || 0
  }
}

const saveEdit = async (id) => {
  try {
    await api.put(`/bar/categories/${id}`, editForm.value)
    editingCategoryId.value = null
    toast.success('Категория успешно обновлена')
    await fetchCategories()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка при сохранении изменений')
  }
}

const deleteCategory = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить эту категорию?')) return
  try {
    await api.delete(`/bar/categories/${id}`)
    toast.success('Категория успешно удалена')
    await fetchCategories()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка удаления категории')
  }
}

const openAddModal = () => {
  fetchCategories()
  showAddModal.value = true
}

const createProduct = async () => {
  try {
    await api.post('/bar/products', newProduct.value)
    showAddModal.value = false
    newProduct.value = { name: '', price: 0, stock_quantity: 0, category_id: null }
    toast.success('Блюдо успешно добавлено в меню')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка добавления')
  }
}

const fetchKitchenOrders = async () => {
  try {
    const res = await api.get('/bar/orders')
    // Show only orders that are 'new' or 'preparing'
    orders.value = res.data.filter(o => o.status === 'new' || o.status === 'preparing')
  } catch (err) {
    console.error("Error loading kitchen orders", err)
  }
}

const updateStatus = async (orderId, newStatus) => {
  try {
    await api.post(`/bar/orders/${orderId}/status?status=${newStatus}`)
    toast.success(newStatus === 'preparing' ? 'Начато приготовление' : 'Заказ готов')
    fetchKitchenOrders()
  } catch (e) {
    toast.error('Не удалось обновить статус заказа')
  }
}

const formatTime = (isoString) => {
  if (!isoString) return ''
  const d = new Date(isoString.endsWith('Z') ? isoString : isoString + 'Z')
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

let pollInterval
onMounted(() => {
  fetchKitchenOrders()
  fetchCategories()
  pollInterval = setInterval(fetchKitchenOrders, 5000) // Auto refresh every 5 seconds
})

onUnmounted(() => {
  clearInterval(pollInterval)
})
</script>

<style scoped>
.animate-pulse-subtle {
  animation: pulse-subtle 2s infinite ease-in-out;
}
@keyframes pulse-subtle {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; border-color: rgba(239, 68, 68, 0.5); }
}
</style>
