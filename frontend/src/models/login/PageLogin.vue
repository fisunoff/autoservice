<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { REGISTER_NAME } from '@/router'
import api from '@/api/api'
import { setUser } from '@/api/tokensSrvices'

const emit = defineEmits<{
  (ev: 'gotoApp'): void
}>()
const router = useRouter()

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  login: '',
  password: '',
})

const rules = reactive<FormRules>({
  login: [{ required: true, message: 'Пожалуйста, введите логин', trigger: 'blur' }],
  password: [{ required: true, message: 'Пожалуйста, введите пароль', trigger: 'blur' }],
})

const handleLogin = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const response = await api.post('/auth/login', form)
        setUser(response.data.access_token, response.data.refresh_token)
        ElMessage.success('Вход выполнен успешно!')
        emit('gotoApp')
      } catch (error) {
        console.error('Login failed:', error)
        ElMessage.error('Неверный логин или пароль.')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <main class="flex justify-center items-center min-h-screen bg-gray-100">
    <el-card class="w-full max-w-sm">
      <template #header>
        <div class="text-center text-xl font-bold">Вход в систему</div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent>
        <el-form-item label="Логин" prop="login">
          <el-input v-model="form.login" placeholder="Введите логин" size="large" clearable />
        </el-form-item>

        <el-form-item label="Пароль" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="Введите пароль"
            size="large"
            show-password
            @keyup.enter="handleLogin(formRef)"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            class="w-full"
            size="large"
            :loading="loading"
            @click="handleLogin(formRef)"
          >
            Войти
          </el-button>
        </el-form-item>
      </el-form>

      <div class="text-center mt-4">
        <el-link type="primary" @click="router.push({ name: REGISTER_NAME })">
          Нет профиля? Зарегистрироваться
        </el-link>
      </div>
    </el-card>
  </main>
</template>
