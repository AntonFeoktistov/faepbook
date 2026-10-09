import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { LoginRequest, RegisterRequest, User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => user.value !== null)
  const isAdmin = computed(() => user.value?.is_admin === true)

  async function login(payload: LoginRequest) {
    const tokens = await authApi.login(payload)
    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    await fetchUser()
  }

  async function register(payload: RegisterRequest) {
    const tokens = await authApi.register(payload)
    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    await fetchUser()
  }

  async function fetchUser() {
    try {
      user.value = await authApi.me()
    } catch {
      user.value = null
    }
  }

  async function makeMeAdmin() {
    user.value = await authApi.makeMeAdmin()
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
  }

  return { user, isAuthenticated, isAdmin, login, register, fetchUser, makeMeAdmin, logout }
})