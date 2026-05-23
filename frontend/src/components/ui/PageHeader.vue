<template>
  <header
    v-motion
    :initial="{ opacity: 0, y: 12 }"
    :enter="{ opacity: 1, y: 0, transition: { duration: 400, ease: [0.22, 1, 0.36, 1] } }"
    class="page-toolbar mb-1 sm:mb-2"
  >
    <div class="min-w-0 flex-1">
      <h1 class="page-title text-xl sm:text-2xl md:text-3xl">{{ title }}</h1>
      <p v-if="subtitle" class="page-subtitle mt-0.5 sm:mt-1 line-clamp-2 sm:line-clamp-none">{{ subtitle }}</p>
    </div>
    <div
      v-if="$slots.badge || $slots.actions"
      class="flex flex-wrap items-center gap-2 sm:gap-3 w-full sm:w-auto sm:shrink-0"
    >
      <slot name="badge" />
      <slot name="actions" />
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>
