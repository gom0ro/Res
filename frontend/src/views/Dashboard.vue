<template>
  <div class="page-content page-stack">

    <PageHeader :title="'Обзор'" :subtitle="todayShort">
      <template #badge>
        <span class="badge badge-success w-full sm:w-auto justify-center">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse-soft"/>
          Система активна
        </span>
      </template>
    </PageHeader>

    <!-- KPI -->
    <div class="stats-grid">
      <template v-if="loading">
        <div v-for="i in 4" :key="i" class="glass-card rounded-premium-xl p-4 sm:p-6 glass-card--flat">
          <Skeleton width="2.25rem" height="2.25rem" rounded="xl" class="mb-4" />
          <Skeleton width="60%" height="1.75rem" class="mb-2" />
          <Skeleton width="40%" height="0.75rem" />
        </div>
      </template>
      <GlassCard
        v-else
        v-for="(stat, i) in stats"
        :key="stat.name"
        tag="div"
        class="stat-card stat-card-compact group cursor-default !p-4 sm:!p-6"
        :delay="i * 60"
        :hoverable="true"
      >
        <div
          class="absolute inset-0 rounded-premium-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
          :style="`background: radial-gradient(circle at 50% 0%, ${stat.glow}12, transparent 70%)`"
        />
        <div class="relative z-10">
          <div class="flex items-start justify-between gap-2 mb-3 sm:mb-4">
            <div
              class="w-9 h-9 sm:w-10 sm:h-10 rounded-premium-lg flex items-center justify-center shrink-0"
              :style="`background:${stat.glow}12;border:1px solid ${stat.glow}22`"
            >
              <component :is="stat.icon" class="w-4 h-4 sm:w-[1.125rem] sm:h-[1.125rem]" :style="`color:${stat.glow}`"/>
            </div>
            <span
              class="text-[10px] sm:text-[11px] font-semibold px-2 py-0.5 rounded-lg shrink-0"
              style="color: #34d399; background: rgba(16,185,129,0.1)"
            >
              {{ stat.change }}
            </span>
          </div>
          <p class="text-xl sm:text-2xl font-bold text-ink tracking-tight leading-none break-words">{{ stat.value }}</p>
          <p class="text-ink-muted text-[11px] sm:text-xs mt-1.5 sm:mt-2 font-medium leading-snug">{{ stat.name }}</p>
        </div>
      </GlassCard>
    </div>

    <!-- Main grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-5 md:gap-6">
      <GlassCard
        tag="section"
        class="lg:col-span-2 overflow-hidden !p-0 glass-card--flat"
        :delay="280"
        :hoverable="false"
      >
        <div class="flex items-center justify-between gap-2 px-4 sm:px-6 py-3.5 sm:py-4 border-b border-[var(--border-subtle)]">
          <div class="flex items-center gap-2 min-w-0">
            <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse-soft shrink-0" style="box-shadow: 0 0 8px rgba(59,130,246,0.6)"/>
            <h3 class="text-ink font-semibold text-sm truncate">Активные в бассейне</h3>
            <span class="badge badge-live shrink-0">{{ visitsLoading ? '…' : activeVisits.length }}</span>
          </div>
          <router-link to="/pool" class="text-xs text-ink-muted hover:text-primary-400 font-medium transition-colors shrink-0">
            Все →
          </router-link>
        </div>

        <div class="p-3 sm:p-5 space-y-1">
          <template v-if="visitsLoading">
            <div v-for="i in 3" :key="i" class="flex items-center gap-3 p-3">
              <Skeleton width="2.5rem" height="2.5rem" rounded="xl" />
              <div class="flex-1 space-y-2">
                <Skeleton width="50%" height="0.875rem" />
                <Skeleton width="35%" height="0.625rem" />
              </div>
              <Skeleton width="4rem" height="1.25rem" />
            </div>
          </template>

          <div
            v-else
            v-for="(v, i) in activeVisits.slice(0, 5)"
            :key="v.id"
            v-motion
            :initial="{ opacity: 0, x: -6 }"
            :enter="{ opacity: 1, x: 0, transition: { delay: 320 + i * 45, duration: 380 } }"
            class="list-row-responsive flex items-center gap-3 sm:gap-4 p-3 sm:p-3.5 rounded-premium-lg cursor-pointer transition-all duration-300 hover:bg-[var(--surface-hover)] group"
            @click="$router.push('/pool')"
          >
            <div
              class="w-10 h-10 sm:w-11 sm:h-11 rounded-premium-lg flex items-center justify-center text-blue-400 font-bold text-sm shrink-0"
              style="background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.15)"
            >
              {{ v.bracelet_number }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-ink text-sm font-semibold truncate">{{ v.client_name || 'Гость' }}</p>
              <p class="text-ink-muted text-xs mt-0.5 truncate">{{ getTariffLabel(v.tariff_type) }} · {{ formatTime(v.entry_time) }}</p>
            </div>
            <div class="list-row-responsive__end sm:list-row-responsive__end-none text-right shrink-0 sm:border-0 sm:block sm:w-auto sm:pt-0">
              <p class="text-ink text-sm font-bold tabular-nums">{{ v.total_amount.toLocaleString() }} ₸</p>
              <span class="text-[10px] text-blue-400/90 font-semibold">В бассейне</span>
            </div>
          </div>

          <div v-if="!visitsLoading && activeVisits.length === 0" class="flex flex-col items-center justify-center py-12 sm:py-14 text-ink-muted">
            <UserGroupIcon class="w-10 h-10 mb-3 opacity-30"/>
            <p class="text-sm font-medium">Нет активных посетителей</p>
          </div>
        </div>
      </GlassCard>

      <GlassCard tag="section" padding="lg" class="!p-4 sm:!p-5 md:!p-6" :delay="360" :hoverable="false">
        <h3 class="text-ink font-semibold text-sm mb-4 sm:mb-5">Быстрые действия</h3>
        <div class="grid grid-cols-2 gap-2.5 sm:gap-3">
          <button
            v-for="(action, i) in quickActions"
            :key="action.label"
            v-motion
            :initial="{ opacity: 0, scale: 0.96 }"
            :enter="{ opacity: 1, scale: 1, transition: { delay: 400 + i * 50, duration: 350 } }"
            class="flex flex-col items-center gap-2.5 sm:gap-3 p-3.5 sm:p-4 rounded-premium-lg transition-colors duration-300 text-center group min-h-[5.5rem]"
            :style="`background:${action.color}08;border:1px solid ${action.color}18`"
            @click="$router.push(action.to)"
          >
            <div
              class="w-10 h-10 sm:w-11 sm:h-11 rounded-premium-lg flex items-center justify-center"
              :style="`background:${action.color}14`"
            >
              <component :is="action.icon" class="w-5 h-5" :style="`color:${action.color}`"/>
            </div>
            <span class="text-[11px] sm:text-xs font-semibold text-ink-muted group-hover:text-ink transition-colors leading-tight">
              {{ action.label }}
            </span>
          </button>
        </div>
      </GlassCard>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../stores/auth'
import PageHeader from '../components/ui/PageHeader.vue'
import GlassCard from '../components/ui/GlassCard.vue'
import Skeleton from '../components/ui/Skeleton.vue'
import {
  CurrencyDollarIcon,
  UserGroupIcon,
  MapIcon,
  ShoppingCartIcon,
  UserPlusIcon,
  BeakerIcon,
  FireIcon,
} from '@heroicons/vue/24/outline'

const stats = ref([
  { name: 'Выручка сегодня', value: '—', icon: CurrencyDollarIcon, change: '+12%', glow: '#10b981', key: 'daily_revenue' },
  { name: 'В бассейне', value: '0', icon: UserGroupIcon, change: '+5%', glow: '#3b82f6', key: 'active_pool_guests' },
  { name: 'Занятость топчанов', value: '0%', icon: MapIcon, change: '+2%', glow: '#8b5cf6', key: 'loungers_occupancy' },
  { name: 'Активные заказы', value: '0', icon: ShoppingCartIcon, change: '+18%', glow: '#f59e0b', key: 'active_orders' },
])

const activeVisits = ref([])
const loading = ref(true)
const visitsLoading = ref(true)

const todayShort = computed(() =>
  new Date().toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', weekday: 'short' })
)

const quickActions = [
  { label: 'Новый гость', to: '/pool', icon: UserPlusIcon, color: '#3b82f6' },
  { label: 'Новый заказ', to: '/bar', icon: BeakerIcon, color: '#10b981' },
  { label: 'Топчан', to: '/loungers', icon: MapIcon, color: '#8b5cf6' },
  { label: 'Бани & VIP', to: '/steam', icon: FireIcon, color: '#f59e0b' },
]

onMounted(async () => {
  await Promise.all([fetchStats(), fetchActivePoolVisits()])
})

const fetchStats = async () => {
  loading.value = true
  try {
    const res = await api.get('/dashboard/stats')
    stats.value.forEach((stat) => {
      if (res.data[stat.key] !== undefined) stat.value = res.data[stat.key]
    })
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const fetchActivePoolVisits = async () => {
  visitsLoading.value = true
  try {
    const res = await api.get('/pool/')
    activeVisits.value = res.data.filter((v) => v.status === 'active')
  } catch (err) {
    console.error(err)
  } finally {
    visitsLoading.value = false
  }
}

const formatTime = (iso) => {
  if (!iso) return '-'
  return new Date(iso + 'Z').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getTariffLabel = (t) =>
  ({ adult: 'Взрослый', child: 'Детский', daily: 'Безлимит', vip: 'VIP', hourly: 'Часовой' }[t] || t)
</script>

<style scoped>
@media (min-width: 481px) {
  .list-row-responsive__end-none {
    width: auto;
    display: block;
    border-top: none;
    padding-top: 0;
  }
}
</style>
