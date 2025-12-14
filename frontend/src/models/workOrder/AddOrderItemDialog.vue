<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'

interface PriceListItem {
  id: number
  title: string
}

interface EditableItem {
  position: { title: string }
  price: number
  quantity: number
}

const props = defineProps<{
  visible: boolean
  mode: 'add' | 'edit'
  title: string
  selectLabel?: string
  itemsList?: PriceListItem[]
  itemToEdit?: EditableItem | null
}>()

const emit = defineEmits(['update:visible', 'save'])

const form = reactive({
  itemId: null as number | null,
  quantity: 1,
  price: 0,
})
watch(
  () => props.visible,
  (isVisible) => {
    if (isVisible) {
      if (props.mode === 'add') {
        form.itemId = null
        form.quantity = 1
        form.price = 0
      } else if (props.mode === 'edit' && props.itemToEdit) {
        form.quantity = props.itemToEdit.quantity
        form.price = props.itemToEdit.price
        form.itemId = null
      }
    }
  },
)

const handleSave = () => {
  if (props.mode === 'add') {
    if (!form.itemId) {
      ElMessage.warning('Пожалуйста, выберите позицию.')
      return
    }
    emit('save', { itemId: form.itemId, quantity: form.quantity })
  } else {
    if (form.price < 0 || form.quantity <= 0) {
      ElMessage.warning('Цена и количество должны быть корректными.')
      return
    }
    emit('save', { price: form.price, quantity: form.quantity })
  }
}

const handleClose = () => {
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog :model-value="visible" :title="title" width="500px" @close="handleClose">
    <el-form :model="form" label-width="120px">
      <template v-if="mode === 'add'">
        <el-form-item :label="selectLabel" required>
          <el-select
            v-model="form.itemId"
            placeholder="Выберите позицию"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="item in itemsList"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </template>
      <template v-if="mode === 'edit' && itemToEdit">
        <el-form-item label="Наименование">
          <el-input :model-value="itemToEdit.position.title" readonly />
        </el-form-item>
        <el-form-item label="Цена" required>
          <el-input-number
            v-model="form.price"
            :min="0"
            :precision="2"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
      </template>

      <el-form-item label="Количество" required>
        <el-input-number
          v-model="form.quantity"
          :min="mode === 'add' ? 1 : 0.01"
          controls-position="right"
          style="width: 100%"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Отмена</el-button>
        <el-button type="primary" @click="handleSave">Сохранить</el-button>
      </span>
    </template>
  </el-dialog>
</template>
