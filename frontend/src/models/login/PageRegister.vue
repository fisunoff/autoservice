<script setup lang="ts">
import { ref } from 'vue'
import { LOGIN_NAME } from '@/router'
import api from '@/api/api.ts'
import { setUser } from '@/api/tokensSrvices.ts'

const emit = defineEmits<{
  (ev: 'gotoApp'): void
}>()
const login = ref('')
const password = ref('')
const passwordVerification = ref('')
const tabelNumber = ref('')
const name = ref('')
const surname = ref('')
const patronymic = ref('')
const hireDate = ref('')
const isAdmin = ref(false)
const isMechanic = ref(false)
const isActive = ref(false)
const onRegister = async () => {
  if (password.value !== passwordVerification.value) return alert('Пароли не совпадают')
  try {
    const response = await api.post('/auth/register', {
      login: login.value,
      password: password.value,
      name: name.value,
      surname: surname.value,
      patronymic: patronymic.value,
      tabel_number: tabelNumber.value,
      hire_date: hireDate.value,
      is_admin: isAdmin.value,
      is_active: isActive.value,
      is_mechanic: isMechanic.value,
    })
    setUser(response.data.accessToken, response.data.refreshToken)
    emit('gotoApp')
  } catch (error) {
    alert('Произошла ошибка при регистрации.')
    console.error('Registration failed:', error)
  }
}
</script>

<template>
  <main class="mx-200 my-60 rounded-md bg-teal-300 flex flex-col gap-2 px-5 py-4">
    <span class="text-xl font-bold">Вход</span>
    <input v-model="surname" placeholder="Введите фамилию" />
    <input v-model="name" placeholder="Введите имя" />
    <input v-model="patronymic" placeholder="Введите отчество" />
    <input v-model="tabelNumber" placeholder="Введите табельный номер" />
    <input v-model="hireDate" placeholder="Введите дату найма" type="date" />

    <div class="flex gap-2 items-center">
      <input id="isAdmin" v-model="isAdmin" type="checkbox" />
      <label for="isAdmin">Админ</label>
    </div>
    <div class="flex gap-2 items-center">
      <input id="isMechanic" v-model="isMechanic" type="checkbox" />
      <label for="isMechanic">Механик</label>
    </div>
    <div class="flex gap-2 items-center">
      <input id="isActive" v-model="isActive" type="checkbox" />
      <label for="isActive">Активный</label>
    </div>

    <input v-model="login" placeholder="Введите логин" />
    <input v-model="password" placeholder="Введите пароль" type="password" />
    <input v-model="passwordVerification" placeholder="Подтвердите пароль" type="password" />

    <RouterLink :to="{ name: LOGIN_NAME }">Уже есть профиль? Войти</RouterLink>
    <button @click="onRegister">Зарегистрироваться</button>
  </main>
</template>

<style scoped></style>
