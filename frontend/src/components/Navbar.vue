<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="bg-slate-900 text-white shadow-lg">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
      <RouterLink to="/" class="text-xl font-bold">Epbook</RouterLink>

      <div class="flex items-center gap-4">
        <RouterLink to="/" class="hover:text-indigo-300">Каталог</RouterLink>

        <template v-if="authStore.isAuthenticated">
          <RouterLink to="/profile" class="hover:text-indigo-300">
            {{ authStore.user?.username }}
          </RouterLink>

          <a
            v-if="authStore.isAdmin"
            href="http://localhost:8000/admin"
            target="_blank"
            class="text-amber-300 hover:text-amber-200"
          >
            Админка
          </a>

          <button
            @click="handleLogout"
            class="text-sm border border-slate-700 hover:border-slate-500 rounded px-3 py-1.5"
          >
            Выйти
          </button>
        </template>

        <template v-else>
          <RouterLink to="/login" class="hover:text-indigo-300">Вход</RouterLink>
          <RouterLink
            to="/register"
            class="bg-indigo-600 hover:bg-indigo-700 rounded px-3 py-1.5"
          >
            Регистрация
          </RouterLink>
        </template>
      </div>
    </div>
  </nav>
</template>