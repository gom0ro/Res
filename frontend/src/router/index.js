import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    component: () => import('../components/common/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue')
      },
      {
        path: 'pool',
        name: 'Pool',
        component: () => import('../views/Pool.vue')
      },
      {
        path: 'loungers',
        name: 'Loungers',
        component: () => import('../views/Loungers.vue')
      },
      {
        path: 'bar',
        name: 'Bar',
        component: () => import('../views/Bar.vue')
      },
      {
        path: 'staff',
        name: 'Staff',
        component: () => import('../views/Staff.vue')
      },
      {
        path: 'steam',
        name: 'Steam',
        component: () => import('../views/Steam.vue')
      },
      {
        path: 'finance',
        name: 'Finance',
        component: () => import('../views/Finance.vue')
      },
      {
        path: 'kitchen',
        name: 'Kitchen',
        component: () => import('../views/Kitchen.vue')
      },
      {
        path: 'waiter',
        name: 'Waiter',
        component: () => import('../views/Waiter.vue')
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('../views/Analytics.vue')
      },
      {
        path: 'stock',
        name: 'Stock',
        component: () => import('../views/Stock.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // Redirect logged-in users based on role allowed tabs
    if (!authStore.user) {
      await authStore.fetchUser()
    }
    const user = authStore.user
    const roleNameLower = (user?.role?.name || '').toLowerCase()
    const isAdmin = roleNameLower === 'admin' || roleNameLower === 'админ' || user?.role_id === 1
    
    if (isAdmin) {
      next({ name: 'Dashboard' })
    } else {
      const allowedTabsStr = user?.role?.allowed_tabs || ''
      if (allowedTabsStr) {
        const allowedList = allowedTabsStr.split(',')
        const layoutRouteNames = ['Dashboard', 'Pool', 'Loungers', 'Bar', 'Steam', 'Finance', 'Kitchen', 'Staff', 'Waiter', 'Analytics', 'Stock']
        const firstAllowed = layoutRouteNames.find(name => allowedList.includes(name))
        if (firstAllowed) {
          next({ name: firstAllowed })
        } else {
          next({ name: 'Login' })
        }
      } else {
        const role = user?.role?.name
        if (role === 'waiter' || role === 'Официант') {
          next({ name: 'Waiter' })
        } else if (role === 'cook' || role === 'Повар') {
          next({ name: 'Kitchen' })
        } else {
          next({ name: 'Dashboard' })
        }
      }
    }
  } else if (to.meta.requiresAuth && isAuthenticated) {
    if (!authStore.user) {
      await authStore.fetchUser()
    }
    const user = authStore.user
    if (user) {
      const roleNameLower = (user.role?.name || '').toLowerCase()
      const isAdmin = roleNameLower === 'admin' || roleNameLower === 'админ' || user.role_id === 1
      
      if (!isAdmin) {
        const allowedTabsStr = user.role?.allowed_tabs || ''
        if (allowedTabsStr) {
          const allowedList = allowedTabsStr.split(',')
          const layoutRouteNames = ['Dashboard', 'Pool', 'Loungers', 'Bar', 'Steam', 'Finance', 'Kitchen', 'Staff', 'Waiter', 'Analytics', 'Stock']
          // If trying to access a page registered in the side navigation, ensure they are allowed
          if (layoutRouteNames.includes(to.name) && !allowedList.includes(to.name)) {
            const firstAllowed = layoutRouteNames.find(name => allowedList.includes(name))
            if (firstAllowed) {
              next({ name: firstAllowed })
            } else {
              authStore.logout()
              next({ name: 'Login' })
            }
            return
          }
        } else {
          // Backward compatibility fallback
          const role = user.role?.name
          const isWaiter = role === 'waiter' || role === 'Официант'
          const isCook = role === 'cook' || role === 'Повар'
          const isAdminPage = ['Dashboard', 'Pool', 'Loungers', 'Steam', 'Staff'].includes(to.name)
          
          if (isWaiter && (isAdminPage || to.name === 'Kitchen')) {
            next({ name: 'Waiter' })
            return
          }
          if (isCook && (isAdminPage || to.name === 'Waiter')) {
            next({ name: 'Kitchen' })
            return
          }
        }
      }
    }
    next()
  } else {
    next()
  }
})

export default router
