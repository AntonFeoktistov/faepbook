import apiClient from './client'
import type { Category, CategoryCreate, CategoryUpdate } from '@/types'

export const categoriesApi = {
  async list(): Promise<Category[]> {
    const { data } = await apiClient.get<Category[]>('/api/v1/categories/')
    return data
  },

  async create(payload: CategoryCreate): Promise<Category> {
    const { data } = await apiClient.post<Category>('/api/v1/categories/', payload)
    return data
  },

  async update(id: number, payload: CategoryUpdate): Promise<Category> {
    const { data } = await apiClient.patch<Category>(`/api/v1/categories/${id}/`, payload)
    return data
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/categories/${id}/`)
  },
}