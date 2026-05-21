<template>
  <div class="flex h-screen bg-dark-bg overflow-hidden relative">
    
    <!-- Mobile overlay -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"
      @click="sidebarOpen = false"
    ></div>

    <!-- Sidebar -->
    <aside 
      class="fixed lg:static inset-y-0 left-0 z-50 w-64 glass-dark border-r border-dark-border flex flex-col transition-transform duration-300 transform lg:transform-none"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="h-16 flex items-center justify-between px-6 border-b border-dark-border/50">
        <span class="text-xl font-bold text-white tracking-wider flex items-center gap-2">
          <svg class="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          Resort OS
        </span>
        <button @click="sidebarOpen = false" class="lg:hidden text-gray-400 hover:text-white">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-2 custom-scrollbar">
        <router-link 
          v-for="item in navigation" 
          :key="item.name" 
          :to="item.to"
          @click="sidebarOpen = false"
          class="flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 group relative overflow-hidden"
          :class="[$route.name === item.routeName ? 'text-white shadow-lg' : 'text-gray-400 hover:text-white hover:bg-white/5']"
        >
          <!-- Active Background -->
          <div v-if="$route.name === item.routeName" class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-500 opacity-90"></div>
          
          <component :is="item.icon" class="mr-3 flex-shrink-0 h-5 w-5 relative z-10 transition-transform group-hover:scale-110" :class="[$route.name === item.routeName ? 'text-white' : 'text-gray-500 group-hover:text-primary-400']" aria-hidden="true" />
          <span class="relative z-10">{{ item.name }}</span>
        </router-link>
      </nav>

      <div class="p-4 border-t border-dark-border/50 bg-black/20">
        <div class="flex items-center gap-3 mb-4 px-2">
          <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-primary-500 to-purple-500 flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-primary-500/30">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate">{{ authStore.user?.full_name || 'Администратор' }}</p>
            <p class="text-xs text-gray-400 truncate">{{ authStore.user?.email }}</p>
          </div>
        </div>
        <button @click="logout" class="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/20 hover:text-red-300 rounded-xl transition-all duration-200 group">
          <ArrowRightOnRectangleIcon class="w-5 h-5 transition-transform group-hover:-translate-x-1" />
          Выйти из системы
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col relative min-w-0 overflow-hidden bg-dark-bg/50">
      <header class="h-16 flex items-center justify-between px-4 sm:px-8 glass border-b border-dark-border/50 z-50 sticky top-0 overflow-visible">
        <div class="flex items-center gap-4">
          <button @click="sidebarOpen = true" class="lg:hidden p-2 text-gray-400 hover:text-white rounded-lg hover:bg-white/5 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
          <h2 class="text-lg font-bold text-white hidden sm:block">{{ currentRouteName }}</h2>
        </div>
        <div class="flex items-center gap-4 relative overflow-visible">
          <!-- Notification Bell -->
          <button @click="toggleNotificationsDropdown" class="p-2 text-gray-400 hover:text-white rounded-full hover:bg-white/5 transition-colors relative group">
            <BellIcon class="w-6 h-6 transition-transform group-hover:rotate-12" :class="{'text-white animate-pulse': unreadCount > 0}" />
            <span v-if="unreadCount > 0" class="absolute top-1.5 right-1.5 w-4 h-4 bg-red-500 rounded-full border border-dark-surface text-[9px] font-black text-white flex items-center justify-center animate-bounce">
              {{ unreadCount }}
            </span>
          </button>

          <!-- Notifications Dropdown -->
          <div 
            v-if="showNotifications" 
            class="absolute right-0 top-12 w-80 sm:w-96 glass-dark border border-dark-border rounded-2xl shadow-2xl overflow-hidden z-30"
          >
            <div class="p-4 border-b border-dark-border bg-white/5 flex justify-between items-center">
              <span class="font-bold text-white text-xs uppercase tracking-wider">Оповещения</span>
              <button 
                v-if="unreadCount > 0" 
                @click="markAllAsRead" 
                class="text-[10px] font-black text-primary-400 hover:text-primary-300 transition-colors uppercase tracking-widest"
              >
                Прочитать все
              </button>
            </div>
            
            <div class="max-h-80 overflow-y-auto custom-scrollbar p-3 space-y-2">
              <div 
                v-for="n in notifications" 
                :key="n.id" 
                class="p-3 rounded-xl border transition-all relative overflow-hidden"
                :class="{
                  'bg-white/5 border-white/5 opacity-60': n.read,
                  'bg-primary-500/10 border-primary-500/25 shadow-md shadow-primary-500/5': !n.read,
                }"
              >
                <div class="flex gap-2.5">
                  <div class="shrink-0 mt-1">
                    <span v-if="n.type === 'warning'" class="w-2 h-2 rounded-full bg-red-500 inline-block animate-ping"></span>
                    <span v-else-if="n.type === 'success'" class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
                    <span v-else class="w-2 h-2 rounded-full bg-blue-500 inline-block"></span>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs font-black text-white leading-tight truncate">{{ n.title }}</p>
                    <p class="text-[11px] text-gray-400 mt-1 leading-normal font-semibold">{{ n.description }}</p>
                    <div class="flex justify-between items-center mt-2.5">
                      <span class="text-[8px] font-black uppercase tracking-wider text-gray-500">{{ n.time }}</span>
                      <button 
                        v-if="!n.read" 
                        @click="markAsRead(n.id)" 
                        class="text-[9px] font-black text-primary-400 hover:text-primary-300 uppercase tracking-widest"
                      >
                        Ок
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      <!-- Background animations -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none z-0">
        <div class="absolute w-[500px] h-[500px] bg-primary-600/10 rounded-full blur-3xl -top-40 -right-40 animate-slow-spin"></div>
        <div class="absolute w-[600px] h-[600px] bg-purple-600/10 rounded-full blur-3xl -bottom-60 -left-40 animate-slow-spin-reverse"></div>
      </div>

      <div class="flex-1 overflow-auto p-4 sm:p-8 relative z-10 custom-scrollbar">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore, api } from '../../stores/auth'
import { 
  HomeIcon, 
  UserGroupIcon, 
  MapIcon, 
  BeakerIcon,
  ArrowRightOnRectangleIcon,
  BellIcon,
  UserPlusIcon,
  FireIcon,
  BanknotesIcon,
  QueueListIcon,
  ClipboardDocumentListIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const sidebarOpen = ref(false)
const showNotifications = ref(false)
const notifications = ref([])

const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)

// Close notifications dropdown on navigation route change
watch(() => route.path, () => {
  showNotifications.value = false
})

const toggleNotificationsDropdown = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    fetchAlerts()
  }
}

const readNotificationIds = ref(JSON.parse(localStorage.getItem('read_notifications') || '[]'))

const saveReadNotifications = () => {
  localStorage.setItem('read_notifications', JSON.stringify(readNotificationIds.value))
}

const markAsRead = (id) => {
  const n = notifications.value.find(item => item.id === id)
  if (n) {
    n.read = true
    if (!readNotificationIds.value.includes(id)) {
      readNotificationIds.value.push(id)
      saveReadNotifications()
    }
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(n => {
    n.read = true
    if (!readNotificationIds.value.includes(n.id)) {
      readNotificationIds.value.push(n.id)
    }
  })
  saveReadNotifications()
}

const fetchAlerts = async () => {
  try {
    const alertsList = []
    
    const roleName = (authStore.user?.role?.name || '').toLowerCase()
    const isWaiter = roleName === 'waiter' || roleName === 'официант'
    const isCook = roleName === 'cook' || roleName === 'повар'

    // For waiter: show their order status updates
    if (isWaiter) {
      const ordersRes = await api.get('/bar/orders')
      const userId = authStore.user?.id
      ordersRes.data.forEach(o => {
        if (o.waiter_id === userId && o.status === 'ready') {
          const alertId = `order-ready-${o.id}`
          alertsList.push({
            id: alertId,
            title: `Заказ #${o.id} готов!`,
            description: `Заберите и доставьте к T-${o.lounger_id || 'стойка'}`,
            type: 'warning',
            time: 'Срочно',
            read: readNotificationIds.value.includes(alertId)
          })
        }
      })
    } else if (isCook) {
      // For cook: new orders waiting
      const ordersRes = await api.get('/bar/orders')
      ordersRes.data.forEach(o => {
        if (o.status === 'new') {
          const alertId = `order-new-${o.id}`
          alertsList.push({
            id: alertId,
            title: `Новый заказ #${o.id}`,
            description: `${o.items?.length || 0} позиций — начните готовить`,
            type: 'info',
            time: 'В очереди',
            read: readNotificationIds.value.includes(alertId)
          })
        }
      })
    } else {
      // Admin: pool + orders
      try {
        const poolRes = await api.get('/pool/')
        const now = new Date()
        poolRes.data.forEach(v => {
          if (v.status === 'active' && v.expected_exit_time) {
            const exitTime = new Date(v.expected_exit_time + 'Z')
            if (now > exitTime) {
              const overMinutes = Math.floor((now - exitTime) / 60000)
              const alertId = `pool-${v.id}`
              alertsList.push({
                id: alertId,
                title: `Просрочен браслет #${v.bracelet_number}`,
                description: `Гость ${v.client_name || 'без имени'} превысил время на ${overMinutes} мин.`,
                type: 'warning',
                time: 'Срочно',
                read: readNotificationIds.value.includes(alertId)
              })
            }
          }
        })
      } catch (e) {}

      const ordersRes = await api.get('/bar/orders')
      ordersRes.data.forEach(o => {
        if (o.status === 'new') {
          const alertId = `order-${o.id}`
          alertsList.push({
            id: alertId,
            title: `Новый заказ #${o.id}`,
            description: o.lounger_id 
              ? `Необходимо подать к топчану T-${o.lounger_id} (${o.total_amount} ₸)`
              : `Готов к выдаче на барной стойке (${o.total_amount} ₸)`,
            type: 'info',
            time: 'В очереди',
            read: readNotificationIds.value.includes(alertId)
          })
        }
      })
    }

    // Default welcome state
    if (alertsList.length === 0) {
      alertsList.push({
        id: 'system-status',
        title: 'Все зоны в норме',
        description: 'Нет новых уведомлений.',
        type: 'success',
        time: 'Система',
        read: true
      })
    }

    notifications.value = alertsList
  } catch (err) {
    console.error("Error loading alerts in layout", err)
  }
}

let alertsInterval;
onMounted(() => {
  fetchAlerts()
  alertsInterval = setInterval(fetchAlerts, 10000)
  window.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  clearInterval(alertsInterval)
  window.removeEventListener('click', closeDropdown)
})

const closeDropdown = (e) => {
  if (showNotifications.value && !e.target.closest('.relative')) {
    showNotifications.value = false
  }
}

// --- ROLE-BASED NAVIGATION ---
const allNavigation = [
  { name: 'Дашборд', routeName: 'Dashboard', to: '/', icon: HomeIcon, roles: ['admin'] },
  { name: 'Бассейн', routeName: 'Pool', to: '/pool', icon: UserGroupIcon, roles: ['admin'] },
  { name: 'Тапчаны', routeName: 'Loungers', to: '/loungers', icon: MapIcon, roles: ['admin'] },
  { name: 'Бар', routeName: 'Bar', to: '/bar', icon: BeakerIcon, roles: ['admin', 'bartender'] },
  { name: 'Бани & VIP', routeName: 'Steam', to: '/steam', icon: FireIcon, roles: ['admin'] },
  { name: 'Касса', routeName: 'Finance', to: '/finance', icon: BanknotesIcon, roles: ['admin', 'bartender'] },
  { name: 'Кухня', routeName: 'Kitchen', to: '/kitchen', icon: QueueListIcon, roles: ['admin', 'cook'] },
  { name: 'Персонал', routeName: 'Staff', to: '/staff', icon: UserPlusIcon, roles: ['admin'] },
  { name: 'Панель Официанта', routeName: 'Waiter', to: '/waiter', icon: ClipboardDocumentListIcon, roles: ['waiter'] },
]

const navigation = computed(() => {
  const user = authStore.user
  if (!user) return []

  const roleNameLower = (user.role?.name || '').toLowerCase()
  const isAdmin = roleNameLower === 'admin' || roleNameLower === 'админ' || user.role_id === 1

  const allowedTabsStr = user.role?.allowed_tabs || ''

  // Fallback to hardcoded role check if allowed_tabs is empty
  if (!allowedTabsStr) {
    if (isAdmin) {
      return allNavigation.filter(n => n.roles.includes('admin'))
    }
    let matchedRoleName = user.role?.name
    if (matchedRoleName === 'Повар') matchedRoleName = 'cook'
    if (matchedRoleName === 'Официант') matchedRoleName = 'waiter'
    if (matchedRoleName === 'Бармэн') matchedRoleName = 'bartender'
    if (matchedRoleName === 'Кассир') matchedRoleName = 'bartender'
    
    return allNavigation.filter(n => n.roles.includes(matchedRoleName))
  }

  const allowedList = allowedTabsStr.split(',')

  // Safety rule: Admin must always see the 'Staff' and 'Dashboard' tabs
  if (isAdmin) {
    if (!allowedList.includes('Staff')) allowedList.push('Staff')
    if (!allowedList.includes('Dashboard')) allowedList.push('Dashboard')
  }

  return allNavigation.filter(n => allowedList.includes(n.routeName))
})

const currentRouteName = computed(() => {
  const current = navigation.value.find(n => n.routeName === route.name)
  return current ? current.name : route.name
})

const userInitials = computed(() => {
  const name = authStore.user?.full_name || 'А Д'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.page-enter-active,
.page-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.98);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.98);
}

.animate-slow-spin {
  animation: spin 20s linear infinite;
}

.animate-slow-spin-reverse {
  animation: spin 25s linear infinite reverse;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
