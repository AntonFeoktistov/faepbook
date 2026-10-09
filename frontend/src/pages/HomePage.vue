<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { booksApi } from '@/api/books'
import { categoriesApi } from '@/api/categories'
import type { Book, Category } from '@/types'
import BookCard from '@/components/BookCard.vue'

const books = ref<Book[]>([])
const categories = ref<Category[]>([])
const selectedCategory = ref<number | null>(null)
const search = ref('')
const loading = ref(false)

const visibleBooks = computed(() => {
  let result = books.value

  if (selectedCategory.value !== null) {
    result = result.filter((b) =>
      b.categories.some((c) => c.id === selectedCategory.value)
    )
  }

  const q = search.value.trim().toLowerCase()
  if (q) {
    result = result.filter(
      (b) =>
        b.title.toLowerCase().includes(q) ||
        b.author.name.toLowerCase().includes(q)
    )
  }

  return result
})

onMounted(async () => {
  loading.value = true
  try {
    const [b, c] = await Promise.all([booksApi.list(), categoriesApi.list()])
    books.value = b
    categories.value = c
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-slate-900 mb-4">Каталог книг</h1>

      <div class="flex flex-col md:flex-row gap-3">
        <input
          v-model="search"
          type="text"
          placeholder="Поиск по названию или автору…"
          class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />

        <select
          v-model="selectedCategory"
          class="px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option :value="null">Все категории</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">
            {{ c.name }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-center text-slate-500 py-12">Загрузка…</div>

    <div v-else-if="!visibleBooks.length" class="text-center text-slate-500 py-12">
      Ничего не найдено
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <BookCard v-for="book in visibleBooks" :key="book.id" :book="book" />
    </div>
  </div>
</template>