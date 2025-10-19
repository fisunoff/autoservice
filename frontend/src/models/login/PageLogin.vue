<script setup lang="ts">
import { ref } from 'vue'
import { REGISTER_NAME } from '@/router'
import api from '@/api/api.ts'
import { setUser } from '@/api/tokensSrvices.ts'

const emit = defineEmits<{
  (ev: 'gotoApp'): void
}>()
const login = ref('')
const password = ref('')
const onLogin = async () => {
  const response = await api.post('/auth/login', { login: login.value, password: password.value })
  if (response.status === 200) {
    setUser(response.data.accessToken, response.data.refreshToken)
    emit('gotoApp')
  } else {
    alert('Неверный логин или пароль')
  }
}
</script>

<template>
  <main class="mx-200 my-60 rounded-md bg-teal-300 flex flex-col gap-2 px-5 py-4">
    <span class="text-xl font-bold">Вход</span>
    <input v-model="login" placeholder="Введите логин" />
    <input v-model="password" placeholder="Введите пароль" type="password" />
    <RouterLink :to="{ name: REGISTER_NAME }">Нет профиля, создать</RouterLink>
    <button @click="onLogin">Войти</button>
  </main>
</template>

<style scoped></style>
