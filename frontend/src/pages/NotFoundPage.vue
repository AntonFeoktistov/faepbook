<template>
  <div class="min-h-[calc(100vh-64px)] flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-slate-300">404</h1>
      <p class="text-slate-600 mt-4">Страница не найдена</p>
      <RouterLink to="/" class="inline-block mt-6 text-indigo-600 hover:underline">
        Вернуться на главную
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>