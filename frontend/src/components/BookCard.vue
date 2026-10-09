<script setup lang="ts">
import type { Book } from '@/types'

defineProps<{ book: Book }>()

function formatPrice(price: string): string {
  return `${Number(price).toFixed(2)} BYN`
}

function finalPrice(book: Book): string {
  if (!book.discount_percent) return formatPrice(book.price)
  const discount = Number(book.discount_percent)
  const price = Number(book.price)
  return formatPrice(((price * (100 - discount)) / 100).toFixed(2))
}
</script>

<template>
  <div class="bg-white rounded-lg shadow p-4 hover:shadow-md transition flex flex-col">
    <h3 class="font-semibold text-lg line-clamp-2">{{ book.title }}</h3>
    <p class="text-sm text-gray-600 mt-1">{{ book.author.name }}</p>

    <div class="mt-2 flex items-center gap-2">
      <span v-if="book.discount_percent" class="text-sm text-gray-400 line-through">
        {{ formatPrice(book.price) }}
      </span>
      <span class="text-lg font-bold text-indigo-600">
        {{ finalPrice(book) }}
      </span>
    </div>

    <div class="mt-3 flex flex-wrap gap-1">
      <span
        v-for="cat in book.categories"
        :key="cat.id"
        class="text-xs bg-slate-100 text-slate-600 rounded px-2 py-0.5"
      >
        {{ cat.name }}
      </span>
    </div>
  </div>
</template>