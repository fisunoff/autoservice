<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'

interface NewPriceListItem {
  title: string
  unit: string
  price: number
  in_stock_quantity: number
  is_work: boolean
  using: boolean
}

const props = defineProps<{
  visible: boolean
}>()
const emit = defineEmits(['update:visible', 'save'])

const defaultNewItem: NewPriceListItem = {
  title: '',
  unit: '',
  price: 0,
  in_stock_quantity: 0,
  is_work: false,
  using: true,
}
const newItemForm = reactive<NewPriceListItem>({ ...defaultNewItem })

watch(
  () => props.visible,
  (newValue) => {
    if (newValue) {
      Object.assign(newItemForm, defaultNewItem)
    }
  },
)

const handleSaveClick = () => {
  if (!newItemForm.title) {
    ElMessage.warning('Пожалуйста, введите наименование.')
    return
  }

  emit('save', newItemForm)
}

const handleClose = () => {
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="Добавить новую позицию в прейскурант"
    width="500px"
    @close="handleClose"
  >
    <el-form :model="newItemForm" label-width="150px">
      <el-form-item label="Наименование" required>
        <el-input v-model="newItemForm.title" />
      </el-form-item>
      <el-form-item label="Ед. измерения">
        <el-input v-model="newItemForm.unit" />
      </el-form-item>
      <el-form-item label="Цена">
        <el-input-number v-model="newItemForm.price" :min="0" controls-position="right" />
      </el-form-item>
      <el-form-item v-if="!newItemForm.is_work" label="В наличии">
        <el-input-number
          v-model="newItemForm.in_stock_quantity"
          :min="0"
          controls-position="right"
        />
      </el-form-item>
      <el-form-item label="Это работа?">
        <el-checkbox v-model="newItemForm.is_work" />
      </el-form-item>
      <el-form-item label="Используется">
        <el-checkbox v-model="newItemForm.using" />
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
