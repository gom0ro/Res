<template>
  <div class="page-content flex flex-col min-h-0 flex-1 space-y-3 sm:space-y-4">
    <!-- Header -->
    <div class="page-toolbar">
      <div>
        <h1 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Касса Бара</h1>
        <p class="text-gray-400 font-medium">POS Терминал & Прием заказов</p>
      </div>
      <div class="page-toolbar__actions">
        <!-- Tab Toggle -->
        <div class="bg-dark-surface border border-dark-border p-1 rounded-xl flex w-full sm:w-auto">
          <button 
            @click="activeTab = 'pos'"
            class="flex-1 sm:flex-none px-4 py-2 text-sm font-bold rounded-lg transition-colors"
            :class="activeTab === 'pos' ? 'bg-orange-600 text-white shadow' : 'text-gray-400 hover:text-white'"
          >
            Продажи
          </button>
          <button 
            @click="activeTab = 'orders'"
            class="flex-1 sm:flex-none px-4 py-2 text-sm font-bold rounded-lg transition-colors relative"
            :class="activeTab === 'orders' ? 'bg-orange-600 text-white shadow' : 'text-gray-400 hover:text-white'"
          >
            Заказы официантов
            <span v-if="pendingOrdersCount > 0" class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-red-500 rounded-full border border-dark-surface text-[10px] font-black text-white flex items-center justify-center animate-bounce">
              {{ pendingOrdersCount }}
            </span>
          </button>
        </div>
        <button @click="showCategoryModal = true; fetchCategories()" class="flex-1 sm:flex-none px-5 py-3 bg-dark-surface border border-dark-border hover:bg-white/5 text-gray-300 rounded-xl font-bold text-xs sm:text-sm text-center transition-all duration-300 hover:-translate-y-0.5">
          Категории
        </button>
        <button @click="showAddModal = true" class="flex-1 sm:flex-none px-6 py-3 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold text-xs sm:text-sm text-center shadow-lg shadow-orange-500/20 transition-all duration-300 hover:-translate-y-0.5">
          Добавить товар
        </button>
      </div>
    </div>
    
    <!-- POS Terminal Tab -->
    <div v-if="activeTab === 'pos'" class="flex flex-col lg:flex-row gap-4 sm:gap-6 flex-1 min-h-0">
      <!-- Sub-tabs for Mobile/Tablet POS View -->
      <div class="lg:hidden flex gap-2 mb-2 bg-dark-surface/50 border border-dark-border p-1 rounded-xl shrink-0">
        <button 
          @click="posSubTab = 'catalog'"
          type="button"
          class="flex-1 py-2.5 text-xs font-bold rounded-lg transition-all"
          :class="posSubTab === 'catalog' ? 'bg-orange-600 text-white shadow' : 'text-gray-400 hover:text-white'"
        >
          <MenuIcon class="w-5 h-5 mr-1 inline-block"/> Меню
        </button>
        <button 
          @click="posSubTab = 'cart'"
          type="button"
          class="flex-1 py-2.5 text-xs font-bold rounded-lg transition-all flex items-center justify-center gap-1.5"
          :class="[
            posSubTab === 'cart' ? 'bg-orange-600 text-white shadow' : 'text-gray-400 hover:text-white',
            { 'scale-105 bg-orange-600/20 text-orange-400 transition-transform': cartAnimated }
          ]"
        >
          <span><ShoppingCartIcon class="w-5 h-5 inline-block mr-1"/> Корзина</span>
          <span v-if="cart.length > 0" class="px-2 py-0.5 bg-orange-500/20 text-orange-400 rounded-md text-[10px] font-black border border-orange-500/30">
            {{ cart.reduce((acc, item) => acc + item.quantity, 0) }}
          </span>
        </button>
      </div>

      <!-- Products Catalog -->
      <div :class="[posSubTab === 'catalog' ? 'flex' : 'hidden lg:flex', 'flex-1 glass-dark rounded-2xl sm:rounded-3xl border border-dark-border p-4 sm:p-6 flex-col overflow-hidden min-h-[min(58dvh,28rem)] lg:min-h-0 lg:h-full']">
        <!-- Search bar -->
        <div class="relative mb-4">
          <input type="text" v-model="searchQuery" placeholder="Поиск по названию или штрихкоду..." class="w-full pl-12 pr-4 py-3 bg-dark-surface/50 border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500 transition-all">
          <svg class="w-5 h-5 text-gray-500 absolute left-4 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </div>

        <!-- Categories horizontal scroll -->
        <div class="flex gap-2 overflow-x-auto pb-3 mb-4 custom-scrollbar whitespace-nowrap shrink-0">
          <button 
            @click="selectedCategoryId = null"
            class="px-4 py-2 text-xs font-bold rounded-xl border transition-all flex items-center gap-1.5"
            :class="selectedCategoryId === null ? 'bg-orange-600 border-orange-600 text-white' : 'bg-dark-surface/50 border-dark-border text-gray-400 hover:text-white'"
          >
            <UtensilsIcon class="w-5 h-5 inline-block"/>
            <span>Все товары</span>
          </button>
          <button 
            v-for="cat in categories" :key="cat.id"
            @click="selectedCategoryId = cat.id"
            class="px-4 py-2 text-xs font-bold rounded-xl border transition-all flex items-center gap-1.5"
            :class="selectedCategoryId === cat.id ? 'bg-orange-600 border-orange-600 text-white' : 'bg-dark-surface/50 border-dark-border text-gray-400 hover:text-white'"
            :style="selectedCategoryId === cat.id ? {} : { borderColor: cat.color ? cat.color + '40' : undefined, color: cat.color || undefined }"
          >
            <UtensilsIcon class="w-4 h-4" :style="selectedCategoryId === cat.id ? {} : { color: cat.color || undefined }"/>
            <span>{{ cat.name }}</span>
          </button>
        </div>

        <!-- Products list -->
        <div class="overflow-y-auto custom-scrollbar flex-1 pr-2">
          <div class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-4 gap-4">
            <div 
              v-for="p in filteredProducts" :key="p.id"
              @click="addToCart(p)"
              class="bg-dark-surface/30 border border-dark-border rounded-2xl p-4 cursor-pointer hover:border-orange-500/50 hover:bg-orange-500/5 transition-all group active:scale-95"
            >
              <div class="h-20 bg-dark-bg rounded-xl mb-3 flex items-center justify-center text-orange-500/30 group-hover:text-orange-500/50 transition-colors">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>
              </div>
              <h4 class="text-white font-bold text-sm leading-tight mb-1">{{ p.name }}</h4>
              <p class="text-orange-400 font-black">{{ p.price }} ₸</p>
              <p class="text-xs text-gray-500 mt-1">Остаток: {{ p.stock_quantity }}</p>
            </div>
          </div>
          <div v-if="filteredProducts.length === 0" class="text-center py-10 text-gray-500">
            Товары в этой категории отсутствуют
          </div>
        </div>
      </div>

      <!-- Current POS Cart -->
      <div :class="[posSubTab === 'cart' ? 'flex' : 'hidden lg:flex', 'w-full lg:w-96 glass-dark rounded-2xl sm:rounded-3xl border border-dark-border flex-col overflow-hidden shrink-0 min-h-[min(50dvh,24rem)] lg:min-h-0 lg:h-full']">
        <div class="p-6 border-b border-dark-border bg-white/5">
          <h3 class="text-xl font-bold text-white tracking-tight">Текущий заказ</h3>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-4">
          <div v-for="(item, idx) in cart" :key="idx" class="flex justify-between items-center group animate-fade-in">
            <div class="flex-1 pr-2">
              <p class="text-white font-bold text-sm truncate">{{ item.product.name }}</p>
              <p class="text-xs text-gray-400">{{ item.product.price }} ₸</p>
            </div>
            <div class="flex items-center gap-3">
              <div class="flex items-center bg-dark-bg rounded-lg border border-dark-border">
                <button @click="decreaseQty(idx)" class="px-2.5 py-1 text-gray-400 hover:text-white transition-colors">-</button>
                <span class="text-white font-bold text-sm w-6 text-center">{{ item.quantity }}</span>
                <button @click="increaseQty(idx)" class="px-2.5 py-1 text-gray-400 hover:text-white transition-colors">+</button>
              </div>
              <p class="text-orange-400 font-bold text-sm w-16 text-right">{{ item.product.price * item.quantity }} ₸</p>
            </div>
          </div>
          <div v-if="cart.length === 0" class="h-full flex flex-col items-center justify-center text-gray-500 opacity-50">
            <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            <p class="font-bold text-sm">Корзина пуста</p>
          </div>
        </div>

        <div class="p-6 border-t border-dark-border bg-dark-surface/50">
          <div class="space-y-2 mb-4">
            <div class="flex justify-between text-sm">
              <span class="text-gray-400">Подытог:</span>
              <span class="text-white font-bold">{{ subtotal }} ₸</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-400">Обслуживание (0% у стойки):</span>
              <span class="text-orange-400 font-bold">{{ serviceFee }} ₸</span>
            </div>
            <div class="h-px bg-dark-border my-2"></div>
            <div class="flex justify-between text-lg">
              <span class="text-gray-300 font-bold">К оплате:</span>
              <span class="text-white font-black text-2xl">{{ total }} ₸</span>
            </div>
          </div>
          <button @click="checkout" :disabled="cart.length === 0" class="w-full py-4 bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white rounded-xl font-bold text-lg shadow-lg shadow-orange-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed transform active:scale-95">
            Пробить чек (Оплатить)
          </button>
        </div>
      </div>
    </div>

    <!-- Waiter Orders Tab -->
    <div v-else class="glass-dark border border-dark-border rounded-2xl sm:rounded-3xl p-4 sm:p-6 flex flex-col flex-1 overflow-hidden min-h-[min(55dvh,26rem)] lg:min-h-[20rem]">
      <h3 class="text-xl font-bold text-white tracking-tight mb-4">Активные заказы официантов ({{ waiterOrders.length }})</h3>
      
      <div class="overflow-y-auto custom-scrollbar flex-1 pr-2 space-y-4">
        <div 
          v-for="o in waiterOrders" 
          :key="o.id" 
          class="p-5 bg-dark-surface/30 border border-dark-border/80 rounded-2xl flex flex-col md:flex-row md:justify-between md:items-center gap-4 hover:border-orange-500/30 transition-all"
        >
          <div class="space-y-2">
            <div class="flex flex-wrap items-center gap-2">
              <span class="text-lg font-black text-white">Заказ #{{ o.id }}</span>
              <span 
                class="px-2.5 py-0.5 rounded-lg text-xs font-bold uppercase tracking-wider"
                :class="getStatusBadgeClass(o.status)"
              >
                {{ getStatusLabel(o.status) }}
              </span>
              <span v-if="o.is_paid" class="px-2.5 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg text-xs font-bold uppercase">
                Оплачено
              </span>
              <span v-else class="px-2.5 py-0.5 bg-red-500/10 text-red-400 border border-red-500/20 rounded-lg text-xs font-bold uppercase">
                Не оплачено
              </span>
            </div>
            
            <p class="text-sm font-black text-orange-400">
              Локация: {{ o.lounger_id ? `Топчан T-${o.lounger_id}` : 'Барная стойка' }}
            </p>

            <div class="flex flex-wrap gap-2 text-xs text-gray-400 font-semibold mt-1">
              <span v-for="item in o.items" :key="item.id" class="px-2 py-1 bg-white/5 border border-white/5 rounded-lg">
                {{ item.product?.name || 'Товар' }} × {{ item.quantity }}
              </span>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-4 justify-between md:justify-end w-full md:w-auto">
            <div class="text-right">
              <p class="text-xs text-gray-500 font-bold uppercase tracking-wider">К оплате</p>
              <p class="text-xl font-black text-white">{{ o.total_amount }} ₸</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <button 
                v-if="o.status === 'new'" 
                @click="updateStatus(o.id, 'preparing')" 
                class="px-4 py-2 bg-blue-500/20 text-blue-400 hover:bg-blue-500 hover:text-white font-bold text-sm rounded-lg transition-colors"
              >
                Готовить
              </button>
              <button 
                v-if="o.status === 'preparing'" 
                @click="updateStatus(o.id, 'ready')" 
                class="px-4 py-2 bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500 hover:text-white font-bold text-sm rounded-lg transition-colors"
              >
                Готов к выдаче
              </button>
              <button 
                v-if="!o.is_paid" 
                @click="updateStatus(o.id, 'paid', true)" 
                class="px-4 py-2 bg-green-500/20 text-green-400 hover:bg-green-500 hover:text-white font-bold text-sm rounded-lg transition-colors"
              >
                Оплатить & Выдать
              </button>
            </div>
          </div>
        </div>

        <div v-if="waiterOrders.length === 0" class="text-center py-20 text-gray-500">
          Активные заказы официантов отсутствуют
        </div>
      </div>
    </div>

    <!-- Modal for Adding Product -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-md w-full shadow-2xl relative">
        <button @click="showAddModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>
        <h3 class="text-2xl font-bold text-white mb-6">Новый товар</h3>
        <form @submit.prevent="createProduct" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Название товара</label>
            <input v-model="newProduct.name" required type="text" placeholder="Например: Смузи Ягодный" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
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
              <label class="block text-sm font-semibold text-gray-300 mb-2">Остаток на складе</label>
              <input v-model.number="newProduct.stock_quantity" required type="number" min="0" class="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-xl text-white outline-none focus:ring-2 focus:ring-orange-500">
            </div>
          </div>
          <button type="submit" class="w-full py-3 bg-orange-600 hover:bg-orange-500 text-white rounded-xl font-bold shadow-lg transition-colors mt-4">Добавить в меню</button>
        </form>
      </div>
    </div>

    <!-- Modal for Managing Categories -->
    <div v-if="showCategoryModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-dark-surface border border-dark-border rounded-3xl p-8 max-w-md w-full shadow-2xl relative flex flex-col max-h-[90vh]">
        <button @click="showCategoryModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-white"><XIcon class="w-5 h-5"/></button>
        <h3 class="text-2xl font-bold text-white mb-4">Управление категориями</h3>
        
        <!-- List of Categories -->
        <div class="flex-1 overflow-y-auto custom-scrollbar mb-6 pr-1 space-y-2 max-h-[300px]">
          <div v-for="(cat, idx) in categories" :key="cat.id" class="p-3 bg-dark-bg border border-dark-border/50 rounded-xl flex items-center justify-between">
            <!-- View Mode -->
            <div v-if="editingCategoryId !== cat.id" class="flex-1 flex justify-between items-center">
              <div>
                <p class="text-white font-bold text-sm flex items-center gap-2">
                  <UtensilsIcon class="w-4 h-4" :style="{ color: cat.color || undefined }"/>
                  <span>{{ cat.name }}</span>
                </p>
                <p v-if="cat.description" class="text-xs text-gray-400">{{ cat.description }}</p>
              </div>
              <div class="flex gap-1 items-center">
                <!-- Move Up -->
                <button 
                  @click="moveCategory(idx, -1)" 
                  :disabled="idx === 0"
                  class="p-1 text-xs text-gray-400 hover:text-white hover:bg-white/5 rounded transition-colors disabled:opacity-30 disabled:pointer-events-none"
                  title="Переместить вверх"
                >
                  ▲
                </button>
                <!-- Move Down -->
                <button 
                  @click="moveCategory(idx, 1)" 
                  :disabled="idx === categories.length - 1"
                  class="p-1 text-xs text-gray-400 hover:text-white hover:bg-white/5 rounded transition-colors disabled:opacity-30 disabled:pointer-events-none"
                  title="Переместить вниз"
                >
                  ▼
                </button>

                <button 
                  @click="startEdit(cat)"
                  class="p-2 text-blue-400 hover:text-blue-300 hover:bg-blue-500/10 rounded-lg transition-colors ml-2"
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
                <input v-model="newCategory.icon" type="text" placeholder="" class="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-xl text-center text-white text-sm outline-none focus:ring-2 focus:ring-orange-500">
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
import { ShoppingCartIcon, Bars3Icon as MenuIcon, TagIcon as UtensilsIcon, XMarkIcon as XIcon } from '@heroicons/vue/24/solid'

const activeTab = ref('pos')
const posSubTab = ref('catalog')
const cartAnimated = ref(false)
const products = ref([])
const categories = ref([])
const selectedCategoryId = ref(null)
const cart = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showCategoryModal = ref(false)
const waiterOrders = ref([])

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

const pendingOrdersCount = computed(() => {
  return waiterOrders.value.filter(o => o.status !== 'paid' && o.status !== 'cancelled' && !o.is_paid).length
})

const fetchProducts = async () => {
  try {
    const res = await api.get('/bar/products')
    products.value = res.data
  } catch(e) {}
}

const fetchCategories = async () => {
  try {
    const res = await api.get('/bar/categories')
    categories.value = res.data
  } catch(e) {}
}

const createCategory = async () => {
  try {
    await api.post('/bar/categories', newCategory.value)
    newCategory.value = { name: '', description: '', color: '#4B5563', icon: '' }
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
    icon: cat.icon || '🍽️',
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

const moveCategory = async (index, direction) => {
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= categories.value.length) return
  
  // Swap locally
  const temp = categories.value[index]
  categories.value[index] = categories.value[targetIndex]
  categories.value[targetIndex] = temp
  
  try {
    const ids = categories.value.map(c => c.id)
    await api.put('/bar/categories/reorder', ids)
    toast.success('Порядок категорий обновлен')
    await fetchCategories()
    await fetchProducts() // Refresh products catalog mapping
  } catch (e) {
    toast.error('Не удалось обновить порядок категорий')
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

const fetchOrders = async () => {
  try {
    const res = await api.get('/bar/orders')
    // Filter to show active orders that are not served/paid
    waiterOrders.value = res.data.filter(o => o.status !== 'paid' && o.status !== 'cancelled' && !o.is_paid)
  } catch(e) {}
}

const createProduct = async () => {
  try {
    await api.post('/bar/products', newProduct.value)
    showAddModal.value = false
    newProduct.value = { name: '', price: 0, stock_quantity: 0, category_id: null }
    toast.success('Товар добавлен в меню')
    fetchProducts()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка добавления')
  }
}

const updateStatus = async (orderId, newStatus, markPaid = false) => {
  try {
    let url = `/bar/orders/${orderId}/status?status=${newStatus}`
    if (markPaid) {
      url += `&is_paid=true`
    }
    await api.post(url)
    toast.success('Статус заказа обновлен')
    fetchOrders()
  } catch (e) {
    toast.error('Не удалось обновить статус')
  }
}

const getStatusLabel = (status) => {
  const map = {
    new: 'Новый заказ',
    preparing: 'Готовится',
    ready: 'Готов к выдаче',
    served: 'Подан',
    paid: 'Оплачен',
    cancelled: 'Отменен'
  }
  return map[status] || status
}

const getStatusBadgeClass = (status) => {
  const map = {
    new: 'bg-red-500/10 text-red-400 border border-red-500/20',
    preparing: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    ready: 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20',
    served: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
    paid: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
  }
  return map[status] || 'bg-gray-500/10 text-gray-400 border border-gray-500/20'
}

let pollInterval;
onMounted(() => {
  fetchProducts()
  fetchCategories()
  fetchOrders()
  pollInterval = setInterval(fetchOrders, 5000) // Poll for new orders every 5s
})

onUnmounted(() => {
  clearInterval(pollInterval)
})

const filteredProducts = computed(() => {
  return products.value.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategoryId.value === null || p.category_id === selectedCategoryId.value
    return matchesSearch && matchesCategory
  })
})

const addToCart = (product) => {
  if (product.stock_quantity <= 0) {
    toast.warning('Товар закончился на складе!')
    return
  }
  
  const existing = cart.value.find(item => item.product.id === product.id)
  if(existing) {
    if (existing.quantity >= product.stock_quantity) {
      toast.warning('Больше нет в наличии на складе')
      return
    }
    existing.quantity++
  } else {
    cart.value.push({ product, quantity: 1 })
  }
  
  // Trigger cart bounce animation on mobile
  cartAnimated.value = true
  setTimeout(() => {
    cartAnimated.value = false
  }, 300)
}

const increaseQty = (idx) => {
  const item = cart.value[idx]
  if (item.quantity >= item.product.stock_quantity) {
    toast.warning('Превышен остаток товара на складе')
    return
  }
  item.quantity++
}
const decreaseQty = (idx) => {
  if(cart.value[idx].quantity > 1) {
    cart.value[idx].quantity--
  } else {
    cart.value.splice(idx, 1)
  }
}

const subtotal = computed(() => cart.value.reduce((acc, item) => acc + (item.product.price * item.quantity), 0))
const serviceFee = computed(() => 0) // POS checkout at the bar has 0% service fee (self-pickup)
const total = computed(() => subtotal.value)

const checkout = async () => {
  if (cart.value.length === 0) return
  try {
    const payload = {
      items: cart.value.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity
      })),
      lounger_id: null,
      waiter_id: null
    }
    await api.post('/bar/orders', payload)
    toast.success(`Чек на сумму ${total.value} ₸ успешно оплачен!`)
    cart.value = []
    fetchProducts()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Ошибка оплаты')
  }
}
</script>
