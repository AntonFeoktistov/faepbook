import apiClient from './client'
import type { Book, BookCreate, BookUpdate } from '@/types'

export const booksApi = {
  async list(): Promise<Book[]> {
    const { data } = await apiClient.get<Book[]>('/api/v1/books/')
    return data
  },

  async get(id: number): Promise<Book> {
    const { data } = await apiClient.get<Book>(`/api/v1/books/${id}/`)
    return data
  },

  async create(payload: BookCreate): Promise<Book> {
    const { data } = await apiClient.post<Book>('/api/v1/books/', payload)
    return data
  },

  async update(id: number, payload: BookUpdate): Promise<Book> {
    const { data } = await apiClient.patch<Book>(`/api/v1/books/${id}/`, payload)
    return data
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/books/${id}/`)
  },
}