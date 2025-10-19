<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { NewCar } from './PageCars.vue'

const props = defineProps<{
  visible: boolean
}>()
const emit = defineEmits(['update:visible', 'save'])

const defaultNewItem: NewCar = {
  brand: '',
  model: '',
  state_number: '',
  vin: '',
  year: new Date().getFullYear(),
}
const newItemForm = reactive<NewCar>({ ...defaultNewItem })

watch(
  () => props.visible,
  (newValue) => {
    if (newValue) {
      Object.assign(newItemForm, defaultNewItem)
      newItemForm.year = new Date().getFullYear()
    }
  },
)

const handleSaveClick = () => {
  if (!newItemForm.brand) {
    ElMessage.warning('Пожалуйста, введите марку автомобиля.')
    return
  }
  if (!newItemForm.model) {
    ElMessage.warning('Пожалуйста, введите модель автомобиля.')
    return
  }
  if (
    !newItemForm.year ||
    newItemForm.year < 1900 ||
    newItemForm.year > new Date().getFullYear() + 1
  ) {
    ElMessage.warning('Пожалуйста, введите корректный год выпуска.')
    return
  }

  emit('save', newItemForm)
}

const handleClose = () => {
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog :model-value="visible" title="Добавить Автомобиль" width="500px" @close="handleClose">
    <el-form :model="newItemForm" label-width="150px">
      <el-form-item label="Марка" required>
        <el-input v-model="newItemForm.brand" />
      </el-form-item>
      <el-form-item label="Модель" required>
        <el-input v-model="newItemForm.model" />
      </el-form-item>
      <el-form-item label="Гос. номер">
        <el-input v-model="newItemForm.state_number" />
      </el-form-item>
      <el-form-item label="VIN">
        <el-input v-model="newItemForm.vin" />
      </el-form-item>
      <el-form-item label="Год выпуска" required>
        <el-input-number
          v-model="newItemForm.year"
          :min="1900"
          :max="new Date().getFullYear() + 1"
        />
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
