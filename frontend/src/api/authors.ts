import apiClient from './client'
import type { Author, AuthorCreate, AuthorUpdate } from '@/types'

export const authorsApi = {
  async list(): Promise<Author[]> {
    const { data } = await apiClient.get<Author[]>('/api/v1/authors/')
    return data
  },

  async create(payload: AuthorCreate): Promise<Author> {
    const { data } = await apiClient.post<Author>('/api/v1/authors/', payload)
    return data
  },

  async update(id: number, payload: AuthorUpdate): Promise<Author> {
    const { data } = await apiClient.patch<Author>(`/api/v1/authors/${id}/`, payload)
    return data
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/authors/${id}/`)
  },
}