<script setup lang="ts">
import Navbar from '@/models/navigation/Navbar.vue'
</script>

<template>
  <div class="flex flex-col gap-1">
    <div class="flex-end">
      <span>Фисунов Антон</span>
      <ElButton>Выход</ElButton>
    </div>

    <Navbar />
  </div>
  <RouterView />
</template>

<style scoped></style>
