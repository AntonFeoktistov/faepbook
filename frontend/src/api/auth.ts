import apiClient from './client'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '@/types'

export const authApi = {
  async register(payload: RegisterRequest): Promise<TokenResponse> {
    const { data } = await apiClient.post<TokenResponse>('/api/v1/register/', payload)
    return data
  },

  async login(payload: LoginRequest): Promise<TokenResponse> {
    const { data } = await apiClient.post<TokenResponse>('/api/v1/login/', payload)
    return data
  },

  async me(): Promise<User> {
    const { data } = await apiClient.get<User>('/api/v1/me/')
    return data
  },

  async makeMeAdmin(): Promise<User> {
    const { data } = await apiClient.post<User>('/api/v1/make-me-admin/')
    return data
  },
}