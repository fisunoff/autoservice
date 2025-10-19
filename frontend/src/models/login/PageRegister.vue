<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { LOGIN_NAME } from '@/router'
import api from '@/api/api'
import { setUser } from '@/api/tokensSrvices'

const emit = defineEmits<{
  (ev: 'gotoApp'): void
}>()
const router = useRouter()

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  surname: '',
  name: '',
  patronymic: '',
  tabel_number: '',
  hire_date: '',
  is_admin: false,
  is_mechanic: false,
  is_active: true,
  login: '',
  password: '',
  passwordVerification: '',
})

const validatePassConfirm = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('Пожалуйста, подтвердите пароль'))
  } else if (value !== form.password) {
    callback(new Error('Пароли не совпадают!'))
  } else {
    callback()
  }
}

const rules = reactive<FormRules>({
  surname: [{ required: true, message: 'Введите фамилию', trigger: 'blur' }],
  name: [{ required: true, message: 'Введите имя', trigger: 'blur' }],
  tabel_number: [{ required: true, message: 'Введите табельный номер', trigger: 'blur' }],
  hire_date: [{ required: true, message: 'Выберите дату найма', trigger: 'change' }],
  login: [{ required: true, message: 'Введите логин', trigger: 'blur' }],
  password: [{ required: true, message: 'Введите пароль', trigger: 'blur' }],
  passwordVerification: [{ required: true, validator: validatePassConfirm, trigger: 'blur' }],
})

const handleRegister = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const { passwordVerification, ...payload } = form
        const response = await api.post('/auth/register', payload)
        setUser(response.data.access_token, response.data.refresh_token)
        ElMessage.success('Регистрация прошла успешно!')
        emit('gotoApp')
      } catch (error) {
        console.error('Registration failed:', error)
        ElMessage.error('Произошла ошибка при регистрации.')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<template>
  <main class="flex justify-center items-center min-h-screen bg-gray-100 py-8">
    <el-card class="w-full max-w-2xl">
      <template #header>
        <div class="text-center text-xl font-bold">Регистрация</div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-divider content-position="left">Личные данные</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="Фамилия" prop="surname">
              <el-input v-model="form.surname" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Имя" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="Отчество" prop="patronymic">
              <el-input v-model="form.patronymic" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Табельный номер" prop="tabel_number">
              <el-input v-model="form.tabel_number" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Дата найма" prop="hire_date">
              <el-date-picker
                v-model="form.hire_date"
                type="date"
                placeholder="Выберите дату"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">Роли и доступы</el-divider>
        <el-form-item label="Права пользователя">
          <el-checkbox v-model="form.is_admin" label="Администратор" />
          <el-checkbox v-model="form.is_mechanic" label="Механик" />
          <el-checkbox v-model="form.is_active" label="Активен" />
        </el-form-item>

        <el-divider content-position="left">Данные для входа</el-divider>
        <el-form-item label="Логин" prop="login">
          <el-input v-model="form.login" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Пароль" prop="password">
              <el-input v-model="form.password" type="password" show-password />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Подтверждение пароля" prop="passwordVerification">
              <el-input v-model="form.passwordVerification" type="password" show-password />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item class="mt-6">
          <el-button
            type="primary"
            class="w-full"
            size="large"
            :loading="loading"
            @click="handleRegister(formRef)"
          >
            Зарегистрироваться
          </el-button>
        </el-form-item>
      </el-form>

      <div class="text-center mt-4">
        <el-link type="primary" @click="router.push({ name: LOGIN_NAME })">
          Уже есть профиль? Войти
        </el-link>
      </div>
    </el-card>
  </main>
</template>
