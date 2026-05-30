<template>
  <div class="page-content page-stack">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Управление Персоналом</h1>
        <p class="text-gray-400 font-medium">Контроль учетных записей, ролей и прав доступа</p>
      </div>
      <div class="flex gap-2">
        <button
          @click="openAddUserModal"
          class="px-4 py-2.5 bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 text-white rounded-xl font-bold text-sm shadow-lg shadow-primary-500/20 transition-all flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
          Добавить сотрудника
        </button>
        <button
          @click="openAddRoleModal"
          class="px-4 py-2.5 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white rounded-xl font-bold text-sm shadow-lg shadow-purple-500/20 transition-all flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/></svg>
          Создать роль
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex flex-col sm:flex-row gap-2 bg-dark-surface/50 p-1.5 rounded-2xl border border-dark-border/50 w-full sm:w-fit">
      <button
        @click="activeTab = 'users'"
        class="px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 flex items-center justify-center gap-2 flex-1 w-full sm:w-auto"
        :class="activeTab === 'users'
          ? 'bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-lg shadow-primary-500/25'
          : 'text-gray-400 hover:text-white hover:bg-white/5'"
      >
        <UsersIcon class="w-4 h-4"/>
        <span>Персонал ({{ users.length }})</span>
      </button>
      <button
        @click="activeTab = 'roles'"
        class="px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 flex items-center justify-center gap-2 flex-1 w-full sm:w-auto"
        :class="activeTab === 'roles'
          ? 'bg-gradient-to-r from-purple-600 to-purple-500 text-white shadow-lg shadow-purple-500/25'
          : 'text-gray-400 hover:text-white hover:bg-white/5'"
      >
        <KeyIcon class="w-4 h-4"/>
        <span>Роли доступа ({{ roles.length }})</span>
      </button>
    </div>

    <!-- Users Tab -->
    <div v-if="activeTab === 'users'" class="glass-dark rounded-3xl border border-dark-border shadow-lg overflow-hidden flex flex-col">
      <div class="p-6 border-b border-dark-border bg-white/5">
        <h3 class="text-xl font-bold text-white tracking-tight">Список персонала</h3>
      </div>
      <div class="table-wrap custom-scrollbar">
        <table class="w-full text-left text-sm text-gray-400">
          <thead class="text-xs text-gray-500 uppercase font-bold bg-dark-surface/50">
            <tr>
              <th scope="col" class="px-6 py-4">Сотрудник</th>
              <th scope="col" class="px-6 py-4 hidden sm:table-cell">Роль</th>
              <th scope="col" class="px-6 py-4 hidden sm:table-cell">Дата добавления</th>
              <th scope="col" class="px-6 py-4 hidden sm:table-cell">Статус</th>
              <th scope="col" class="px-6 py-4 text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" class="border-b border-dark-border/50 hover:bg-white/5 transition-colors">
              <td class="px-6 py-4">
                <div class="text-white font-bold text-base">{{ user.full_name }}</div>
                <div class="text-xs text-gray-500 mt-1">{{ user.email }}</div>
              </td>
              <td class="px-6 py-4 hidden sm:table-cell">
                <span class="px-3 py-1 bg-white/10 text-white rounded-lg text-xs font-semibold">{{ user.role?.name || 'Нет роли' }}</span>
              </td>
              <td class="px-6 py-4 text-gray-400 font-medium hidden sm:table-cell">
                {{ new Date(user.created_at).toLocaleDateString() }}
              </td>
              <td class="px-6 py-4 hidden sm:table-cell">
                <span v-if="user.is_active" class="inline-flex items-center px-3 py-1 rounded-xl text-xs font-bold bg-green-500/10 text-green-400 border border-green-500/20">Активен</span>
                <span v-else class="inline-flex items-center px-3 py-1 rounded-xl text-xs font-bold bg-red-500/10 text-red-400 border border-red-500/20">Заблокирован</span>
              </td>
              <td class="px-6 py-4 text-right space-x-2">
                <button
                  @click="openEditUserModal(user)"
                  class="px-3 py-1.5 bg-primary-500/20 text-primary-400 hover:bg-primary-500/30 rounded-lg text-xs font-bold transition-all"
                >
                  Профиль / Изменить
                </button>
                <button
                  @click="deleteUserConfirm(user)"
                  class="px-3 py-1.5 bg-red-500/20 text-red-400 hover:bg-red-500/30 rounded-lg text-xs font-bold transition-all"
                >
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="users.length === 0">
              <td colspan="5" class="px-6 py-10 text-center text-gray-500">Загрузка персонала...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Roles Tab -->
    <div v-if="activeTab === 'roles'" class="glass-dark rounded-3xl border border-dark-border shadow-lg overflow-hidden flex flex-col">
      <div class="p-6 border-b border-dark-border bg-white/5">
        <h3 class="text-xl font-bold text-white tracking-tight">Роли доступа</h3>
      </div>
      <div class="table-wrap custom-scrollbar">
        <table class="w-full text-left text-sm text-gray-400">
          <thead class="text-xs text-gray-500 uppercase font-bold bg-dark-surface/50">
            <tr>
              <th scope="col" class="px-6 py-4">Роль (System ID)</th>
              <th scope="col" class="px-6 py-4">Описание / Отображение</th>
              <th scope="col" class="px-6 py-4 text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="role in roles" :key="role.id" class="border-b border-dark-border/50 hover:bg-white/5 transition-colors">
              <td class="px-6 py-4">
                <div class="text-white font-bold text-base">{{ role.name }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-gray-300 font-medium">{{ role.description || 'Нет описания' }}</div>
                <div class="flex flex-wrap gap-1 mt-2">
                  <span 
                    v-for="tab in getRoleTabNames(role.allowed_tabs)" 
                    :key="tab" 
                    class="px-2 py-0.5 bg-purple-500/10 text-purple-300 border border-purple-500/20 rounded-md text-[10px] font-bold"
                  >
                    {{ tab }}
                  </span>
                  <span v-if="!role.allowed_tabs" class="text-xs text-gray-500 italic">Нет доступа к вкладкам</span>
                </div>
              </td>
              <td class="px-6 py-4 text-right space-x-2">
                <button
                  @click="openEditRoleModal(role)"
                  class="px-3 py-1.5 bg-purple-500/20 text-purple-400 hover:bg-purple-500/30 rounded-lg text-xs font-bold transition-all"
                >
                  Изменить
                </button>
                <button
                  @click="deleteRoleConfirm(role)"
                  class="px-3 py-1.5 bg-red-500/20 text-red-400 hover:bg-red-500/30 rounded-lg text-xs font-bold transition-all"
                >
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="roles.length === 0">
              <td colspan="3" class="px-6 py-10 text-center text-gray-500">Загрузка ролей...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL: Add User -->
    <div v-if="showUserModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div class="glass-dark border border-dark-border w-full max-w-full md:max-w-lg rounded-3xl p-6 sm:p-8 space-y-6 shadow-2xl relative">
        <button @click="showUserModal = false" class="absolute top-5 right-5 text-gray-400 hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
        <h3 class="text-2xl font-black text-white tracking-tight">
          {{ isEditMode ? 'Профиль сотрудника' : 'Новый сотрудник' }}
        </h3>
        <form @submit.prevent="saveUser" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">ФИО сотрудника</label>
            <input v-model="userForm.full_name" type="text" required class="w-full px-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Email (Логин для входа)</label>
            <input v-model="userForm.email" type="email" required class="w-full px-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Роль</label>
              <select v-model="userForm.role_id" required class="w-full px-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
                <option value="" disabled>Выберите роль</option>
                <option v-for="r in roles" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Статус</label>
              <select v-model="userForm.is_active" class="w-full px-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500">
                <option :value="true">Активен</option>
                <option :value="false">Заблокирован</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">
              Пароль {{ isEditMode ? '(заполните только если хотите сменить)' : '' }}
            </label>
            <input
              v-model="userForm.password"
              type="password"
              :placeholder="isEditMode ? '••••••••' : 'Введите пароль'"
              :required="!isEditMode"
              class="w-full px-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-primary-500"
            >
          </div>
          <button type="submit" :disabled="loading" class="w-full py-3 bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400 text-white rounded-xl font-bold transition-all shadow-lg shadow-primary-500/25">
            {{ loading ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </form>
      </div>
    </div>

    <!-- MODAL: Add/Edit Role -->
    <div v-if="showRoleModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div class="glass-dark border border-dark-border w-full max-w-full md:max-w-md rounded-3xl p-6 sm:p-8 space-y-6 shadow-2xl relative flex flex-col max-h-[90vh]">
        <button @click="showRoleModal = false" class="absolute top-5 right-5 text-gray-400 hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
        <h3 class="text-2xl font-black text-white tracking-tight">
          {{ isEditMode ? 'Редактировать роль' : 'Новая роль' }}
        </h3>
        <form @submit.prevent="saveRole" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Название (System ID)</label>
            <input v-model="roleForm.name" type="text" required placeholder="Например: waiter" class="w-full px-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-purple-500">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Описание / Отображение</label>
            <input v-model="roleForm.description" type="text" required placeholder="Например: Официант" class="w-full px-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-purple-500">
          </div>
          
          <!-- Tab Access Selection -->
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Доступные вкладки (разделы)</label>
            <div class="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto custom-scrollbar p-3 bg-dark-surface/50 border border-dark-border rounded-xl">
              <div v-for="tab in availableTabs" :key="tab.id" class="flex items-center gap-2">
                <input 
                  type="checkbox" 
                  :id="'tab-' + tab.id" 
                  v-model="roleForm.selectedTabs" 
                  :value="tab.id"
                  class="rounded bg-dark-bg border-dark-border text-purple-600 focus:ring-purple-500 w-4 h-4 cursor-pointer"
                >
                <label :for="'tab-' + tab.id" class="text-sm text-gray-300 cursor-pointer select-none">{{ tab.name }}</label>
              </div>
            </div>
          </div>

          <button type="submit" :disabled="loading" class="w-full py-3 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white rounded-xl font-bold transition-all shadow-lg shadow-purple-500/25">
            {{ loading ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../stores/auth'
import { toast } from 'vue3-toastify'
import { UsersIcon, KeyIcon } from '@heroicons/vue/24/solid'

const activeTab = ref('users')
const loading = ref(false)
const users = ref([])
const roles = ref([])

// Modals state
const showUserModal = ref(false)
const showRoleModal = ref(false)
const isEditMode = ref(false)
const currentEditId = ref(null)

// Forms state
const userForm = ref({
  full_name: '',
  email: '',
  role_id: '',
  is_active: true,
  password: ''
})

const roleForm = ref({
  name: '',
  description: '',
  selectedTabs: []
})

const availableTabs = [
  { id: 'Dashboard', name: 'Дашборд' },
  { id: 'Pool', name: 'Бассейн' },
  { id: 'Loungers', name: 'Тапчаны' },
  { id: 'Bar', name: 'Бар' },
  { id: 'Steam', name: 'Бани' },
  { id: 'Finance', name: 'Касса' },
  { id: 'Kitchen', name: 'Кухня' },
  { id: 'Staff', name: 'Персонал' },
  { id: 'Analytics', name: 'Аналитика' },
  { id: 'Stock', name: 'Склад' },
  { id: 'Waiter', name: 'Официант' }
]

const getRoleTabNames = (allowedTabsStr) => {
  if (!allowedTabsStr) return []
  const ids = allowedTabsStr.split(',')
  return ids
    .map(id => availableTabs.find(t => t.id === id)?.name)
    .filter(Boolean)
}

const fetchData = async () => {
  try {
    const [usersRes, rolesRes] = await Promise.all([
      api.get('/staff/users'),
      api.get('/staff/roles')
    ])
    users.value = usersRes.data
    roles.value = rolesRes.data
  } catch (err) {
    toast.error('Ошибка загрузки данных')
  }
}

// User methods
const openAddUserModal = () => {
  isEditMode.value = false
  currentEditId.value = null
  userForm.value = {
    full_name: '',
    email: '',
    role_id: '',
    is_active: true,
    password: ''
  }
  showUserModal.value = true
}

const openEditUserModal = (user) => {
  isEditMode.value = true
  currentEditId.value = user.id
  userForm.value = {
    full_name: user.full_name,
    email: user.email,
    role_id: user.role_id,
    is_active: user.is_active,
    password: '' // Keep empty unless updating
  }
  showUserModal.value = true
}

const saveUser = async () => {
  if (loading.value) return
  loading.value = true
  try {
    if (isEditMode.value) {
      await api.put(`/staff/users/${currentEditId.value}`, userForm.value)
      toast.success('Профиль сотрудника успешно обновлен!')
    } else {
      await api.post('/staff/users', userForm.value)
      toast.success('Сотрудник успешно добавлен!')
    }
    showUserModal.value = false
    fetchData()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка сохранения')
  } finally {
    loading.value = false
  }
}

const deleteUserConfirm = async (user) => {
  if (confirm(`Вы уверены, что хотите удалить сотрудника ${user.full_name}?`)) {
    try {
      await api.delete(`/staff/users/${user.id}`)
      toast.success('Сотрудник удален')
      fetchData()
    } catch (err) {
      toast.error('Ошибка удаления сотрудника')
    }
  }
}

// Role methods
const openAddRoleModal = () => {
  isEditMode.value = false
  currentEditId.value = null
  roleForm.value = {
    name: '',
    description: '',
    selectedTabs: []
  }
  showRoleModal.value = true
}

const openEditRoleModal = (role) => {
  isEditMode.value = true
  currentEditId.value = role.id
  roleForm.value = {
    name: role.name,
    description: role.description,
    selectedTabs: role.allowed_tabs ? role.allowed_tabs.split(',') : []
  }
  showRoleModal.value = true
}

const saveRole = async () => {
  if (loading.value) return
  loading.value = true
  try {
    const payload = {
      name: roleForm.value.name,
      description: roleForm.value.description,
      allowed_tabs: roleForm.value.selectedTabs.join(',')
    }
    if (isEditMode.value) {
      await api.put(`/staff/roles/${currentEditId.value}`, payload)
      toast.success('Роль успешно обновлена!')
    } else {
      await api.post('/staff/roles', payload)
      toast.success('Роль успешно создана!')
    }
    showRoleModal.value = false
    fetchData()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка сохранения')
  } finally {
    loading.value = false
  }
}

const deleteRoleConfirm = async (role) => {
  if (confirm(`Вы уверены, что хотите удалить роль "${role.description || role.name}"?`)) {
    try {
      await api.delete(`/staff/roles/${role.id}`)
      toast.success('Роль удалена')
      fetchData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Невозможно удалить эту роль')
    }
  }
}

onMounted(() => {
  fetchData()
})
</script>
