<template>
  <div class="flex h-[100dvh] max-h-[100dvh] overflow-hidden app-shell relative safe-top">

    <PremiumBackground />

    <!-- Mobile overlay -->
    <transition name="fade">
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 z-40 lg:hidden modal-overlay !items-stretch !p-0 !bg-black/50"
        @click="sidebarOpen = false"
      />
    </transition>

    <!-- Sidebar -->
    <aside
      class="glass-sidebar fixed lg:static inset-y-0 left-0 z-50 flex flex-col w-[min(18rem,88vw)] sm:w-[260px] max-w-[320px] transition-transform duration-300 lg:translate-x-0 shadow-2xl lg:shadow-none"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
      style="transition-timing-function: cubic-bezier(0.22, 1, 0.36, 1)"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 h-[4.25rem] shrink-0 border-b border-[var(--border-subtle)]">
        <div
          class="w-9 h-9 rounded-premium-lg flex items-center justify-center shrink-0"
          style="background: linear-gradient(135deg, var(--accent-from), var(--accent-to)); box-shadow: var(--glow-sm)"
        >
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-ink font-bold text-sm tracking-tight">Resort OS</p>
          <p class="text-ink-muted text-[10px] font-medium">Management</p>
        </div>
        <button class="lg:hidden ml-auto icon-btn" @click="sidebarOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto py-5 px-3 space-y-0.5 custom-scrollbar">
        <p class="text-[10px] font-semibold uppercase tracking-[0.14em] text-ink-muted px-3 mb-2.5">Навигация</p>

        <router-link
          v-for="(item, idx) in navigation"
          :key="item.name"
          :to="item.to"
          v-motion
          :initial="{ opacity: 0, x: -8 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: idx * 35, duration: 350 } }"
          class="nav-item group"
          :class="{ active: $route.name === item.routeName }"
          @click="sidebarOpen = false"
        >
          <component
            :is="item.icon"
            class="w-4 h-4 mr-3 shrink-0 transition-colors duration-300"
            :class="$route.name === item.routeName ? 'text-primary-400' : 'text-ink-muted group-hover:text-ink-secondary'"
          />
          <span>{{ item.name }}</span>
          <div
            v-if="$route.name === item.routeName"
            class="ml-auto w-1.5 h-1.5 rounded-full bg-primary-400"
            style="box-shadow: 0 0 8px rgba(99, 102, 241, 0.7)"
          />
        </router-link>
      </nav>

      <!-- User -->
      <div class="p-3 shrink-0 border-t border-[var(--border-subtle)]">
        <div class="flex items-center gap-3 p-3 rounded-premium-lg mb-2 glass">
          <div
            class="w-9 h-9 rounded-premium flex items-center justify-center text-white text-xs font-bold shrink-0"
            style="background: linear-gradient(135deg, var(--accent-from), var(--accent-to))"
          >
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-ink text-xs font-semibold truncate">{{ authStore.user?.full_name || 'Admin' }}</p>
            <p class="text-ink-muted text-[10px] truncate">{{ authStore.user?.email }}</p>
          </div>
        </div>
        <button
          class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-premium text-xs font-medium text-ink-muted hover:text-rose-400 transition-all duration-300 group"
          style="background: var(--surface-muted)"
          @click="logout"
        >
          <ArrowRightOnRectangleIcon class="w-4 h-4 transition-transform duration-300 group-hover:-translate-x-0.5"/>
          Выйти
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden relative z-10">

      <header class="glass-header shrink-0 flex items-center justify-between gap-2 px-3 sm:px-5 md:px-7 py-2.5 sm:py-0 sm:min-h-[4.25rem]">
        <div class="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
          <button class="lg:hidden icon-btn shrink-0" aria-label="Открыть меню" @click="sidebarOpen = true">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
          <div class="min-w-0">
            <h2 class="text-ink font-semibold text-sm sm:text-base tracking-tight truncate">{{ currentRouteName }}</h2>
            <p class="text-ink-muted text-[10px] font-medium hidden sm:block">Resort Management</p>
          </div>
        </div>

        <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
          <ThemeToggle />

          <div class="relative notifications-root">
            <button
              class="icon-btn relative"
              aria-label="Уведомления"
              :class="{ '!bg-[var(--surface-hover)] !text-ink': showNotifications }"
              @click.stop="toggleNotificationsDropdown"
            >
              <BellIcon class="w-5 h-5 transition-transform duration-300 hover:rotate-12"/>
              <span
                v-if="unreadCount > 0"
                class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500"
                style="box-shadow: 0 0 8px rgba(244, 63, 94, 0.7)"
              />
            </button>

            <transition name="dropdown">
              <div
                v-if="showNotifications"
                class="notifications-panel fixed left-3 right-3 top-[4.25rem] z-[60] sm:absolute sm:left-auto sm:right-0 sm:top-12 sm:w-80 sm:max-w-[calc(100vw-2rem)] rounded-premium-xl overflow-hidden glass-card glass-card--flat !shadow-modal max-h-[min(70dvh,24rem)] flex flex-col"
              >
                <div class="flex items-center justify-between px-4 py-3 border-b border-[var(--border-subtle)]">
                  <span class="text-ink text-xs font-semibold">Уведомления</span>
                  <button
                    v-if="unreadCount > 0"
                    class="text-[10px] text-primary-400 hover:text-primary-500 font-semibold transition-colors"
                    @click="markAllAsRead"
                  >
                    Прочитать все
                  </button>
                </div>

                <div class="flex-1 min-h-0 overflow-y-auto custom-scrollbar p-2 space-y-1">
                  <div
                    v-for="n in notifications"
                    :key="n.id"
                    class="p-3 rounded-premium-lg transition-all duration-200"
                    :class="n.read ? 'opacity-50' : 'hover:bg-[var(--surface-hover)]'"
                    :style="!n.read ? { background: 'var(--surface-muted)' } : {}"
                  >
                    <div class="flex gap-3">
                      <div
                        class="mt-1 w-1.5 h-1.5 rounded-full shrink-0"
                        :class="{
                          'bg-rose-400': n.type === 'warning',
                          'bg-emerald-400': n.type === 'success',
                          'bg-blue-400': n.type === 'info',
                        }"
                        :style="!n.read ? 'box-shadow: 0 0 6px currentColor' : ''"
                      />
                      <div class="flex-1 min-w-0">
                        <p class="text-ink text-xs font-semibold truncate">{{ n.title }}</p>
                        <p class="text-ink-muted text-[11px] mt-0.5 leading-relaxed">{{ n.description }}</p>
                        <div class="flex items-center justify-between mt-2">
                          <span class="text-ink-muted text-[10px]">{{ n.time }}</span>
                          <button
                            v-if="!n.read"
                            class="text-[10px] text-primary-400 font-semibold hover:text-primary-500"
                            @click="markAsRead(n.id)"
                          >
                            Ок
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <div class="hidden sm:flex items-center gap-2.5 px-3 py-2 rounded-premium-lg glass">
            <div
              class="w-7 h-7 rounded-lg flex items-center justify-center text-white text-[10px] font-bold"
              style="background: linear-gradient(135deg, var(--accent-from), var(--accent-to))"
            >
              {{ userInitials }}
            </div>
            <span class="text-ink-secondary text-xs font-medium">
              {{ authStore.user?.full_name?.split(' ')[0] || 'Admin' }}
            </span>
          </div>
        </div>
      </header>

      <div class="flex-1 min-h-0 overflow-y-auto overflow-x-hidden custom-scrollbar p-3 sm:p-5 md:p-8 safe-bottom">
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
import PremiumBackground from '../ui/PremiumBackground.vue'
import ThemeToggle from '../ui/ThemeToggle.vue'
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
  ClipboardDocumentListIcon,
  ChartBarIcon,
  ArchiveBoxIcon,
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const sidebarOpen = ref(false)
const showNotifications = ref(false)
const notifications = ref([])

const unreadCount = computed(() => notifications.value.filter((n) => !n.read).length)

watch(() => route.path, () => {
  showNotifications.value = false
  sidebarOpen.value = false
})

watch(sidebarOpen, (open) => {
  if (typeof document === 'undefined') return
  document.body.style.overflow = open ? 'hidden' : ''
  document.body.style.touchAction = open ? 'none' : ''
})

const toggleNotificationsDropdown = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) fetchAlerts()
}

const readNotificationIds = ref(JSON.parse(localStorage.getItem('read_notifications') || '[]'))

const saveReadNotifications = () => {
  localStorage.setItem('read_notifications', JSON.stringify(readNotificationIds.value))
}

const markAsRead = (id) => {
  const n = notifications.value.find((item) => item.id === id)
  if (n) {
    n.read = true
    if (!readNotificationIds.value.includes(id)) {
      readNotificationIds.value.push(id)
      saveReadNotifications()
    }
  }
}

const markAllAsRead = () => {
  notifications.value.forEach((n) => {
    n.read = true
    if (!readNotificationIds.value.includes(n.id)) readNotificationIds.value.push(n.id)
  })
  saveReadNotifications()
}

const fetchAlerts = async () => {
  try {
    const alertsList = []
    const roleName = (authStore.user?.role?.name || '').toLowerCase()
    const isWaiter = roleName === 'waiter' || roleName === 'официант'
    const isCook = roleName === 'cook' || roleName === 'повар'

    if (isWaiter) {
      const ordersRes = await api.get('/bar/orders')
      const userId = authStore.user?.id
      ordersRes.data.forEach((o) => {
        if (o.waiter_id === userId && o.status === 'ready') {
          const alertId = `order-ready-${o.id}`
          alertsList.push({
            id: alertId,
            title: `Заказ #${o.id} готов!`,
            description: `Доставьте к T-${o.lounger_id || 'стойка'}`,
            type: 'warning',
            time: 'Срочно',
            read: readNotificationIds.value.includes(alertId),
          })
        }
      })
    } else if (isCook) {
      const ordersRes = await api.get('/bar/orders')
      ordersRes.data.forEach((o) => {
        if (o.status === 'new') {
          const alertId = `order-new-${o.id}`
          alertsList.push({
            id: alertId,
            title: `Новый заказ #${o.id}`,
            description: `${o.items?.length || 0} позиций`,
            type: 'info',
            time: 'В очереди',
            read: readNotificationIds.value.includes(alertId),
          })
        }
      })
    } else {
      try {
        const poolRes = await api.get('/pool/')
        const now = new Date()
        poolRes.data.forEach((v) => {
          if (v.status === 'active' && v.expected_exit_time) {
            const exitTime = new Date(v.expected_exit_time + 'Z')
            if (now > exitTime) {
              const overMinutes = Math.floor((now - exitTime) / 60000)
              const alertId = `pool-${v.id}`
              alertsList.push({
                id: alertId,
                title: `Браслет #${v.bracelet_number} просрочен`,
                description: `${v.client_name || 'Гость'} — +${overMinutes} мин.`,
                type: 'warning',
                time: 'Срочно',
                read: readNotificationIds.value.includes(alertId),
              })
            }
          }
        })
      } catch (e) { /* pool optional */ }
      const ordersRes = await api.get('/bar/orders')
      ordersRes.data.forEach((o) => {
        if (o.status === 'new') {
          const alertId = `order-${o.id}`
          alertsList.push({
            id: alertId,
            title: `Новый заказ #${o.id}`,
            description: o.lounger_id
              ? `Топчан T-${o.lounger_id} · ${o.total_amount} ₸`
              : `Барная стойка · ${o.total_amount} ₸`,
            type: 'info',
            time: 'В очереди',
            read: readNotificationIds.value.includes(alertId),
          })
        }
      })
    }

    if (alertsList.length === 0) {
      alertsList.push({
        id: 'system-ok',
        title: 'Всё в порядке',
        description: 'Нет новых уведомлений',
        type: 'success',
        time: 'Система',
        read: true,
      })
    }
    notifications.value = alertsList
  } catch (err) {
    console.error(err)
  }
}

let alertsInterval
onMounted(() => {
  fetchAlerts()
  alertsInterval = setInterval(fetchAlerts, 10000)
  window.addEventListener('click', closeDropdown)
})
onUnmounted(() => {
  clearInterval(alertsInterval)
  window.removeEventListener('click', closeDropdown)
  document.body.style.overflow = ''
  document.body.style.touchAction = ''
})

const closeDropdown = (e) => {
  if (showNotifications.value && !e.target.closest('.notifications-root')) {
    showNotifications.value = false
  }
}

const allNavigation = [
  { name: 'Дашборд', routeName: 'Dashboard', to: '/', icon: HomeIcon, roles: ['admin'] },
  { name: 'Бассейн', routeName: 'Pool', to: '/pool', icon: UserGroupIcon, roles: ['admin'] },
  { name: 'Топчаны', routeName: 'Loungers', to: '/loungers', icon: MapIcon, roles: ['admin'] },
  { name: 'Бар', routeName: 'Bar', to: '/bar', icon: BeakerIcon, roles: ['admin', 'bartender'] },
  { name: 'Бани & VIP', routeName: 'Steam', to: '/steam', icon: FireIcon, roles: ['admin'] },
  { name: 'Касса', routeName: 'Finance', to: '/finance', icon: BanknotesIcon, roles: ['admin', 'bartender'] },
  { name: 'Кухня', routeName: 'Kitchen', to: '/kitchen', icon: QueueListIcon, roles: ['admin', 'cook'] },
  { name: 'Персонал', routeName: 'Staff', to: '/staff', icon: UserPlusIcon, roles: ['admin'] },
  { name: 'Аналитика', routeName: 'Analytics', to: '/analytics', icon: ChartBarIcon, roles: ['admin'] },
  { name: 'Склад', routeName: 'Stock', to: '/stock', icon: ArchiveBoxIcon, roles: ['admin'] },
  { name: 'Панель Официанта', routeName: 'Waiter', to: '/waiter', icon: ClipboardDocumentListIcon, roles: ['waiter'] },
]

const navigation = computed(() => {
  const user = authStore.user
  if (!user) return []
  const roleNameLower = (user.role?.name || '').toLowerCase()
  const isAdmin = roleNameLower === 'admin' || roleNameLower === 'админ' || user.role_id === 1
  const allowedTabsStr = user.role?.allowed_tabs || ''

  if (!allowedTabsStr) {
    if (isAdmin) return allNavigation.filter((n) => n.roles.includes('admin'))
    let r = user.role?.name
    if (r === 'Повар') r = 'cook'
    if (r === 'Официант') r = 'waiter'
    if (r === 'Бармэн' || r === 'Кассир') r = 'bartender'
    return allNavigation.filter((n) => n.roles.includes(r))
  }
  if (isAdmin) return allNavigation.filter((n) => n.roles.includes('admin'))
  const allowedList = allowedTabsStr.split(',')
  return allNavigation.filter((n) => allowedList.includes(n.routeName))
})

const currentRouteName = computed(() => {
  const current = navigation.value.find((n) => n.routeName === route.name)
  return current ? current.name : route.name
})

const userInitials = computed(() => {
  const name = authStore.user?.full_name || 'AD'
  return name.split(' ').map((n) => n[0]).join('').substring(0, 2).toUpperCase()
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dropdown-enter-active { transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1); }
.dropdown-leave-active { transition: all 0.18s ease-in; }
.dropdown-enter-from { opacity: 0; transform: translateY(-8px) scale(0.98); }
.dropdown-leave-to { opacity: 0; transform: translateY(-4px) scale(0.99); }

.fade-enter-active { transition: opacity 0.25s ease; }
.fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
