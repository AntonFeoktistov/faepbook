<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <Navbar />
    <RouterView />
  </div>
</template>