<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { RegisterRequest } from '@/types'

const form = reactive<RegisterRequest>({
  username: '',
  email: '',
  password: '',
  password2: '',
})
const error = ref('')
const loading = ref(false)

const authStore = useAuthStore()
const router = useRouter()

async function handleRegister() {
  error.value = ''
  if (form.password !== form.password2) {
    error.value = 'Пароли не совпадают'
    return
  }
  loading.value = true
  try {
    await authStore.register(form)
    router.push('/')
  } catch (e: any) {
    const detail = e.response?.data?.detail
    error.value = typeof detail === 'string'
      ? detail
      : Array.isArray(detail)
        ? detail.map((d: any) => d.msg).join(', ')
        : 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-[calc(100vh-64px)] flex items-center justify-center bg-slate-100 px-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
      <h1 class="text-2xl font-bold text-slate-900 mb-2">Регистрация</h1>
      <p class="text-slate-500 mb-6">Создайте новый аккаунт</p>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Username</label>
          <input
            v-model="form.username"
            required
            minlength="3"
            maxlength="150"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            required
            minlength="8"
            maxlength="128"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Повторите пароль</label>
          <input
            v-model="form.password2"
            type="password"
            required
            minlength="8"
            maxlength="128"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <p v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-200 rounded px-3 py-2">
          {{ error }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-medium py-2.5 rounded-lg transition"
        >
          {{ loading ? 'Создаём…' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="text-center text-sm text-slate-500 mt-6">
        Уже есть аккаунт?
        <RouterLink to="/login" class="text-indigo-600 hover:underline font-medium">
          Войти
        </RouterLink>
      </p>
    </div>
  </div>
</template>