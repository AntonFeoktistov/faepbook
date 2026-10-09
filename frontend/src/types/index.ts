export type CoverType = 'hard' | 'soft' | 'none'

export interface Author {
  id: number
  name: string
  description: string | null
  image_url: string | null
}

export interface AuthorCreate {
  name: string
  description?: string | null
  image_url?: string | null
}

export interface AuthorUpdate {
  name?: string | null
  description?: string | null
  image_url?: string | null
}

export interface Category {
  id: number
  name: string
  description: string | null
}

export interface CategoryCreate {
  name: string
  description?: string | null
}

export interface CategoryUpdate {
  name?: string | null
  description?: string | null
}

export interface Book {
  id: number
  title: string
  author_id: number
  price: string
  discount_percent: string | null
  cover_type: CoverType
  pages_count: number | null
  release_year: number | null
  weight_grams: number | null
  dimensions: string | null
  content_summary: string | null
  quotes: string | null
  author: Author
  categories: Category[]
}

export interface BookCreate {
  title: string
  author_id: number
  price: number | string
  discount_percent?: number | string | null
  cover_type?: CoverType
  pages_count?: number | null
  release_year?: number | null
  weight_grams?: number | null
  dimensions?: string | null
  content_summary?: string | null
  quotes?: string | null
  category_ids?: number[]
}

export interface BookUpdate {
  title?: string | null
  author_id?: number | null
  price?: number | string | null
  discount_percent?: number | string | null
  cover_type?: CoverType | null
  pages_count?: number | null
  release_year?: number | null
  weight_grams?: number | null
  dimensions?: string | null
  content_summary?: string | null
  quotes?: string | null
  category_ids?: number[] | null
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  password2: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface TokenResponse {
  access: string
  refresh: string
  token_type?: string
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}