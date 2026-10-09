<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

async function handleMakeAdmin() {
  try {
    await authStore.makeMeAdmin()
  } catch (e) {
    console.error(e)
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="bg-white rounded-2xl shadow p-6">
      <h1 class="text-2xl font-bold text-slate-900 mb-4">Профиль</h1>

      <dl class="space-y-2 text-slate-700">
        <div class="flex justify-between border-b border-slate-100 py-2">
          <dt class="font-medium">ID</dt>
          <dd>{{ authStore.user?.id }}</dd>
        </div>
        <div class="flex justify-between border-b border-slate-100 py-2">
          <dt class="font-medium">Username</dt>
          <dd>{{ authStore.user?.username }}</dd>
        </div>
        <div class="flex justify-between border-b border-slate-100 py-2">
          <dt class="font-medium">Email</dt>
          <dd>{{ authStore.user?.email }}</dd>
        </div>
        <div class="flex justify-between border-b border-slate-100 py-2">
          <dt class="font-medium">Админ</dt>
          <dd>{{ authStore.user?.is_admin ? 'Да' : 'Нет' }}</dd>
        </div>
      </dl>

      <div class="mt-6 flex gap-3 flex-wrap">
        <button
          v-if="!authStore.isAdmin"
          @click="handleMakeAdmin"
          class="bg-amber-500 hover:bg-amber-600 text-white font-medium px-4 py-2 rounded-lg transition"
        >
          Сделать меня админом (dev)
        </button>

        <a
          v-if="authStore.isAdmin"
          href="http://localhost:8000/admin"
          target="_blank"
          class="bg-slate-800 hover:bg-slate-900 text-white font-medium px-4 py-2 rounded-lg transition"
        >
          Открыть SQLAdmin
        </a>

        <button
          @click="handleLogout"
          class="border border-slate-300 hover:border-slate-400 text-slate-700 font-medium px-4 py-2 rounded-lg transition"
        >
          Выйти
        </button>
      </div>
    </div>
  </div>
</template>