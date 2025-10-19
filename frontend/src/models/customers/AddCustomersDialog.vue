<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { NewCustomer } from '@/models/customers/PageCustomers.vue'

const props = defineProps<{
  visible: boolean
}>()
const emit = defineEmits(['update:visible', 'save'])

const defaultNewItem: NewCustomer = {
  surname: '',
  name: '',
  patronymic: '',
  phone: '',
}
const newItemForm = reactive<NewCustomer>({ ...defaultNewItem })

watch(
  () => props.visible,
  (newValue) => {
    if (newValue) {
      Object.assign(newItemForm, defaultNewItem)
    }
  },
)

const handleSaveClick = () => {
  if (!newItemForm.surname) {
    ElMessage.warning('Пожалуйста, введите фамилию.')
    return
  }
  if (!newItemForm.name) {
    ElMessage.warning('Пожалуйста, введите имя.')
    return
  }

  emit('save', newItemForm)
}

const handleClose = () => {
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog :model-value="visible" title="Добавить Клиента" width="500px" @close="handleClose">
    <el-form :model="newItemForm" label-width="150px">
      <el-form-item label="Фамилия" required>
        <el-input v-model="newItemForm.surname" />
      </el-form-item>
      <el-form-item label="Имя" required>
        <el-input v-model="newItemForm.name" />
      </el-form-item>
      <el-form-item label="Отчество">
        <el-input v-model="newItemForm.patronymic" />
      </el-form-item>
      <el-form-item label="Номер телефона">
        <el-input v-model="newItemForm.phone" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Отмена</el-button>
        <el-button type="primary" @click="handleSaveClick"> Сохранить </el-button>
      </span>
    </template>
  </el-dialog>
</template>
