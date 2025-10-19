<script setup lang="ts">
import NabBar from '@/models/navigation/NabBar.vue'
import router, { LOGIN_NAME } from '@/router'

const logout = () => {
  localStorage.clear()
  router.push({ name: LOGIN_NAME })
}
</script>

<template>
  <div class="flex flex-col gap-1">
    <div class="self-end px-5 pt-2">
      <span class="text-sm mr-2">Фисунов Антон</span>
      <button class="font-bold" @click="logout">Выход</button>
    </div>

    <NabBar />
  </div>
  <RouterView />
</template>

<style scoped></style>
