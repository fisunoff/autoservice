<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { NewWorkerData } from './PageWorkers.vue'

const props = defineProps<{
  visible: boolean
}>()
const emit = defineEmits(['update:visible', 'save'])

const defaultWorkerForm: NewWorkerData = {
  name: '',
  surname: '',
  patronymic: '',
  tabel_number: '',
  hire_date: new Date().toISOString().split('T')[0],
  is_admin: false,
  is_mechanic: false,
  is_active: true,
  login: '',
  password: '',
}
const newWorkerForm = reactive<NewWorkerData>({ ...defaultWorkerForm })

watch(
  () => props.visible,
  (newValue) => {
    if (newValue) {
      Object.assign(newWorkerForm, defaultWorkerForm)
    }
  },
)

const handleSaveClick = () => {
  if (
    !newWorkerForm.name ||
    !newWorkerForm.surname ||
    !newWorkerForm.login ||
    !newWorkerForm.password
  ) {
    ElMessage.warning('Пожалуйста, заполните все обязательные поля (Имя, Фамилия, Логин, Пароль).')
    return
  }
  emit('save', newWorkerForm)
}

const handleClose = () => {
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="Принять нового сотрудника"
    width="600px"
    @close="handleClose"
  >
    <el-form :model="newWorkerForm" label-width="150px">
      <el-form-item label="Фамилия" required
        ><el-input v-model="newWorkerForm.surname"
      /></el-form-item>
      <el-form-item label="Имя" required><el-input v-model="newWorkerForm.name" /></el-form-item>
      <el-form-item label="Отчество"><el-input v-model="newWorkerForm.patronymic" /></el-form-item>
      <el-form-item label="Табельный номер"
        ><el-input v-model="newWorkerForm.tabel_number"
      /></el-form-item>
      <el-form-item label="Дата принятия"
        ><el-date-picker v-model="newWorkerForm.hire_date" type="date" value-format="YYYY-MM-DD"
      /></el-form-item>
      <el-form-item label="Логин" required><el-input v-model="newWorkerForm.login" /></el-form-item>
      <el-form-item label="Пароль" required
        ><el-input v-model="newWorkerForm.password" type="password" show-password
      /></el-form-item>
      <el-form-item label="Роли">
        <el-checkbox v-model="newWorkerForm.is_admin" label="Администратор" border />
        <el-checkbox v-model="newWorkerForm.is_mechanic" label="Механик" border />
      </el-form-item>
      <el-form-item label="Активен">
        <el-switch v-model="newWorkerForm.is_active" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">Отмена</el-button>
      <el-button type="primary" @click="handleSaveClick">Принять на работу</el-button>
    </template>
  </el-dialog>
</template>
